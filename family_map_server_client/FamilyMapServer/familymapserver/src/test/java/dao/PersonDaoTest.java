package dao;

import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import java.sql.Connection;
import java.util.ArrayList;

import model.Person;

import static org.junit.Assert.*;

/**
 * @author Kameron Lightheart
 *
 * 2/22/19
 */
public class PersonDaoTest {
    Database db;
    Person person;
    Person person1;
    Person person2;
    Person person3;
    ArrayList<Person> people = new ArrayList<>();
    ArrayList<Person> duplicatePeople = new ArrayList<>();

    @Before
    public void setUp() throws Exception {
        //here we can set up any classes or variables we will need for the rest of our tests
        //lets create a new database
        db = new Database();
        //and a new person with random data
        person = new Person("0", "kameronlightheart14", "Kameron",
                "Lightheart", "m", "", "", "");
        person1 = new Person("0", "kameronlightheart14", "Kameron",
                "Lightheart", "m", "", "", "");
        person2 = new Person("1", "kameronlightheart", "Kameron",
                "Lightheart", "m", "", "", "");
        person3 = new Person("2", "kameronlightheart1", "Kameron",
                "Lightheart", "m", "", "", "");
        people.add(person1);
        people.add(person2);
        people.add(person3);
        duplicatePeople.add(person);
        duplicatePeople.add(person);
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
        Person compareTest = null;
        //Let's clear the database as well so any lingering data doesn't affect our tests
        db.clearTables();
        try {
            //Let's get our connection and make a new DAO
            Connection conn = db.openConnection();
            PersonDao personDao = new PersonDao(conn);
            //While insert returns a bool we can't use that to verify that our function actually worked
            //only that it ran without causing an error
            personDao.insert(person);
            //So lets use a find function to get the person that we just put in back out
            compareTest = personDao.find(person.getPersonID());
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
        assertEquals(person, compareTest);

    }

    @Test
    public void insertFail() throws Exception {
        //lets do this test again but this time lets try to make it fail
        boolean didItWork = true;
        try {
            Connection conn = db.openConnection();
            PersonDao personDao = new PersonDao(conn);
            //if we call the function the first time it will insert it successfully
            personDao.insert(person);
            //but our sql table is set up so that "personID" must be unique. So trying to insert it
            //again will cause the function to throw an exception
            personDao.insert(person);
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
        //to make sure that our person is not in the database
        //Set our compareTest to an actual person
        Person compareTest = person;
        try {
            Connection conn = db.openConnection();
            PersonDao personDao = new PersonDao(conn);
            //and then get something back from our find. If the person is not in the database we
            //should have just changed our compareTest to a null object
            compareTest = personDao.find(person.getPersonID());
            db.closeConnection(true);
        } catch (DataAccessException e) {
            db.closeConnection(false);
        }
        //Now make sure that compareTest is indeed null
        assertNull(compareTest);

    }

    @Test
    public void findPass() throws Exception {
        Person foundPerson = null;

        //Try to insert an person into the table
        try {
            Connection conn = db.openConnection();
            PersonDao personDao = new PersonDao(conn);
            personDao.insert(person);
            db.closeConnection(true);
        } catch(DataAccessException e) {
            db.closeConnection(false);
        }

        //Try to find the person inserted
        try {
            Connection conn = db.openConnection();
            PersonDao personDao = new PersonDao(conn);
            foundPerson = personDao.find(person.getPersonID());
            db.closeConnection(true);
        } catch (DataAccessException e) {
            db.closeConnection(false);
        }

        Assert.assertEquals(person, foundPerson);
    }

    @Test
    public void findFail() throws Exception {

        Person foundPerson = null;
        String fakeID = "fake!!";

        //Try to find a nonexistent person

        try {
            Connection conn = db.openConnection();
            PersonDao personDao = new PersonDao(conn);
            foundPerson = personDao.find(fakeID);
            db.closeConnection(true);
        } catch (DataAccessException e) {
            db.closeConnection(false);
        }

        //The person should be null
        Assert.assertNull(foundPerson);
    }

    @Test
    public void deletePass() throws Exception {
        PersonDao personDao;
        //Let's clear the database as well so any lingering data doesn't affect our tests
        db.clearTables();
        Person foundPerson = null;
        try {
            //Let's get our connection and make a new DAO
            Connection conn = db.openConnection();
            personDao = new PersonDao(conn);
            //While insert returns a bool we can't use that to verify that our function actually worked
            //only that it ran without causing an error
            personDao.insert(person);
            foundPerson = personDao.find(person.getPersonID());
            db.closeConnection(true);
        } catch (DataAccessException e) {
            e.printStackTrace();
            db.closeConnection(false);
        }

        Assert.assertNotNull(foundPerson);

        Person nullPerson = null;
        // Now clear the tables and check if the person is still there
        db.clearTables();
        try {
            Connection conn = db.openConnection();
            personDao = new PersonDao(conn);
            nullPerson = personDao.find(person.getPersonID());
            db.closeConnection(true);
        } catch(DataAccessException e) {
            e.printStackTrace();
            db.closeConnection(false);
        }

        Assert.assertNull(nullPerson);
    }

    @Test
    public void insertManyPass() throws DataAccessException {
        try {
            Connection conn = db.openConnection();
            PersonDao personDao = new PersonDao(conn);
            personDao.insertMany(people);
            db.closeConnection(true);
        } catch (DataAccessException e) {
            e.printStackTrace();
            db.closeConnection(false);
        }

        try {
            Connection conn = db.openConnection();
            PersonDao personDao = new PersonDao(conn);
            ArrayList<Person> comparePeople = new ArrayList<>();
            for (Person findPerson : people) {
                Person comparePerson = personDao.find(findPerson.getPersonID());
                if (comparePerson == null) {
                    throw new DataAccessException("Could not find person");
                }
                comparePeople.add(comparePerson);
            }
            db.closeConnection(true);
            Assert.assertEquals(comparePeople, people);
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
            PersonDao personDao = new PersonDao(conn);
            personDao.insertMany(duplicatePeople);
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
            PersonDao personDao = new PersonDao(conn);
            personDao.insertMany(people);
            db.closeConnection(true);
        } catch (DataAccessException e) {
            e.printStackTrace();
            db.closeConnection(false);
        }

        try {
            Connection conn = db.openConnection();
            PersonDao personDao = new PersonDao(conn);
            ArrayList<Person> comparePeople = new ArrayList<>();
            for (Person findPerson : people) {
                Person comparePerson = personDao.find(findPerson.getPersonID());
                if (comparePerson == null) {
                    throw new DataAccessException("Could not find person");
                }
                comparePeople.add(comparePerson);
            }
            db.closeConnection(true);
            Assert.assertEquals(comparePeople, people);
        }  catch(DataAccessException e) {
            db.closeConnection(false);
            e.printStackTrace();
        }
    }

    @Test
    public void findManyFail() throws DataAccessException {
        try {
            Connection conn = db.openConnection();
            PersonDao personDao = new PersonDao(conn);
            personDao.insertMany(people);
            db.closeConnection(true);
        } catch (DataAccessException e) {
            e.printStackTrace();
            db.closeConnection(false);
        }

        try {
            Connection conn = db.openConnection();
            PersonDao personDao = new PersonDao(conn);
            ArrayList<Person> foundPeople = personDao.findMany("FakeUsername");

            Assert.assertEquals(foundPeople.size(), 0);

            db.closeConnection(true);
        } catch(DataAccessException e) {
            db.closeConnection(false);
        }
    }
}