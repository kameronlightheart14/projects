package dao;

import java.sql.Connection;

import model.Model;

/**
 * Parent class of Dao classes who work with the DataBase to add and find information
 *
 * @author Kameron Lightheart
 *
 * 2/13/19
 */
public abstract class Dao {
    protected Connection conn;
    protected Database db;

    public Dao(Connection conn) {
        this.conn = conn;
    }

    /**
     * insert() takes a Model type and inserts the data into a sql table in the database
     * @param ID
     * @return boolean
     * @throws DataAccessException
     */
    public abstract Model find(String ID) throws DataAccessException;
}
