package services;

import java.sql.Connection;
import java.util.ArrayList;

import dao.DataAccessException;
import dao.Database;
import dao.EventDao;
import model.Event;
import response.EventResponse;
import response.EventResponseMultiple;

/**
 * EventService takes in a request and takes care of it by adding new data via the dao
 *
 * @author Kameron Lightheart
 *
 * 2/13/19
 */
public class EventService {
    /**
     * @param eventID, conn
     * @return EventResponse object
     * @throws dao.DataAccessException
     */
    public static EventResponse getEvent(String eventID) throws DataAccessException {
        Database db = new Database();
        Connection conn = db.openConnection();
        Event event;
        try {
            EventDao eventDao = new EventDao(conn);
            event = eventDao.find(eventID);
            db.closeConnection(true);
        } catch(DataAccessException e) {
            db.closeConnection(false);
            throw e;
        }
        if (event == null) {
            return null;
        }
        return new EventResponse(event.getDescendant(), event.getEventID(), event.getPersonID(),
                event.getLatitude(), event.getLongitude(), event.getCountry(), event.getCity(),
                event.getEventType(), event.getYear());
    }

    /**
     * Returns an array of events of all family members related to the person with given userName
     *
     * @param userName
     * @return PersonResponseMultiple
     * @throws DataAccessException
     */
    public static EventResponseMultiple getEventMultiple(String userName) throws  DataAccessException {
        Database db = new Database();
        ArrayList<Event> events;
        try {
            Connection conn = db.openConnection();
            EventDao eventDao = new EventDao(conn);
            events = eventDao.findMany(userName);
            db.closeConnection(true);
        } catch(DataAccessException e) {
            db.closeConnection(false);
            throw e;
        }
        return new EventResponseMultiple(events);
    }
}
