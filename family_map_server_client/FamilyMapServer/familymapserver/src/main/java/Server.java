import java.io.*;
import java.net.*;
import com.sun.net.httpserver.*;

import dao.DataAccessException;
import dao.Database;
import dao.ResourcePack;
import handlers.ClearHandler;
import handlers.DefaultHandler;
import handlers.EventHandler;
import handlers.FillHandler;
import handlers.LoadHandler;
import handlers.LoginHandler;
import handlers.PersonHandler;
import handlers.RegisterHandler;

/*
	This example demonstrates the basic structure of the Family Map Server
	(although it is for a fictitious "Ticket to Ride" game, not Family Map).
	The example is greatly simplified to help you more easily understand the
	basic elements of the server.

	The Server class is the "main" class for the server (i.e., it contains the
		"main" method for the server program).
	When the server runs, all command-line arguments are passed in to Server.main.
	For this server, the only command-line argument is the port number on which
		the server should accept incoming client connections.
*/
public class Server {

    // The maximum number of waiting incoming connections to queue.
    private static final int MAX_WAITING_CONNECTIONS = 12;

    // Java provides an HttpServer class
    // The "server" field contains the HttpServer instance for this program,
    // which is initialized in the "run" method below.
    private HttpServer server;

    // This method initializes and runs the server.
    // The "portNumber" parameter specifies the port number on which the
    // server should accept incoming client connections.
    private void run(String portNumber) {

        // Since the server has no "user interface", it should display "log"
        // messages containing information about its internal activities.
        // This allows a system administrator (or you) to know what is happening
        // inside the server, which can be useful for diagnosing problems
        // that may occur.
        System.out.println("Initializing HTTP Server");

        try {
            // Create a new HttpServer object.
            // Rather than calling "new" directly, we instead create
            // the object by calling the HttpServer.create static factory method.
            // Just like "new", this method returns a reference to the new object.
            server = HttpServer.create(
                    new InetSocketAddress(Integer.parseInt(portNumber)),
                    MAX_WAITING_CONNECTIONS);
        }
        catch (IOException e) {
            e.printStackTrace();
            return;
        }

        // Indicate that we are using the default "executor".
        // This line is necessary, but its function is unimportant for our purposes.
        server.setExecutor(null);

        // Log message indicating that the server is creating and installing
        // its HTTP handlers.
        // The HttpServer class listens for incoming HTTP requests.  When one
        // is received, it looks at the URL path inside the HTTP request, and
        // forwards the request to the handler for that URL path.
        System.out.println("Creating contexts");

        // Create and install the HTTP handler for the "/user/register" URL path.
        server.createContext("/user/register", new RegisterHandler());

        // Create and install the HTTP handler for the "/user/login" URL path.
        server.createContext("/user/login", new LoginHandler());

        // Create and install the HTTP handler for the "/clear" URL path.
        server.createContext("/clear", new ClearHandler());

        // Create and install the HTTP handler for the "/fill/[userName]/{generations}" URL path.
        server.createContext("/fill", new FillHandler());

        // Create and install the HTTP handler for the "/load" URL path.
        server.createContext("/load", new LoadHandler());

        // Create and install the HTTP handler for the "/login" URL path.
        server.createContext("/login", new LoginHandler());

        // Create and install the HTTP handler for the "/person/[personID]" URL path.
        server.createContext("/person", new PersonHandler());

        // Create and install the HTTP handler for the "/event/[eventID]" URL path.
        server.createContext("/event", new EventHandler());

        server.createContext("/", new DefaultHandler());

        // Log message indicating that the HttpServer is about the start accepting
        // incoming client connections.
        System.out.println("Starting server");

        // Tells the HttpServer to start accepting incoming client connections.
        // This method call will return immediately, and the "main" method
        // for the program will also complete.
        // Even though the "main" method has completed, the program will continue
        // running because the HttpServer object we created is still running
        // in the background.
        server.start();

        // Log message indicating that the server has successfully started.
        System.out.println("Server started");
    }

    // "main" method for the server program
    // "args" should contain one command-line argument, which is the port number
    // on which the server should accept incoming client connections.
    public static void main(String[] args) {

        //Make sure database is set up
        try {
            Database db = new Database();
            db.createTables();
        } catch (DataAccessException e) {
            e.printStackTrace();
        }

        String portNumber = args[0];
        new Server().run(portNumber);

    }
}
