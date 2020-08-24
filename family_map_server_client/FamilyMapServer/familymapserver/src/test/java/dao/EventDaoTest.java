package dao;

import model.Event;
import model.Person;

import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;

import org.junit.*;
import static org.junit.Assert.*;

/**
 * @author Kameron Lightheart
 *
 * 2/20/19
 */
public class EventDaoTest {
    Database db;
    Event event;
    ArrayList<Event> events = new ArrayList<>();
    ArrayList<Event> duplicateEvents = new ArrayList<>();

    @Before
    public void setUp() throws Exception {
        //here we can set up any classes or variables we will need for the rest of our tests
        //lets create a new database
        db = new Database();
        //and a new event with random data
        event = new Event("Biking_123A", "Gale", "Gale123A",
                10.3f, 10.3f, "Japan", "Ushiku",
                "Biking_Around", 2020);
        Person person1 = new Person("2", "kameronlightheart1", "Kameron",
                "Lightheart", "m", "", "", "");
        Event birthEvent = Event.generateBirthEvent(1969, person1);
        Event marrriageEvent = Event.generateBirthEvent(1979, person1);
        Event deathEvent = Event.generateDeathEvent(2016, person1);
        events.add(birthEvent);
        events.add(marrriageEvent);
        events.add(deathEvent);
        duplicateEvents.add(event);
        duplicateEvents.add(event);
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
        //First lets create an Event that we'll set to null. We'll use this to make sure what we put
        //in the database is actually there.
        Event compareTest = null;
        //Let's clear the database as well so any lingering data doesn't affect our tests
        db.clearTables();
        try {
            //Let's get our connection and make a new DAO
            Connection conn = db.openConnection();
            EventDao eDao = new EventDao(conn);
            //While insert returns a bool we can't use that to verify that our function actually worked
            //only that it ran without causing an error
            eDao.insert(event);
            //So lets use a find function to get the event that we just put in back out
            compareTest = eDao.find(event.getEventID());
            db.closeConnection(true);
        } catch (DataAccessException e) {
            db.closeConnection(false);
        }
        //First lets see if our find found anything at all. If it did then we know that if nothing
        //else something was put into our database, since we cleared it in the beginning
        assertNotNull(compareTest);
        //Now lets make sure that what we put in is exactly the same as what we got out. If this
        //passes then we know that our insert did put something in, and that it didn't change the
        //data in any way
        assertEquals(event, compareTest);

    }

