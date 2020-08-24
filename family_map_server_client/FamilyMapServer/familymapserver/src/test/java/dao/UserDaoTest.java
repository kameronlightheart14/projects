package dao;

import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;

import model.User;

import static org.junit.Assert.*;

/**
 * @author Kameron Lightheart
 *
 * 2/22/19
 */
public class UserDaoTest {
    Database db;
    User user1;
    User user2;
    User user3;
    ArrayList<User> users = new ArrayList<>();
    ArrayList<User> duplicateUsers = new ArrayList<>();

    @Before
    public void setUp() throws Exception {
        //here we can set up any classes or variables we will need for the rest of our tests
        //lets create a new database
        db = new Database();
        //and a new user with random data
        user1 = new User("kameronlightheart14", "KingdomHeartsRulez",
                "kameronlightheart14@gmail.com", "Kameron", "Lightheart",
                "m", "0");
        user2 = new User("kameronlightheart14", "KingdomHeartsRulez",
                "kameronlightheart14@gmail.com", "Kameron", "Lightheart",
                "m", "0");
        user3 = new User("kameronlightheart14", "KingdomHeartsRulez",
                "kameronlightheart14@gmail.com", "Kameron", "Lightheart",
                "m", "0");
        users.add(user1);
        users.add(user2);
        users.add(user3);
        duplicateUsers.add(user1);
        duplicateUsers.add(user1);
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
    public void insertPass() throws Exception {
        //We want to make sure insert works
        //First lets create an User that we'll set to null. We'll use this to make sure what we put
        //in the database is actually there.
        User compareTest = null;
        //Let's clear the database as well so any lingering data doesn't affect our tests
        db.clearTables();
        try {
            //Let's get our connection and make a new DAO
            Connection conn = db.openConnection();
            UserDao userDao = new UserDao(conn);
            //While insert returns a bool we can't use that to verify that our function actually worked
            //only that it ran without causing an error
            userDao.insert(user1);
            //So lets use a find function to get the user that we just put in back out
            compareTest = userDao.find(user1.getUsername());
            db.closeConnection(true);
        } catch (DataAccessException e) {
            e.printStackTrace();
            db.closeConnection(false);
        }
        //First lets see if our find found anything at all. If it did then we know that if nothing
        //else something was put into our database, since we cleared it in the beginning
        assertNotNull(compareTest);
        //Now lets make sure that what we put in is exactly the same as what we got out. If this
        //passes then we know that our insert did put something in, and that it didn't change the
        //data in any way
        assertEquals(user1, compareTest);

    }

    @Test
    public void insertFail() throws Exception {
        //lets do this test again but this time lets try to make it fail
        boolean didItWork = true;
        try {
            Connection conn = db.openConnection();
            UserDao userDao = new UserDao(conn);
            //if we call the function the first time it will insert it successfully
            userDao.insert(user1);
            //but our sql table is set up so that "userID" must be unique. So trying to insert it
            //again will cause the function to throw an exception
            userDao.insert(user1);
            db.closeConnection(didItWork);
        } catch (DataAccessException e) {
            //If we catch an exception we will end up in here, where we can change our boolean to
            //false to show that our function failed to perform correctly
            db.closeConnection(false);
            didItWork = false;
        }
        //Check to make sure that we did in fact enter our catch statement
        assertFalse(didItWork);
        //Since we know our database encountered an error, both instances of insert should have been
        //rolled back. So for added security lets make one more quick check using our find function
        //to make sure that our user is not in the database
        //Set our compareTest to an actual user
        User compareTest = user1;
        try {
            Connection conn = db.openConnection();
            UserDao userDao = new UserDao(conn);
            //and then get something back from our find. If the user is not in the database we
            //should have just changed our compareTest to a null object
            compareTest = userDao.find(user1.getUsername());
            db.closeConnection(true);
        } catch (DataAccessException e) {
            db.closeConnection(false);
        }
        //Now make sure that compareTest is indeed null
        assertNull(compareTest);

    }

    @Test
    public void findPass() throws Exception {
        User foundUser = null;

        //Try to insert an user into the table
        try {
            Connection conn = db.openConnection();
            UserDao userDao = new UserDao(conn);
            userDao.insert(user1);
            db.closeConnection(true);
        } catch(DataAccessException e) {
            e.printStackTrace();
            db.closeConnection(false);
        }

        //Try to find the user inserted
        try {
            Connection conn = db.openConnection();
            UserDao userDao = new UserDao(conn);
            foundUser = userDao.find(user1.getUsername());
            db.closeConnection(true);
        } catch (DataAccessException e) {
            e.printStackTrace();
            db.closeConnection(false);
        }

        Assert.assertEquals(user1, foundUser);
    }

    @Test
    public void findFail() throws Exception {

        User foundUser = null;
        String fakeID = "fake!!";

        //Try to find a nonexistent user

        try {
            Connection conn = db.openConnection();
            UserDao userDao = new UserDao(conn);
            foundUser = userDao.find(fakeID);
            db.closeConnection(true);
        } catch (DataAccessException e) {
            db.closeConnection(false);
        }

        //The user should be null
        Assert.assertNull(foundUser);
    }

    @Test
    public void deletePass() throws Exception {
        UserDao userDao;
        //Let's clear the database as well so any lingering data doesn't affect our tests
        db.clearTables();
        User foundUser = null;
        try {
            //Let's get our connection and make a new DAO
            Connection conn = db.openConnection();
            userDao = new UserDao(conn);
            //While insert returns a bool we can't use that to verify that our function actually worked
            //only that it ran without causing an error
            userDao.insert(user1);
            foundUser = userDao.find(user1.getUsername());
            db.closeConnection(true);
        } catch (DataAccessException e) {
            e.printStackTrace();
            db.closeConnection(false);
        }

        Assert.assertNotNull(foundUser);

        User nullUser = null;
        // Now clear the tables and check if the user is still there
        db.clearTables();
        try {
            Connection conn = db.openConnection();
            userDao = new UserDao(conn);
            nullUser = userDao.find(user1.getUsername());
            db.closeConnection(true);
        } catch(DataAccessException e) {
            e.printStackTrace();
            db.closeConnection(false);
        }

        Assert.assertNull(nullUser);
    }

    @Test
    public void insertManyPass() throws DataAccessException {
        try {
            Connection conn = db.openConnection();
            UserDao userDao = new UserDao(conn);
            userDao.insertMany(users);
            db.closeConnection(true);
        } catch (DataAccessException e) {
            e.printStackTrace();
            db.closeConnection(false);
        }

        try {
            Connection conn = db.openConnection();
            UserDao userDao = new UserDao(conn);
            ArrayList<User> compareUsers = new ArrayList<>();
            for (User findUser : users) {
                User compareUser = userDao.find(findUser.getUsername());
                if (compareUser == null) {
                    throw new DataAccessException("Could not find user");
                }
                compareUsers.add(compareUser);
            }
            db.closeConnection(true);
            Assert.assertEquals(compareUsers, users);
        }  catch(DataAccessException e) {
            db.closeConnection(false);
            e.printStackTrace();
        }
    }

    @Test(expected = DataAccessException.class)
    public void insertManyFail() throws DataAccessException {
        try {
            db.clearTables();
            Connection conn = db.openConnection();
            UserDao userDao = new UserDao(conn);
            userDao.insertMany(duplicateUsers);
            db.closeConnection(true);
        } catch(DataAccessException e) {
            db.closeConnection(false);
            throw e;
        }

    }
}