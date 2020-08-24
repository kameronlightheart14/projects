package handlers;

import java.io.*;
import java.net.*;
import com.sun.net.httpserver.*;

import response.BasicResponse;
import services.FillService;

/**
 * Handler object that handles Fill requests
 *
 * @author Kameron Lightheart
 *
 * 2/13/19
 */
public class FillHandler implements HttpHandler {
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

                // Get the HTTP request headers
                String headersStr = exchange.getRequestURI().getPath();
                // Split string to find header pieces of username and (optional) gen #
                String splitHeaders[] = headersStr.split("/");
                int generations = 4;
                String userName;
                if (splitHeaders.length == 4) {
                    userName = splitHeaders[splitHeaders.length - 2];
                    String gens = splitHeaders[splitHeaders.length - 1];
                    generations = Integer.parseInt(gens);
                }
                else if (splitHeaders.length == 3) {
                    userName = splitHeaders[splitHeaders.length - 1];
                }
                else {
                    throw new IOException("Invalid web headers");
                }


                // Run the register request
                BasicResponse registerResponse = FillService.fill(userName, generations);
                // Send OK http response
                exchange.sendResponseHeaders(HttpURLConnection.HTTP_OK, 0);
                // Send response (login response)
                OutputStream responseBody = exchange.getResponseBody();
                String responseJson = registerResponse.serialize();
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
