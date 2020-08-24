package familytree;

import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import java.sql.Connection;
import java.util.ArrayList;

import dao.DataAccessException;
import dao.Database;
import dao.PersonDao;
import model.Model;
import model.Person;
import model.User;

import static org.junit.Assert.*;

public class FamilyTreeTest {
    private Database db;
    User user;
    Person person;

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
    }

    @After
    public void tearDown() throws DataAccessException {
        db.clearTables();
    }

    @Test
    public void addSpousePairPass() {

    }

    @Test
    public void addGenerationsPass() {
        FamilyTree tree = new FamilyTree(person);
        try {
            tree.addGenerations(4);
            Assert.assertEquals(31, tree.getNumNodes());
        } catch(DataAccessException e) {
            e.printStackTrace();
        }
    }

    @Test
    public void addSpousalPairPASS() throws DataAccessException {

        // create a node to test
        FamilyTreeNode node = new FamilyTreeNode(person);

        // create a family tree ONLY so we can call the function
        FamilyTree tree = new FamilyTree(person);
        try {
            Connection conn = db.openConnection();
            ArrayList<FamilyTreeNode> toAdd = new ArrayList<>();
            tree.addSpousePair(node, toAdd);
            PersonDao pDao = new PersonDao(conn);
            for (FamilyTreeNode node1 : toAdd) {
                pDao.insert(node1.getPerson());
            }

            // check that father and mother exist
            FamilyTreeNode father = node.getFatherNode();
            FamilyTreeNode mother = node.getMotherNode();
            Assert.assertNotNull(father);
            Assert.assertNotNull(mother);

            // check that spouse id's are correct
            Assert.assertEquals(father.getSpouseID(), mother.getPerson().getPersonID());
            Assert.assertEquals(mother.getSpouseID(), father.getPerson().getPersonID());

            // check that the parent id's are correct
            Assert.assertEquals(node.getFatherID(), father.getPerson().getPersonID());
            Assert.assertEquals(node.getMotherID(), mother.getPerson().getPersonID());

            // check that all three are in the database
            Person foundMother = pDao.find(mother.getPerson().getPersonID());
            Person foundFather = pDao.find(father.getPerson().getPersonID());
            Assert.assertNotNull(foundFather);
            Assert.assertNotNull(foundMother);

            // check that they match the inserted people
            Assert.assertEquals(mother.getPerson(), foundMother);
            Assert.assertEquals(father.getPerson(), foundFather);
            db.closeConnection(true);
        } catch(DataAccessException e) {
            db.closeConnection(false);
            throw e;
        }

    }
}