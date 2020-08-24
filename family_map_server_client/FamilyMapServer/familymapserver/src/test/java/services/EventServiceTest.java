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
import dao.EventDao;
import model.Event;
import model.Person;
import response.EventResponse;
import response.EventResponseMultiple;

import static org.junit.Assert.*;

public class EventServiceTest {
    Event birthEvent;
    Event marrriageEvent;
    Event deathEvent;
    Person person;
    Database db;

    @Before
    public void setUp() throws DataAccessException {
        person = new Person("0", "kameronlightheart14", "Kameron",
                "Lightheart", "m", "", "", "");
        birthEvent = Event.generateBirthEvent(1969, person);
        marrriageEvent = Event.generateBirthEvent(1979, person);
        deathEvent = Event.generateDeathEvent(2016, person);

        db = new Database();
        db.clearTables();
        try {
            Connection conn = db.openConnection();
            EventDao eventDao = new EventDao(conn);
            eventDao.insert(birthEvent);
            eventDao.insert(marrriageEvent);
            eventDao.insert(deathEvent);
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
    public void getEventPass() throws DataAccessException {
        EventResponse eventResponse = EventService.getEvent(birthEvent.getEventID());
        Assert.assertEquals(eventResponse.generateEvent(), birthEvent);
    }

    @Test
    public void getEventFail() throws DataAccessException {
        EventResponse eventResponse = EventService.getEvent("FakeEvent");
        Assert.assertNull(eventResponse);
    }

    @Test
    public void getEventMultiplePass()  throws DataAccessException {
        EventResponseMultiple eventResponse = EventService.getEventMultiple(person.getDescendant());
        // Get Json of events
        Gson gson = new Gson();
        String expected = gson.toJson(eventResponse, EventResponseMultiple.class);
        // Test the serialized response we found
        String actual= eventResponse.serialize();
        // Check if they are equal
        Assert.assertEquals(actual, expected);
    }

    @Test public void getEventsFAIL() throws DataAccessException {

        // try to call for nonexistent user
        EventResponseMultiple response = EventService.getEventMultiple("kameron");

        // resulting response should have no events
        Assert.assertEquals(response.getData().size(), 0);

    }
}