package familytree;

import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import java.sql.Connection;

import dao.DataAccessException;
import dao.Database;
import dao.EventDao;
import dao.PersonDao;
import model.Event;
import model.Model;
import model.Person;
import model.User;

public class FamilyTreeNodeTest {
    private Database db;
    private User user;
    private Person person;
    private FamilyTreeNode node;

    @Before
    public void setUp() {
        try {
            db = new Database();
            db.clearTables();
            db.createTables();
        } catch(DataAccessException e) {
            e.printStackTrace();
        }
        user = new User("kameronlightheart14", "KingdomHeartsRulez",
                "kameronlightheart14@gmail.com", "Kameron", "Lightheart",
                "m", Model.generateUUID());
        person = Person.generateUserPerson(user);
        node = new FamilyTreeNode(person);
        node.addEvent(Event.generateBirthEvent(2020, person));
    }

    @After
    public void tearDown() throws DataAccessException {
        db.clearTables();
    }

    @Test
    public void addToDatabasePass() throws DataAccessException {
        Database db = new Database();
        try {
            Connection conn = db.openConnection();
            node.addToDatabase(conn);

            PersonDao personDao = new PersonDao(conn);
            EventDao eventDao = new EventDao(conn);

            Event compareEvent = eventDao.find(node.getEvents().get(0).getEventID());
            Person comparePerson = personDao.find(person.getPersonID());

            Assert.assertEquals(compareEvent, node.getEvents().get(0));
            Assert.assertEquals(comparePerson, person);

            db.closeConnection(true);
        } catch(DataAccessException e) {
            db.closeConnection(false);
            e.printStackTrace();
        }
    }
}