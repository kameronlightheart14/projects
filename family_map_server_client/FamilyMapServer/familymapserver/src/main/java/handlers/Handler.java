package handlers;

import com.sun.net.httpserver.HttpHandler;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.sql.Connection;

/**
 *
 * Generic handler.
 *
 * @author Eric Riddoch
 *
 */

public abstract class Handler implements HttpHandler {

    /** A connection to the database that the server uses. */
    protected Connection conn;

    /*
		The readString method shows how to read a String from an InputStream.
	*/
    public static String readString(InputStream is) throws IOException {
        StringBuilder sb = new StringBuilder();
        InputStreamReader sr = new InputStreamReader(is);
        char[] buf = new char[1024];
        int len;
        while ((len = sr.read(buf)) > 0) {
            sb.append(buf, 0, len);
        }
        return sb.toString();
    }
    /*
		The writeString method shows how to write a String to an OutputStream.
	*/
    public static void writeString(String str, OutputStream os) throws IOException {
        OutputStreamWriter sw = new OutputStreamWriter(os);
        sw.write(str);
        sw.flush();
    }
}
