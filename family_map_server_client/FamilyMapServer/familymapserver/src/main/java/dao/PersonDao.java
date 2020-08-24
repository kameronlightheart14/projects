package dao;


import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;

import model.Person;

/**
 *  PersonDao Object that inserts and finds Person data stored in the database
 *
 * @author Kameron Lightheart
 */
public class PersonDao extends Dao {

    public PersonDao(Connection conn) {
        super(conn);
    }

    /**
     * insert() takes and Event and inserts the data into a sql table in the database
     * @param person
     * @return boolean
     * @throws DataAccessException
     */
    public boolean insert(Person person) throws DataAccessException {
        boolean commit = true;
        //We can structure our string to be similar to a sql command, but if we insert question
        //marks we can change them later with help from the statement
        String sql = "INSERT INTO people (person_id, descendant, first_name, last_name, " +
                "gender, father_id, mother_id, spouse_id) VALUES(?,?,?,?,?,?,?,?)";
        try (PreparedStatement stmt = conn.prepareStatement(sql)) {
            //Using the statements built-in set(type) functions we can pick the question mark we want
            //to fill in and give it a proper value. The first argument corresponds to the first
            //question mark found in our sql String
            stmt.setString(1, person.getPersonID());
            stmt.setString(2, person.getDescendant());
            stmt.setString(3, person.getFirstName());
            stmt.setString(4, person.getLastName());
            stmt.setString(5, person.getGender());
            stmt.setString(6, person.getFatherID());
            stmt.setString(7, person.getMotherID());
            stmt.setString(8, person.getSpouseID());

            stmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
            throw new DataAccessException(e.getMessage());
        }

        return commit;
    }

    /**
     * find() will see if an event with the given ID exists and if so return the person object
     * @param personID
     * @return Event
     * @throws DataAccessException
     */
    @Override
    public Person find(String personID) throws DataAccessException {
        Person person = null;
        ResultSet rs = null;
        String sql = "SELECT * FROM people WHERE person_id = ?;";
        try (PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, personID);
            rs = stmt.executeQuery();
            if (rs.next() == true) {
                person = new Person(rs.getString("person_id"), rs.getString("descendant"),
                        rs.getString("first_name"), rs.getString("last_name"), rs.getString("gender"),
                        rs.getString("father_id"), rs.getString("mother_id"), rs.getString("spouse_id"));

                rs.close();

                return person;
            }
            rs.close();

        } catch (SQLException e) {
            throw new DataAccessException(e.getMessage());
        }
        return null;
    }

    /**
     *  findMany takes in an arrayList of people to find, tries to find them and returns a list
     *  if successfull or null if unsuccesfull
     *
     * @param userName
     *
     * @return SQL ResultSet
     */
    public ArrayList<Person> findMany(String userName) throws DataAccessException {
        ArrayList<Person> people = new ArrayList<>();
        Person person = null;
        ResultSet rs = null;
        String sql = "SELECT * FROM people WHERE descendant = ?;";
        try (PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, userName);
            rs = stmt.executeQuery();
            while (rs.next()) {
                person = new Person(rs.getString("person_id"), rs.getString("descendant"),
                        rs.getString("first_name"), rs.getString("last_name"), rs.getString("gender"),
                        rs.getString("father_id"), rs.getString("mother_id"), rs.getString("spouse_id"));
                people.add(person);
            }
            rs.close();
        } catch (SQLException e) {
            throw new DataAccessException(e.getMessage());
        }
        return people;
    }

    /**
     * Insert multiple users at once
     *
     * @param usersToInsert
     */
    public void insertMany(ArrayList<Person> usersToInsert) throws DataAccessException {
        for (Person person : usersToInsert) {
            insert(person);
        }
    }
}
