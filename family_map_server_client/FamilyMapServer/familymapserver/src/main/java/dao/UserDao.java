package dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;

import model.User;

/**
 *  UserDao Object that inserts and finds User data stored in the database
 *
 * @author Kameron Lightheart
 */
public class UserDao extends Dao {
    public UserDao(Connection conn) {
        super(conn);
    }

    /**
     * insert() takes a User object and inserts the data into a sql table in the database
     * @param userObject
     * @return boolean
     * @throws DataAccessException
     */
    public boolean insert(User userObject) throws DataAccessException {
        boolean commit = true;
        //We can structure our string to be similar to a sql command, but if we insert question
        //marks we can change them later with help from the statement
        String sql = "INSERT INTO users (userName, password, email, first_name, last_name, " +
                "gender, person_id) VALUES(?,?,?,?,?,?,?)";
        try (PreparedStatement stmt = conn.prepareStatement(sql)) {
            //Using the statements built-in set(type) functions we can pick the question mark we want
            //to fill in and give it a proper value. The first argument corresponds to the first
            //question mark found in our sql String
            stmt.setString(1, userObject.getUsername());
            stmt.setString(2, userObject.getPassword());
            stmt.setString(3, userObject.getEmail());
            stmt.setString(4, userObject.getFirstName());
            stmt.setString(5, userObject.getLastName());
            stmt.setString(6, userObject.getGender());
            stmt.setString(7, userObject.getPersonID());

            stmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
            throw new DataAccessException(e.getMessage());
        }

        return commit;
    }

    /**
     * find() will see if an event with the given ID exists and if so return the user object
     * @param userName
     * @return Event
     * @throws DataAccessException
     */
    @Override
    public User find(String userName) throws DataAccessException {
        User user = null;
        ResultSet rs = null;
        String sql = "SELECT * FROM users WHERE userName = ?;";
        try (PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, userName);
            rs = stmt.executeQuery();
            if (rs.next() == true) {
                user = new User(rs.getString("userName"), rs.getString("password"),
                        rs.getString("email"), rs.getString("first_name"), rs.getString("last_name"),
                        rs.getString("gender"), rs.getString("person_id"));
                rs.close();
                return user;
            }
            rs.close();

        } catch (SQLException e) {
            throw new DataAccessException(e.getMessage());
        }
        return null;
    }
    /**
     * Insert multiple users at once
     *
     * @param usersToInsert
     */
    public void insertMany(ArrayList<User> usersToInsert) throws DataAccessException {
        for (User user : usersToInsert) {
            insert(user);
        }
    }
}
