package services;

import junit.framework.Assert;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import dao.DataAccessException;
import dao.Database;
import request.RegisterRequest;
import response.BasicResponse;

/**
 * Created by eric on 2/23/19.
 */
public class FillServiceTest {

    private BasicResponse correctResponse;
    private RegisterRequest registerRequest;
    private String userName;
    private Database db;
    private int numGenerations;

    @Before
    public void setUp() throws Exception {

        correctResponse =
                new BasicResponse("Successfully added 7 persons" +
                        " and 19 events to the database.");

        registerRequest = new RegisterRequest(
                "eriddoch",
                "P@SSW0RD!!",
                "eric.riddoch@gmail.com",
                "Eric",
                "Riddoch",
                "m"
        );

        userName = "eriddoch";
        numGenerations = 2;

        db = new Database();

        // initialize database
        db.clearTables();
        db.createTables();

    }

    @After
    public void tearDown() throws Exception {
        db.clearTables();
    }

    @Test
    public void fillPASS() throws DataAccessException {

        // register a user
        RegisterService.register(registerRequest);

        // do the fill service
        BasicResponse compareTest = null;
        compareTest = FillService.fill(userName, numGenerations);

        // check for correct response
        Assert.assertEquals(correctResponse, compareTest);

    }

    @Test(expected = DataAccessException.class)
    public void fillFAIL() throws DataAccessException {

        // register a user
        RegisterService.register(registerRequest);

        // do the fill service
        BasicResponse compareTest = null;
        compareTest = FillService.fill("FAKE_USERNAME", numGenerations);

        // check for error message instead
        Assert.assertNotSame(correctResponse, compareTest);

    }



}