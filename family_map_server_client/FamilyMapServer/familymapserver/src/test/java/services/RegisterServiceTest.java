package services;

import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import java.sql.SQLException;

import dao.DataAccessException;
import dao.Database;
import request.RegisterRequest;
import response.LoginResponse;

import static org.junit.Assert.*;

public class RegisterServiceTest {

    RegisterRequest request;
    LoginResponse expectedResponse;
    Database db;

    @Before
    public void setUp() {
        db = new Database();
        try {
            db.clearTables();
            db.createTables();
        } catch(DataAccessException e)
        {
            e.printStackTrace();
        }
        request = new RegisterRequest("kameronlightheart14",
                "KingdomHeartsRulez", "kameronlightheart14@gmail.com",
                "Kameron", "Lightheart", "m");
        expectedResponse = new LoginResponse("KingdomHeartsRulez",
                "kameronlightheart14", "");
    }

    @After
    public void tearDown() {
        try {
            db.clearTables();
        } catch(DataAccessException e)
        {
            e.printStackTrace();
        }
    }

    @Test
    public void registerPass() {
        try {
            LoginResponse response = RegisterService.register(request);

            Assert.assertEquals(response.getUserName(), expectedResponse.getUserName());
        } catch(DataAccessException e) {
            e.printStackTrace();
        }
    }

    @Test
    public void registerFail() throws DataAccessException {
        try {
            // Register user
            db.clearTables();
            LoginResponse response = RegisterService.register(request);
            Assert.assertEquals(response.getUserName(), expectedResponse.getUserName());

        } catch(DataAccessException e) {
            e.printStackTrace();
        }

        // Attempt to register again
        try {
            RegisterService.register(request);
        } catch(DataAccessException e) {
            Assert.assertNotNull(e);
        }
    }
}