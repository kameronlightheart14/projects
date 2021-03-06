package handlers;

import java.io.*;
import java.net.*;
import com.sun.net.httpserver.*;

import request.LoadRequest;
import response.BasicResponse;
import services.LoadService;

/**
 * Handler object that handles Load requests
 *
 * @author Kameron Lightheart
 *
 * 2/13/19
 */
public class LoadHandler extends Handler {
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
            if (exchange.getRequestMethod().toLowerCase().equals("post")) {

                // Get request body
                InputStream reqBody = exchange.getRequestBody();
                // Read JSON string from the input stream
                String reqData = Handler.readString(reqBody);
                LoadRequest regRequest;
                regRequest = (LoadRequest) requests.JsonPacket.deserialize(reqData, LoadRequest.class);
                // Run the load request
                BasicResponse loadResponse = LoadService.load(regRequest);
                // Send OK http response
                exchange.sendResponseHeaders(HttpURLConnection.HTTP_OK, 0);
                // Send response (basic response w/ built in message)
                OutputStream responseBody = exchange.getResponseBody();
                String responseJson = loadResponse.serialize();
                Handler.writeString(responseJson, responseBody);
                responseBody.close();

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
}
