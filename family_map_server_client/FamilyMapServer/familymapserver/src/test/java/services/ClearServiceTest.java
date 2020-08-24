package services;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import java.sql.Connection;

import dao.DataAccessException;
import dao.Database;
import dao.PersonDao;
import model.Person;

import static org.junit.Assert.*;

public class ClearServiceTest {
    Database db;
    Person person;
    @Before
    public void setUp()throws DataAccessException {
        db = new Database();
        db.clearTables();
        person = new Person("0", "kameronlightheart14", "Kameron",
                "Lightheart", "m", "", "", "");
    }

    @Test
    /**
     * This test makes sure we can clear and add the same person again
     */
    public void clearBeforeAdd() throws DataAccessException {
        try {
            Connection conn = db.openConnection();
            PersonDao personDao = new PersonDao(conn);
            personDao.insert(person);
            db.closeConnection(true);
            ClearService.clear();
            conn = db.openConnection();
            personDao = new PersonDao(conn);
            personDao.insert(person);
            db.closeConnection(true);
        } catch(DataAccessException e) {
            db.closeConnection(false);
            throw e;
        }
    }

    @Test
    /**
     * This test makes sure that the clear indeed deletes the data
     */
    public void clearAfterAdd()throws DataAccessException {
        Person tryFind;
        try {
            Connection conn = db.openConnection();
            PersonDao personDao = new PersonDao(conn);
            personDao.insert(person);
            db.closeConnection(true);
            ClearService.clear();
            conn = db.openConnection();
            personDao = new PersonDao(conn);
            tryFind = personDao.find(person.getPersonID());
            db.closeConnection(true);
        } catch(DataAccessException e) {
            db.closeConnection(false);
            throw e;
        }
        Assert.assertNull(tryFind);
    }
}