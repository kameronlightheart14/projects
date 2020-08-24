package services;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import java.sql.Connection;
import java.util.ArrayList;

import dao.DataAccessException;
import dao.Database;
import dao.EventDao;
import dao.PersonDao;
import dao.UserDao;
import model.Event;
import model.Person;
import model.User;
import request.LoadRequest;

import static org.junit.Assert.*;

public class LoadServiceTest {
    Event birthEvent;
    Event marrriageEvent;
    Event deathEvent;
    Person person1;
    Person person2;
    Person person3;
    User user1;
    User user2;
    User user3;
    ArrayList<Person> people = new ArrayList<>();
    ArrayList<Event> events = new ArrayList<>();
    ArrayList<User> users = new ArrayList<>();
    LoadRequest request;


    @Before
    public void setUp() throws  DataAccessException {
        person1 = new Person("0", "kameronlightheart14", "Kameron",
                "Lightheart", "m", "", "", "");
        person2 = new Person("1", "kameronlightheart", "Kameron",
                "Lightheart", "m", "", "", "");
        person3 = new Person("2", "kameronlightheart1", "Kameron",
                "Lightheart", "m", "", "", "");
        birthEvent = Event.generateBirthEvent(1969, person1);
        marrriageEvent = Event.generateBirthEvent(1979, person1);
        deathEvent = Event.generateDeathEvent(2016, person1);
        user1 = new User("kameronlightheart14", "KingdomHeartsRulez",
                "kameronlightheart14@gmail.com", "Kameron", "Lightheart",
                "m", "0");
        user2 = new User("kameronlightheart", "KingdomHeartsRulez",
                "kameronlightheart14@gmail.com", "Kameron", "Lightheart",
                "m", "0");
        user3 = new User("kameronlightheart1", "KingdomHeartsRulez",
                "kameronlightheart14@gmail.com", "Kameron", "Lightheart",
                "m", "0");
        people.add(person1);
        people.add(person2);
        people.add(person3);
        events.add(birthEvent);
        events.add(deathEvent);
        events.add(marrriageEvent);
        users.add(user1);
        users.add(user2);
        users.add(user3);
        request = new LoadRequest(users, people, events);
        Database db = new Database();
        db.clearTables();
    }

    @Test
    public void load() throws  DataAccessException {
         LoadService.load(request);

         Database db = new Database();
         try {
             Connection conn = db.openConnection();
             UserDao userDao = new UserDao(conn);
             PersonDao personDao = new PersonDao(conn);
             EventDao eventDao = new EventDao(conn);
             ArrayList<Event> compareTest = eventDao.findMany(person1.getDescendant());
             for (Person person : people) {
                 Assert.assertNotNull(personDao.find(person.getPersonID()));
             }
             for (User user : users) {
                 Assert.assertNotNull(userDao.find(user.getUsername()));
             }
             Assert.assertEquals(events, compareTest);
             db.closeConnection(true);
         } catch(DataAccessException e) {
             db.closeConnection(false);
             throw e;
         }


    }

    @Test(expected = DataAccessException.class)
    public void loadFail() throws DataAccessException {
        ArrayList<User> emptyUsers = new ArrayList<>();
        ArrayList<Person> emptyPeople = new ArrayList<>();
        ArrayList<Event> emptyEvents = new ArrayList<>();
        LoadRequest emptyRequest = new LoadRequest(emptyUsers, emptyPeople, emptyEvents);


        LoadService.load(emptyRequest);
    }
}