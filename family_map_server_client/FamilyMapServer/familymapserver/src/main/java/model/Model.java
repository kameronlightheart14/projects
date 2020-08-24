package model;

import java.util.UUID;

/**
 * Model is a parent class for specific Models like Person or User
 * It contains the ID for each of the model types
 *
 * @author Kameron Lightheart
 */
public class Model {

    public static String generateUUID() {
        return UUID.randomUUID().toString();
    }
}
