package services;

import java.sql.Connection;

import dao.DataAccessException;
import dao.Database;
import dao.EventDao;
import dao.PersonDao;
import dao.UserDao;
import request.LoadRequest;
import response.BasicResponse;

/**
 * LoadService takes in a request and takes care of it by adding new data via the dao
 *
 * @author Kameron Lightheart
 *
 * 2/13/19
 */
public class LoadService {
    /**
     * @param
     * @return LoadResponse object
     * @throws dao.DataAccessException
     */
    public static BasicResponse load(LoadRequest loadRequest) throws DataAccessException {
        ClearService.clear();
        Database db = new Database();
        try {
            Connection conn = db.openConnection();
            UserDao userDao = new UserDao(conn);
            EventDao eventDao = new EventDao(conn);
            PersonDao personDao = new PersonDao(conn);

            if (loadRequest.getUsers().size() == 0 || loadRequest.getPersons().size() == 0
                    || loadRequest.getEvents().size() == 0) {
                throw new DataAccessException("Some of the data arrays are empty");
            }

            userDao.insertMany(loadRequest.getUsers());
            eventDao.insertMany(loadRequest.getEvents());
            personDao.insertMany(loadRequest.getPersons());

            int numUsers = loadRequest.getUsers().size();
            int numEvents = loadRequest.getEvents().size();
            int numPeople = loadRequest.getPersons().size();

            db.closeConnection(true);

            return new BasicResponse("Successfully added " + numUsers + " users, " + numPeople +
                    " people, and " + numEvents + " events to the database");
        } catch (DataAccessException e) {
            db.closeConnection(false);
            throw e;
        }
    }
}
