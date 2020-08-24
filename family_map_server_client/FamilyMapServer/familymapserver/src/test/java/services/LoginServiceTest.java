package services;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import java.sql.Connection;

import dao.DataAccessException;
import dao.Database;
import dao.UserDao;
import model.Person;
import model.User;
import request.LoginRequest;
import response.LoginResponse;

import static org.junit.Assert.*;

public class LoginServiceTest {
    private LoginRequest loginRequest;
    private LoginRequest fakeLogin;
    private LoginResponse loginResponse;
    private User user;

    @Before
    public void setUp() throws DataAccessException {

        user = new User(
                "kameronlightheart14",
                "KingdomHeartsRulez",
                "kameronlightheart14@gmail.com",
                "Kameron",
                "Lightheart",
                "m",
                "00000"
        );
        Database db = new Database();
        try {
            db.clearTables();
            db.createTables();
            Connection conn = db.openConnection();
            UserDao userDao = new UserDao(conn);
            userDao.insert(user);
            db.closeConnection(true);
        } catch(DataAccessException e) {
            e.printStackTrace();
            db.closeConnection(false);
        }

        loginRequest = new LoginRequest(
                "kameronlightheart14",
                "KingdomHeartsRulez"
        );
        loginResponse = new LoginResponse(
                "KingdomHeartsRulez",
                "kameronlightheart14",
                ""
        );
        fakeLogin = new LoginRequest("FAKE", "FAKE");
    }

    @Test
    public void loginPass() {
        try {
            Assert.assertEquals(LoginService.login(loginRequest).getUserName(), loginResponse.getUserName());
        } catch(DataAccessException e) {
            e.printStackTrace();
        }
    }

    @Test(expected = DataAccessException.class)
    public void loginFail() throws DataAccessException {
        LoginService.login(fakeLogin);
    }
}