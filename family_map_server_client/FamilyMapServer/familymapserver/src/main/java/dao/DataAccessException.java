package dao;

/**
 * DataAccessException object which inherits from Exception and is thrown when there
 * are issues with trying to access data from the Database
 *
 * @author  Kameron Lightheart
 */

public class DataAccessException extends Exception {
    public DataAccessException(String message)
    {
        super(message);
    }
}
