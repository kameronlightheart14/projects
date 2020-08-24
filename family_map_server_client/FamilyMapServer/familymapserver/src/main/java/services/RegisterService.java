package services;

import java.sql.Connection;
import java.util.UUID;

import dao.DataAccessException;
import dao.Database;
import dao.PersonDao;
import dao.UserDao;
import model.Person;
import model.User;
import request.LoginRequest;
import request.RegisterRequest;
import response.LoginResponse;

/**
 * RegisterService takes in a request and takes care of it by adding new data via the dao
 *
 * @author Kameron Lightheart
 *
 * 2/13/19
 */
public class RegisterService {

    public static final int DEFAULT_GEN_FILL = 4;

    /**
     * @param request
     * @return RegisterResponse object
     * @throws dao.DataAccessException
     */
    public static LoginResponse register(RegisterRequest request) throws DataAccessException {
        Person person = new Person(
                UUID.randomUUID().toString(),
                request.getUsername(),
                request.getFirstName(),
                request.getLastName(),
                request.getGender(),
                "", "", ""
        );

        User user = new User(
                request.getUsername(),
                request.getPassword(),
                request.getEmail(),
                request.getFirstName(),
                request.getLastName(),
                request.getGender(),
                person.getPersonID()
        );

        Database db = new Database();
        try {
            Connection conn = db.openConnection();
            UserDao userDao = new UserDao(conn);
            userDao.insert(user);
            PersonDao personDao = new PersonDao(conn);
            personDao.insert(user.generatePerson());
            db.closeConnection(true);
        } catch(DataAccessException e) {
            db.closeConnection(false);
            throw e;
        }

        FillService.fill(user.getUsername(), DEFAULT_GEN_FILL);

        LoginRequest loginRequest = new LoginRequest(user.getUsername(), user.getPassword());

        return LoginService.login(loginRequest);
    }
}
