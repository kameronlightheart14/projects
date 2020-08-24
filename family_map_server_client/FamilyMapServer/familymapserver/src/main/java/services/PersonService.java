package services;

import java.sql.Connection;
import java.util.ArrayList;

import dao.DataAccessException;
import dao.Database;
import dao.PersonDao;
import model.Person;
import response.PersonResponse;
import response.PersonResponseMultiple;

/**
 * PersonService takes in a request and takes care of it by adding new data via the dao
 *
 * @author Kameron Lightheart
 *
 * 2/13/19
 */
public class PersonService {
    /**
     * @param personID
     * @return EventResponse object
     * @throws dao.DataAccessException
     */
    public static PersonResponse getPerson(String personID) throws DataAccessException {
        Database db = new Database();
        Connection conn = db.openConnection();
        Person person;
        try {
            PersonDao personDao = new PersonDao(conn);
            person = personDao.find(personID);
            db.closeConnection(true);
        } catch(DataAccessException e) {
            db.closeConnection(false);
            throw e;
        }
        if (person == null) {
            return null;
        }
        return new PersonResponse(person.getDescendant(), person.getPersonID(), person.getFirstName(),
                person.getLastName(), person.getGender(), person.getFatherID(), person.getMotherID(),
                person.getSpouseID());
    }

    /**
     * Returns an array of events of all family members related to the person with given userName
     *
     * @param userName
     * @return PersonResponseMultiple
     * @throws DataAccessException
     */
    public static PersonResponseMultiple getPersonMultiple(String userName) throws  DataAccessException {
        Database db = new Database();
        Connection conn = db.openConnection();
        ArrayList<Person> people;
        try {
            PersonDao personDao = new PersonDao(conn);
            people = personDao.findMany(userName);
            db.closeConnection(true);
        } catch(DataAccessException e) {
            db.closeConnection(false);
            throw e;
        }
        return new PersonResponseMultiple(people);
    }
}