    @Test
    public void insertFail() throws Exception {
        //lets do this test again but this time lets try to make it fail
        boolean didItWork = true;
        try {
            Connection conn = db.openConnection();
            EventDao eDao = new EventDao(conn);
            //if we call the function the first time it will insert it successfully
            eDao.insert(event);
            //but our sql table is set up so that "eventID" must be unique. So trying to insert it
            //again will cause the function to throw an exception
            eDao.insert(event);
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
        //to make sure that our event is not in the database
        //Set our compareTest to an actual event
        Event compareTest = event;
        try {
            Connection conn = db.openConnection();
            EventDao eDao = new EventDao(conn);
            //and then get something back from our find. If the event is not in the database we
            //should have just changed our compareTest to a null object
            compareTest = eDao.find(event.getEventID());
            db.closeConnection(true);
        } catch (DataAccessException e) {
            db.closeConnection(false);
        }
        //Now make sure that compareTest is indeed null
        assertNull(compareTest);

    }

    @Test
    public void findPass() throws Exception {
        Event foundEvent = null;

        //Try to insert an event into the table
        try {
            Connection conn = db.openConnection();
            EventDao eDao = new EventDao(conn);
            eDao.insert(event);
            db.closeConnection(true);
        } catch(DataAccessException e) {
            db.closeConnection(false);
        }

        //Try to find the event inserted
        try {
          Connection conn = db.openConnection();
          EventDao eDao = new EventDao(conn);
          foundEvent = eDao.find(event.getEventID());
          db.closeConnection(true);
        } catch (DataAccessException e) {
            db.closeConnection(false);
        }

        Assert.assertEquals(event, foundEvent);
    }

    @Test
    public void findFail() throws Exception {

        Event foundEvent = null;
        String fakeID = "fake!!";

        //Try to find a nonexistent event

        try {
            Connection conn = db.openConnection();
            EventDao eDao = new EventDao(conn);
            foundEvent = eDao.find(fakeID);
            db.closeConnection(true);
        } catch (DataAccessException e) {
            db.closeConnection(false);
        }

        //The event should be null
        Assert.assertNull(foundEvent);
    }

    @Test
    public void deletePass() throws Exception {
        EventDao eDao;
        //Let's clear the database as well so any lingering data doesn't affect our tests
        db.clearTables();
        Event foundEvent = null;
        try {
            //Let's get our connection and make a new DAO
            Connection conn = db.openConnection();
            eDao = new EventDao(conn);
            //While insert returns a bool we can't use that to verify that our function actually worked
            //only that it ran without causing an error
            eDao.insert(event);
            foundEvent = eDao.find(event.getEventID());
            db.closeConnection(true);
        } catch (DataAccessException e) {
            e.printStackTrace();
            db.closeConnection(false);
        }

        Assert.assertNotNull(foundEvent);

        Event nullEvent = null;
        // Now clear the tables and check if the event is still there
        db.clearTables();
        try {
            Connection conn = db.openConnection();
            eDao = new EventDao(conn);
            nullEvent = eDao.find(event.getEventID());
            db.closeConnection(true);
        } catch(DataAccessException e) {
            e.printStackTrace();
            db.closeConnection(false);
        }

        Assert.assertNull(nullEvent);
    }

    @Test
    public void insertManyPass() throws DataAccessException {
        try {
            Connection conn = db.openConnection();
            EventDao eventDao = new EventDao(conn);
            eventDao.insertMany(events);
            db.closeConnection(true);
        } catch (DataAccessException e) {
            e.printStackTrace();
            db.closeConnection(false);
        }

        try {
            Connection conn = db.openConnection();
            EventDao eventDao = new EventDao(conn);
            ArrayList<Event> compareEvents = new ArrayList<>();
            for (Event findEvent : events) {
                Event compareEvent = eventDao.find(findEvent.getEventID());
                if (compareEvent == null) {
                    throw new DataAccessException("Could not find event");
                }
                compareEvents.add(compareEvent);
            }
            db.closeConnection(true);
            Assert.assertEquals(compareEvents, events);
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
            EventDao eventDao = new EventDao(conn);
            eventDao.insertMany(duplicateEvents);
            db.closeConnection(true);
        } catch(DataAccessException e) {
            db.closeConnection(false);
            throw e;
        }

    }

    @Test
    public void findManyPass() throws DataAccessException {
        try {
            Connection conn = db.openConnection();
            EventDao eventDao = new EventDao(conn);
            eventDao.insertMany(events);
            db.closeConnection(true);
        } catch (DataAccessException e) {
            e.printStackTrace();
            db.closeConnection(false);
        }

        try {
            Connection conn = db.openConnection();
            EventDao eventDao = new EventDao(conn);
            ArrayList<Event> compareEvents = new ArrayList<>();
            for (Event findEvent : events) {
                Event compareEvent = eventDao.find(findEvent.getEventID());
                if (compareEvent == null) {
                    throw new DataAccessException("Could not find event");
                }
                compareEvents.add(compareEvent);
            }
            db.closeConnection(true);
            Assert.assertEquals(compareEvents, events);
        }  catch(DataAccessException e) {
            db.closeConnection(false);
            e.printStackTrace();
        }
    }

    @Test
    public void findManyFail() throws DataAccessException {
        try {
            Connection conn = db.openConnection();
            EventDao eventDao = new EventDao(conn);
            eventDao.insertMany(events);
            db.closeConnection(true);
        } catch (DataAccessException e) {
            e.printStackTrace();
            db.closeConnection(false);
        }

        try {
            Connection conn = db.openConnection();
            EventDao eventDao = new EventDao(conn);
            ArrayList<Event> foundEvents = eventDao.findMany("FakeUsername");

            Assert.assertEquals(foundEvents.size(), 0);

            db.closeConnection(true);
        } catch(DataAccessException e) {
            db.closeConnection(false);
        }
    }
}