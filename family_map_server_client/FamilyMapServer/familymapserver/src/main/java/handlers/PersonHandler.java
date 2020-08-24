package handlers;

import java.io.*;
import java.net.*;
import java.sql.Connection;

import com.sun.net.httpserver.*;

import javax.xml.crypto.Data;

import dao.AuthTokenDao;
import dao.DataAccessException;
import dao.Database;
import dao.PersonDao;
import model.Person;
import model.User;
import response.BasicResponse;
import response.PersonResponse;
import response.PersonResponseMultiple;
import services.PersonService;

/**
 * Handler object that handles Person requests
 *
 * @author Kameron Lightheart
 *
 * 2/13/19
 */
public class PersonHandler implements HttpHandler {
    // Handles HTTP requests containing the "/user/register" URL path.
    // In this context, an "exchange" is an HTTP request/response pair
    // (i.e., the client and server exchange a request and response).
    // The HttpExchange object gives the handler access to all of the
    // details of the HTTP request (Request type [GET or POST],
    // request headers, request body, etc.).
    // The HttpExchange object also gives the handler the ability
    // to construct an HTTP response and send it back to the client
    // (Status code, headers, response body, etc.).
    @Override
    public void handle(HttpExchange exchange) throws IOException {

        boolean success = false;

        try {
            // Only allow post register requests
            if (exchange.getRequestMethod().toLowerCase().equals("get")) {

                // Get the HTTP request headers
                Headers httpHeaders = exchange.getRequestHeaders();
                String authToken = httpHeaders.getFirst("Authorization");

                // Get the user associated to auth token
                User user = AuthTokenDao.authenticate(authToken);

                //Get the HTTP URIs
                String uriStr = exchange.getRequestURI().getPath();

                // Split string to find header pieces of username and (optional) gen #
                String splitHeaders[] = uriStr.split("/");
                if (splitHeaders.length == 3) {
                    String personID = splitHeaders[splitHeaders.length - 1];
                    if (!belongsToUser(user, personID)) {
                        throw new DataAccessException("Person does not belong to user signed in");
                    }
                    // Run the register request
                    PersonResponse personResponse = PersonService.getPerson(personID);
                    // Send OK http response
                    exchange.sendResponseHeaders(HttpURLConnection.HTTP_OK, 0);
                    // Send response (login response)
                    OutputStream responseBody = exchange.getResponseBody();
                    String responseJson = personResponse.serialize();
                    Handler.writeString(responseJson, responseBody);
                    responseBody.close();
                }
                else if (splitHeaders.length != 2) {
                    throw new IOException("Invalid web headers");
                }
                else {
                    // Run the register request
                    PersonResponseMultiple personResponseMult =
                            PersonService.getPersonMultiple(user.getUsername());
                    // Send OK http response
                    exchange.sendResponseHeaders(HttpURLConnection.HTTP_OK, 0);
                    // Send response (login response)
                    OutputStream responseBody = exchange.getResponseBody();
                    String responseJson = personResponseMult.serialize();
                    Handler.writeString(responseJson, responseBody);
                    responseBody.close();
                }

                success = true;

            }
            if (!success) {
                // The HTTP request was invalid somehow, so we return a "bad request"
                // status code to the client.
                exchange.sendResponseHeaders(HttpURLConnection.HTTP_BAD_REQUEST, 0);
                // We are not sending a response body, so close the response body
                // output stream, indicating that the response is complete.
                exchange.getResponseBody().close();
            }
        } catch (Exception e) {
            // send BAD REQUEST http response key
            e.printStackTrace();
            exchange.sendResponseHeaders(HttpURLConnection.HTTP_BAD_REQUEST, 0);

            // send json error response
            BasicResponse errorResponse = new BasicResponse(e.getMessage());
            String errorJson = errorResponse.serialize();
            OutputStream responseBody = exchange.getResponseBody();
            Handler.writeString(errorJson, responseBody);

            // close http transaction
            responseBody.close();
        }
    }

    private boolean belongsToUser(User user, String personID) throws DataAccessException {
        Database db = new Database();
        try {
            Connection conn = db.openConnection();
            PersonDao personDao = new PersonDao(conn);
            Person foundPerson = personDao.find(personID);
            if (foundPerson == null) {
                throw new DataAccessException("Person ID not found");
            }
            db.closeConnection(true);
            System.out.println(foundPerson.getDescendant() + " != " + user.getUsername());
            if (!foundPerson.getDescendant().equals(user.getUsername())) {
                return false;
            }
        } catch(DataAccessException e) {
            db.closeConnection(false);
            throw e;
        }
        return true;
    }
}
