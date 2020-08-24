package dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

import model.AuthToken;
import model.User;

/**
 *  AuthTokenDao Object that inserts and finds AuthToken data stored in the database
 *
 * @author Kameron Lightheart
 */
public class AuthTokenDao extends Dao {

    public AuthTokenDao(Connection conn) {
        super(conn);
    }

    /**
     * insert() takes a AuthToken and inserts the data into a sql table in the database
     * @param authTokenObject
     * @return boolean
     * @throws DataAccessException
     */
    public boolean insert(AuthToken authTokenObject) throws DataAccessException {
        boolean commit = true;
        //We can structure our string to be similar to a sql command, but if we insert question
        //marks we can change them later with help from the statement
        String sql = "INSERT INTO auth_tokens (token, user_id) VALUES(?,?)";
        try (PreparedStatement stmt = conn.prepareStatement(sql)) {
            //Using the statements built-in set(type) functions we can pick the question mark we want
            //to fill in and give it a proper value. The first argument corresponds to the first
            //question mark found in our sql String
            stmt.setString(1, authTokenObject.getToken());
            stmt.setString(2, authTokenObject.getUserName());

            stmt.executeUpdate();
        } catch (SQLException e) {
            commit = false;
            throw new DataAccessException(e.getMessage());
        }

        return commit;
    }

    /**
     * find() will see if an event with the given ID exists and if so return the AuthToken object
     * @param token
     * @return AuthToken
     * @throws DataAccessException
     */
    @Override
    public AuthToken find(String token) throws DataAccessException {
        AuthToken authToken = null;
        ResultSet rs = null;
        String sql = "SELECT * FROM auth_tokens WHERE token = ?;";
        try (PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, token);
            rs = stmt.executeQuery();
            if (rs.next() == true) {
                 authToken = new AuthToken(rs.getString("token"), rs.getString("user_id"));
                rs.close();
                return authToken;
            }
            rs.close();

        } catch (SQLException e) {
            throw new DataAccessException(e.getMessage());
        }
        return null;
    }

    public static User authenticate(String token) throws DataAccessException {
        Database db = new Database();
        User user;
        try {
            Connection conn = db.openConnection();
            AuthTokenDao authDao = new AuthTokenDao(conn);
            AuthToken foundToken = authDao.find(token);
            if (foundToken == null) {
                throw new DataAccessException("No user is found for given AuthToken");
            }
            UserDao userDao = new UserDao(conn);
            user = userDao.find(foundToken.getUserName());
            db.closeConnection(true);
            if (user != null) {
                return user;
            }
            else {
                throw new DataAccessException("AuthToken found, but no user associated in DB");
            }
        } catch (DataAccessException e) {
            db.closeConnection(false);
            throw e;
        }
    }
}
