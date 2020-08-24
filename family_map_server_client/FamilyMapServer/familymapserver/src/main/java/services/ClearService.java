package services;

import java.sql.Connection;

import dao.DataAccessException;
import dao.Database;
import response.BasicResponse;

/**
 * ClearService clears the data and returns a response message
 *
 * @author Kameron Lightheart
 *
 * 2/13/19
 */
public class ClearService {
    /**
     * @return ClearResponse object
     * @throws dao.DataAccessException
     */
    public static BasicResponse clear() throws DataAccessException {
        try {
            Database db = new Database();
            db.clearTables();
        } catch (DataAccessException e) {
            return new BasicResponse(e.getMessage());
        }
        return new BasicResponse("Clear succeeded");
    }
}
