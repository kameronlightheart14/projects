package dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;

import model.Event;

/**
 *  EventDao Object that inserts and finds Event data stored in the database
 *
 * @author Kameron Lightheart
 */
public class EventDao extends Dao {

    public EventDao(Connection conn) {
        super(conn);
    }

    /**
     * insert() takes and Event and inserts the data into a sql table in the database
     * @param event
     * @return boolean
     * @throws DataAccessException
     */
    public boolean insert(Event event) throws DataAccessException {
        boolean commit = true;
        //We can structure our string to be similar to a sql command, but if we insert question
        //marks we can change them later with help from the statement
        String sql = "INSERT INTO events (event_id, descendant, person_id, latitude, longitude, " +
                "country, city, event_type, year) VALUES(?,?,?,?,?,?,?,?,?)";
        try (PreparedStatement stmt = conn.prepareStatement(sql)) {
            //Using the statements built-in set(type) functions we can pick the question mark we want
            //to fill in and give it a proper value. The first argument corresponds to the first
            //question mark found in our sql String
            stmt.setString(1, event.getEventID());
            stmt.setString(2, event.getDescendant());
            stmt.setString(3, event.getPersonID());
            stmt.setDouble(4, event.getLatitude());
            stmt.setDouble(5, event.getLongitude());
            stmt.setString(6, event.getCountry());
            stmt.setString(7, event.getCity());
            stmt.setString(8, event.getEventType());
            stmt.setInt(9, event.getYear());

            stmt.executeUpdate();
        } catch (SQLException e) {
            throw new DataAccessException(e.getMessage());
        }

        return commit;
    }

    /**
     * find() will see if an event with the given ID exists and if so return the event object
     * @param eventID
     * @return Event
     * @throws DataAccessException
     */
    @Override
    public Event find(String eventID) throws DataAccessException {
        Event event = null;
        ResultSet rs = null;
        String sql = "SELECT * FROM events WHERE event_id = ?;";
        try (PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, eventID);
            rs = stmt.executeQuery();
            if (rs.next() == true) {
                event = new Event(rs.getString("event_id"), rs.getString("descendant"),
                        rs.getString("person_id"), rs.getFloat("latitude"), rs.getFloat("longitude"),
                        rs.getString("country"), rs.getString("city"), rs.getString("event_type"),
                        rs.getInt("year"));
                rs.close();
                return event;
            }
            rs.close();
        } catch (SQLException e) {
            throw new DataAccessException(e.getMessage());
        }
        return null;
    }

    /**
     *  findMany takes in an arrayList of Events to find, tries to find them and returns a list
     *  if successfull or null if unsuccesfull
     *
     * @return SQL ResultSet
     */
    public ArrayList<Event> findMany(String descendant) throws DataAccessException {
        ArrayList<Event> events = new ArrayList<>();
        Event event = null;
        ResultSet rs = null;
        String sql = "SELECT * FROM events WHERE descendant = ?;";
        try (PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, descendant);
            rs = stmt.executeQuery();
            while (rs.next() == true) {
                event = new Event(rs.getString("event_id"), rs.getString("descendant"),
                        rs.getString("person_id"), rs.getFloat("latitude"), rs.getFloat("longitude"),
                        rs.getString("country"), rs.getString("city"), rs.getString("event_type"),
                        rs.getInt("year"));
                events.add(event);
            }
            rs.close();
        } catch (SQLException e) {
            throw new DataAccessException(e.getMessage());
        }
        return events;
    }

    public void insertMany(ArrayList<Event> eventsToInsert) throws DataAccessException {
        for (Event event : eventsToInsert) {
            insert(event);
        }
    }
}
