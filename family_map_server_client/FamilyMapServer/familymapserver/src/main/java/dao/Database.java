package dao;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

/**
 * Database is a class that sets up the tables and can clear/create tables
 *
 * @author Kameron Lightheart
 *
 * 2/15/2019
 */

public class Database {
    private Connection conn;

    private static final String DATABASE_PATH = "familymapserver/src/main/resources/fms.db";

    static {
        try {
            //This is how we set up the driver for our database
            final String driver = "org.sqlite.JDBC";
            Class.forName(driver);
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }
    }

    //Whenever we want to make a change to our database we will have to open a connection and use
    //Statements created by that connection to initiate transactions
    public Connection openConnection() throws DataAccessException {
        try {
            //The Structure for this Connection is driver:language:path
            //The pathing assumes you start in the root of your project unless given a non-relative path
            final String CONNECTION_URL = "jdbc:sqlite:" + DATABASE_PATH;

            // Open a database connection to the file given in the path
            conn = DriverManager.getConnection(CONNECTION_URL);

            // Start a transaction
            conn.setAutoCommit(false);
        } catch (SQLException e) {
            e.printStackTrace();
            throw new DataAccessException("Unable to open connection to database");
        }

        return conn;
    }

    //When we are done manipulating the database it is important to close the connection. This will
    //End the transaction and allow us to either commit our changes to the database or rollback any
    //changes that were made before we encountered a potential error.

    //IMPORTANT: IF YOU FAIL TO CLOSE A CONNECTION AND TRY TO REOPEN THE DATABASE THIS WILL CAUSE THE
    //DATABASE TO LOCK. YOUR CODE MUST ALWAYS INCLUDE A CLOSURE OF THE DATABASE NO MATTER WHAT ERRORS
    //OR PROBLEMS YOU ENCOUNTER
    public void closeConnection(boolean commit) throws DataAccessException {
        try {
            if (commit) {
                //This will commit the changes to the database
                conn.commit();
            } else {
                //If we find out something went wrong, pass a false into closeConnection and this
                //will rollback any changes we made during this connection
                conn.rollback();
            }

            conn.close();
            conn = null;
        } catch (SQLException e) {
            e.printStackTrace();
            throw new DataAccessException("Unable to close database connection");
        }
    }

    public void createTables() throws DataAccessException {
        //First lets open our connection to our database.
        openConnection();

        try (Statement stmt = conn.createStatement()) {

            //We pull out a statement from the connection we just established
            //Statements are the basis for our transactions in SQL
            //Format this string to be exactly like a sql create table command
            String sqlEvents = "CREATE TABLE IF NOT EXISTS events " +
                    "(\n" +
                    "event_id    varchar(255) not null primary key, -- Unique identifier for this event (non-empty string)\n" +
                    "descendant    varchar(255) not null,              -- User to which this person belongs\n" +
                    "person_id   varchar(255) not null,               -- ID of person to which this event belongs\n" +
                    "latitude    real not null,                      -- Latitude of event’s location\n" +
                    "longitude   real not null,                      -- Longitude of event’s location\n" +
                    "country     varchar(255) not null,              -- Country in which event occurred\n" +
                    "city        varchar(255) not null,              -- City in which event occurred\n" +
                    "event_type  varchar(255) not null,              -- Type of event (birth, baptism, christening, marriage, death, etc.)\n" +
                    "year        integer not null                    -- Year in which event occurred\n" +
                    ");";
            String sqlUsers = "CREATE TABLE IF NOT EXISTS users" +
                    "(" +
                    "userName     varchar(255) not null primary key,  -- Unique user name (non-empty string)\n" +
                    "password    varchar(255) not null,                       -- password (non-empty string)\n" +
                    "email       varchar(255) not null,                       -- email address (non-empty string)\n" +
                    "first_name  varchar(255) not null,                       -- first name (non-empty string)\n" +
                    "last_name   varchar(255) not null,                       -- last name (non-empty string)\n" +
                    "gender      char(1) check (gender in (\"m\", \"f\")),    -- gender (string: \"f\" or \"m\")\n" +
                    "person_id   varchar(255) not null                        -- Unique Person ID assigned to this user’s generated Person object\n" +
                    ");";
            String sqlAuthTokens = "CREATE TABLE IF NOT EXISTS auth_tokens" +
                    "(\n" +
                    "token       varchar(255) not null primary key,             -- Unique ID number of login session\n" +
                    "user_id     varchar(255) not null                          -- id of user associated with login session\n" +
                    ");";

            String sqlPeople = "CREATE TABLE IF NOT EXISTS people" +
                    "(\n" +
                    "person_id   varchar(255) not null primary key,            -- Unique identifier for this person (non-empty string)\n" +
                    "descendant  varchar(255) not null,                        -- Descendant (Username) to which this person belongs\n" +
                    "first_name  varchar(255) not null,                        -- Person’s first name (non-empty string)\n" +
                    "last_name   varchar(255) not null,                        -- Person’s last name (non-empty string)\n" +
                    "gender      char(1) not null check (gender in (\"m\", \"f\")),-- Person’s gender (string: \"f\" or \"m\")\n" +
                    "father_id   varchar(255),                                 -- ID of person’s father (possibly null)\n" +
                    "mother_id   varchar(255),                                 -- ID of person’s mother (possibly null)\n" +
                    "spouse_id   varchar(255)                                  -- ID of person’s spouse (possibly null)\n" +
                    ");";
            stmt.executeUpdate(sqlEvents);
            stmt.execute(sqlAuthTokens);
            stmt.execute(sqlPeople);
            stmt.executeUpdate(sqlUsers);

            //if we got here without any problems we succesfully created the table and can commit
            closeConnection(true);
        } catch (SQLException e) {
            //if our table creation caused an error, we can just not commit the changes that did happen
            closeConnection(false);
            e.printStackTrace();
        } catch (DataAccessException e) {
            closeConnection(false);
            throw e;
        }
    }

    public void clearTables() throws DataAccessException
    {
        //First lets open our connection to our database.
        openConnection();

        try (Statement stmt = conn.createStatement()){
            // Execute these commands through the statement object
            stmt.executeUpdate("DELETE FROM events");
            stmt.executeUpdate("DELETE FROM users");
            stmt.executeUpdate("DELETE FROM auth_tokens");
            stmt.executeUpdate("DELETE FROM people");
            closeConnection(true);
        } catch (SQLException e) {
            e.printStackTrace();
            closeConnection(false);
        } catch(DataAccessException e) {
            closeConnection(false);
            throw e;
        }
    }
}
