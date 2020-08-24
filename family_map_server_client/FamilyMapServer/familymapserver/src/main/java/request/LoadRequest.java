package request;

import java.util.ArrayList;

import model.Event;
import model.Person;
import model.User;

/**
 * Request is sent to server with needed information to load needed info
 *
 * @author Kameron Lightheart
 *
 * 2/13/19
 */
public class LoadRequest extends requests.JsonPacket {
    private ArrayList<User> users;
    private ArrayList<Person> persons;
    private ArrayList<Event> events;

    public LoadRequest(ArrayList<User> users, ArrayList<Person> persons, ArrayList<Event> events) {
        this.users = users;
        this.persons = persons;
        this.events = events;
    }

    public ArrayList<User> getUsers() {
        return users;
    }

    public void setUsers(ArrayList<User> users) {
        this.users = users;
    }

    public ArrayList<Person> getPersons() {
        return persons;
    }

    public void setPersons(ArrayList<Person> persons) {
        this.persons = persons;
    }

    public ArrayList<Event> getEvents() {
        return events;
    }

    public void setEvents(ArrayList<Event> events) {
        this.events = events;
    }
}
