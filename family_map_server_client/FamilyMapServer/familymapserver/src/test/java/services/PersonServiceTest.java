package services;

import com.google.gson.Gson;

import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import java.sql.Connection;
import java.util.ArrayList;

import dao.DataAccessException;
import dao.Database;
import dao.PersonDao;
import model.Person;
import response.EventResponseMultiple;
import response.PersonResponse;
import response.PersonResponseMultiple;

import static org.junit.Assert.*;

public class PersonServiceTest {
    Person person1;
    Person person2;
    Person person3;
    Database db;

    @Before
    public void setUp() throws DataAccessException {
        person1 = new Person("0", "kameronlightheart14", "Kameron",
                "Lightheart", "m", "", "", "");
        person2 = new Person("1", "kameronlightheart", "Kameron",
                "Lightheart", "m", "", "", "");
        person3 = new Person("2", "kameronlightheart1", "Kameron",
                "Lightheart", "m", "", "", "");

        db = new Database();
        db.clearTables();
        try {
            Connection conn = db.openConnection();
            PersonDao PersonDao = new PersonDao(conn);
            PersonDao.insert(person1);
            PersonDao.insert(person2);
            PersonDao.insert(person3);
            db.closeConnection(true);
        } catch(DataAccessException e) {
            db.closeConnection(false);
            e.printStackTrace();
        }
    }

    @After
    public void tearDown() throws DataAccessException {
        db.clearTables();
    }

    @Test
    public void getPersonPass() throws DataAccessException {
        PersonResponse personResponse = PersonService.getPerson(person1.getPersonID());
        Assert.assertEquals(personResponse.generatePerson(), person1);
    }

    @Test
    public void getPersonFail() throws DataAccessException {
        PersonResponse personResponse = PersonService.getPerson("FakePerson");
        Assert.assertNull(personResponse);
    }

    @Test
    public void getPersonMultiplePass()  throws DataAccessException {
        PersonResponseMultiple PersonResponse = PersonService.getPersonMultiple(person1.getDescendant());
        // Get Json of Persons
        Gson gson = new Gson();
        String expected = gson.toJson(PersonResponse, PersonResponseMultiple.class);
        // Test the serialized response we found
        String actual= PersonResponse.serialize();
        // Check if they are equal
        Assert.assertEquals(actual, expected);
    }

    @Test public void getPersonFAIL() throws DataAccessException {

        // try to call for nonexistent user
        PersonResponseMultiple response = PersonService.getPersonMultiple("kameron");

        // resulting response should have no events
        Assert.assertEquals(response.getData().size(), 0);
    }
}