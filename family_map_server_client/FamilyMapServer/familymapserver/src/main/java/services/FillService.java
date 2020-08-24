package services;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.sql.Statement;

import dao.DataAccessException;
import dao.Database;
import dao.PersonDao;
import dao.UserDao;
import familytree.FamilyTree;
import model.Person;
import model.User;
import response.BasicResponse;

/**
 * FillService takes in a request and takes care of it by adding new data via the dao
 *
 * @author Kameron Lightheart
 *
 * 2/13/19
 */
public class FillService {
    /**
     * @param generations, conn # of generations to generate
     * @return FillResponse object
     * @throws dao.DataAccessException
     */
    public static BasicResponse fill(String userName, int generations) throws DataAccessException {
        // 1. Delete every person and event connected to the user
        deleteUserPeople(userName);

        // 2. Get userName associated with userName
        User user = getUser(userName);
        if (user == null) {
            throw new DataAccessException("User not found in database");
        }

        // 3. Generate user data
        Person userPerson = Person.generateUserPerson(user);

        FamilyTree familyTree = new FamilyTree(userPerson);
        familyTree.addGenerations(generations);

        // 4. Return a success response
        int numPeopleAdded = familyTree.getNumNodes();
        int numEventsAdded = familyTree.getNumEvents();
        return new BasicResponse("Successfully added " + numPeopleAdded +  " persons and " + numEventsAdded + " events to the database.");
    }

    private static User getUser(String userName) throws DataAccessException{
        Database db = new Database();
        Connection conn = db.openConnection();
        UserDao userDao = new UserDao(conn);
        User user = userDao.find(userName);
        db.closeConnection(true);
        return user;
    }

    private static void deleteUserPeople(String userName) throws DataAccessException {
        Database db = new Database();
        Connection conn = db.openConnection();
        try {
            String prep = "DELETE FROM people WHERE descendant = ?";
            PreparedStatement stmt = conn.prepareStatement(prep);
            stmt.setString(1, userName);

            //delete all people related to person
            stmt.executeUpdate();
            stmt.close();
            String prep1 = "DELETE FROM events WHERE descendant = ?";
            PreparedStatement stmt1 = conn.prepareStatement(prep1);
            stmt1.setString(1, userName);
            stmt1.executeUpdate();
            //stmt1.close();
            db.closeConnection(true);
        } catch(SQLException e) {
            db.closeConnection(false);
            e.printStackTrace();
        }
    }
}
