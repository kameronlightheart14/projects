package handlers;

import java.io.*;
import java.net.*;
import java.nio.file.*;
import com.sun.net.httpserver.*;

public class DefaultHandler extends Handler {
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
    public void handle(HttpExchange exchange) {

        try {

            // gets everything past the ip.address:port including '/...'
            String uri = exchange.getRequestURI().toString();

            Path filePath = null;

            // handle default request
            if (uri.equals("/")) {
                String filePathStr = "web/index.html";
                String path = Paths.get("").toAbsolutePath().toString() + filePathStr;
                filePath = FileSystems.getDefault().getPath(filePathStr);
            } else {
                // attempt to find the requested file
                filePath = FileSystems.getDefault().getPath("web" + uri);

                // check to see if the file exists:
                String path = filePath.toString();
                System.out.println(path);
                File file = new File(path);

                System.out.println("File " + path + " exists: " + file.exists());

                if (!file.exists()) {
                    String page404 = "web/HTML/404.html";
                    filePath = FileSystems.getDefault().getPath(page404);
                }

            }

            // send response header
            exchange.sendResponseHeaders(HttpURLConnection.HTTP_ACCEPTED, 0);
            OutputStream httpResponseBody = exchange.getResponseBody();
            Files.copy(filePath, httpResponseBody);
            httpResponseBody.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
