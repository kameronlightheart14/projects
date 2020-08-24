package handlers;

import java.io.*;
import java.net.*;

import com.sun.net.httpserver.*;

import request.RegisterRequest;
import response.BasicResponse;
import response.LoginResponse;
import services.RegisterService;

/**
 * Handler object that handles Register requests
 *
 * @author Kameron Lightheart
 *
 * 2/13/19
 */
public class RegisterHandler extends Handler {

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
                    RegisterRequest regRequest;
                    regRequest = (RegisterRequest) requests.JsonPacket.deserialize(reqData, RegisterRequest.class);
                    // Run the register request
                    LoginResponse registerResponse = RegisterService.register(regRequest);
                    // Send OK http response
                    exchange.sendResponseHeaders(HttpURLConnection.HTTP_OK, 0);
                    // Send response (login response)
                    OutputStream responseBody = exchange.getResponseBody();
                    System.out.println(registerResponse.serialize());
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
                exchange.sendResponseHeaders(HttpURLConnection.HTTP_BAD_REQUEST, 0);

                // send json error response
                BasicResponse errorResponse;
                if (e.getMessage().equals("[SQLITE_CONSTRAINT]  Abort due to constraint "
                        + "violation (column userName is not unique)")) {
                    errorResponse = new BasicResponse("Username already taken");
                }
                else {
                    errorResponse = new BasicResponse(e.getMessage());
                }
                String errorJson = errorResponse.serialize();
                OutputStream responseBody = exchange.getResponseBody();
                Handler.writeString(errorJson, responseBody);

                // close http transaction
                responseBody.close();
            }
        }
}
