package dao;

import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import java.sql.Connection;

import model.AuthToken;
import model.User;

import static org.junit.Assert.*;

public class AuthTokenDaoTest {
    Database db;
    AuthToken token;

    @Before
    public void setUp() throws Exception {
        //here we can set up any classes or variables we will need for the rest of our tests
        //lets create a new database
        db = new Database();
        //and a new authToken with random data
        token = new AuthToken("111111", "kameronlightheart14");
        //and make sure to initialize our tables since we don't know if our database files exist yet
        db.createTables();
    }

    @After
    public void tearDown() {
        //here we can get rid of anything from our tests we don't want to affect the rest of our program
        //lets clear the tables so that any data we entered for testing doesn't linger in our files
        try {
            db.clearTables();
        } catch(DataAccessException e) {
            e.printStackTrace();
        }
    }


    @Test
    public void insertPass() throws DataAccessException {
        AuthToken compareTest = null;
        try {
            // Open connection, make authDao and insert the authToken
            Connection conn = db.openConnection();
            AuthTokenDao authDao = new AuthTokenDao(conn);
            authDao.insert(token);

            // Try to find the authToken in the database
            compareTest = authDao.find(token.getToken());
            db.closeConnection(true);
        } catch (DataAccessException e) {
            e.printStackTrace();
            db.closeConnection(false);
        }

        // Check if the found token isn't null
        Assert.assertNotNull(compareTest);

        //Compare the found token with the token we started with
        Assert.assertEquals(compareTest, token);
    }

    @Test
    public void insertFail() throws DataAccessException {
        //lets do this test again but this time lets try to make it fail
        boolean didItWork = true;
        try {
            Connection conn = db.openConnection();
            AuthTokenDao authTokenDao = new AuthTokenDao(conn);
            //if we call the function the first time it will insert it successfully
            authTokenDao.insert(token);
            //but our sql table is set up so that "authTokenID" must be unique. So trying to insert it
            //again will cause the function to throw an exception
            authTokenDao.insert(token);
            db.closeConnection(didItWork);
        } catch (DataAccessException e) {
            e.printStackTrace();
            //If we catch an exception we will end up in here, where we can change our boolean to
            //false to show that our function failed to perform correctly
            db.closeConnection(false);
            didItWork = false;
        }
        //Check to make sure that we did in fact enter our catch statement
        assertFalse(didItWork);
        //Since we know our database encountered an error, both instances of insert should have been
        //rolled back. So for added security lets make one more quick check using our find function
        //to make sure that our authToken is not in the database
        //Set our compareTest to an actual authToken
        AuthToken compareTest = token;
        try {
            Connection conn = db.openConnection();
            AuthTokenDao authTokenDao = new AuthTokenDao(conn);
            //and then get something back from our find. If the authToken is not in the database we
            //should have just changed our compareTest to a null object
            compareTest = authTokenDao.find(token.getToken());
            db.closeConnection(true);
        } catch (DataAccessException e) {
            e.printStackTrace();
            db.closeConnection(false);
        }
        //Now make sure that compareTest is indeed null
        assertNull(compareTest);
    }

    @Test
    public void findPass() throws DataAccessException {
        AuthToken foundAuthToken = null;

        //Try to insert an authToken into the table
        try {
            Connection conn = db.openConnection();
            AuthTokenDao authTokenDao = new AuthTokenDao(conn);
            authTokenDao.insert(token);
            db.closeConnection(true);
        } catch(DataAccessException e) {
            db.closeConnection(false);
        }

        //Try to find the authToken inserted
        try {
            Connection conn = db.openConnection();
            AuthTokenDao authTokenDao = new AuthTokenDao(conn);
            foundAuthToken = authTokenDao.find(token.getToken());
            db.closeConnection(true);
        } catch (DataAccessException e) {
            e.printStackTrace();
            db.closeConnection(false);
        }

        Assert.assertEquals(token, foundAuthToken);
    }

    @Test
    public void findFail() throws DataAccessException {
        AuthToken foundAuthToken = null;
        String fakeID = "fake!!";

        //Try to find a nonexistent authToken

        try {
            Connection conn = db.openConnection();
            AuthTokenDao authTokenDao = new AuthTokenDao(conn);
            foundAuthToken = authTokenDao.find(fakeID);
            db.closeConnection(true);
        } catch (DataAccessException e) {
            e.printStackTrace();
            db.closeConnection(false);
        }

        //The authToken should be null
        Assert.assertNull(foundAuthToken);
    }

    @Test
    public void authenticatePass() throws DataAccessException {
        try {
            // Open connection, insert token and try to authenticate
            Connection conn = db.openConnection();
            AuthTokenDao authDao = new AuthTokenDao(conn);
            authDao.insert(token);
            User compareUser = AuthTokenDao.authenticate(token.getToken());

            // Assert if the username of the returned user equals the token given's username
            Assert.assertEquals(token.getUserName(), compareUser.getUsername());

        } catch(DataAccessException e) {
            e.printStackTrace();
            db.closeConnection(false);
        }
    }

    @Test
    public void authenticateFail() throws DataAccessException {
        try {
            // Open connection, insert token and try to authenticate with a false token
            Connection conn = db.openConnection();
            AuthTokenDao authDao = new AuthTokenDao(conn);
            authDao.insert(token);
            User compareUser = AuthTokenDao.authenticate("FalseToken");

            // Assert if the username of the returned user equals the token given's username
            Assert.assertNull(compareUser);

        } catch(DataAccessException e) {
            e.printStackTrace();
            db.closeConnection(false);
        }
    }
}