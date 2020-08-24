package services;

import java.sql.Connection;
import java.util.UUID;

import dao.AuthTokenDao;
import dao.DataAccessException;
import dao.Database;
import dao.UserDao;
import model.AuthToken;
import model.User;
import request.LoginRequest;
import response.LoginResponse;

/**
 * LoginService takes in a request and takes care of it by adding new data via the dao
 *
 * @author Kameron Lightheart
 *
 * 2/13/19
 */
public class LoginService {
    /**
     * @param request
     * @return LoginResponse object
     * @throws dao.DataAccessException
     */
    public static LoginResponse login(LoginRequest request) throws DataAccessException {

        Database db = new Database();
        LoginResponse loginResponse;
        try {
            Connection conn = db.openConnection();
            UserDao userDao = new UserDao(conn);
            AuthToken authToken = null;

            User user = userDao.find(request.getUsername());

            if (user == null) {
                throw new DataAccessException("User not found");
            }

            if (!user.getPassword().equals(request.getPassword())) {
                throw new DataAccessException("Wrong password");
            }

            if (user.getPassword().equals(request.getPassword())) {
                String token = UUID.randomUUID().toString();
                authToken = new AuthToken(token, request.getUsername());
                AuthTokenDao authTokenDao = new AuthTokenDao(conn);
                authTokenDao.insert(authToken);
            }

            loginResponse = new LoginResponse(
                    authToken.getToken(),
                    authToken.getUserName(),
                    user.getPersonID()
            );
            db.closeConnection(true);
        } catch(DataAccessException e) {
            e.printStackTrace();
            db.closeConnection(false);
            throw e;
        }
        return loginResponse;
    }
}
