package model;

import java.util.Objects;

import dao.ResourcePack;

/**
 * Event data object. Contains details of an event labeled by an ID
 *
 * @author Kameron Lightheart
 */
public class Event extends Model {
    private String eventID; // Unique id for the event
    private String descendant; //  to which this person belongs
    private String personID; // ID of person to which this event belongs
    private double latitude; // Latitude of event’s location
    private double longitude; // Longitude of event’s location
    private String country; // Country in which event occurred
    private String city; // City in which event occurred
    private String eventType; // Type of event (birth, baptism, christening, marriage, death, etc.)
    private int year; // Year in which event occurred

    public Event(String userName, String personID, double latitude, double longitude,
                 String country, String city, String eventType, int year) {
        this.eventID = Model.generateUUID();
        this.descendant = userName;
        this.personID = personID;
        this.latitude = latitude;
        this.longitude = longitude;
        this.country = country;
        this.city = city;
        this.eventType = eventType;
        this.year = year;
    }

    public Event(String eventID, String userName, String personID, double latitude,
                 double longitude, String country, String city, String eventType, int year) {
        this.eventID = eventID;
        this.descendant = userName;
        this.personID = personID;
        this.latitude = latitude;
        this.longitude = longitude;
        this.country = country;
        this.city = city;
        this.eventType = eventType;
        this.year = year;
    }

    public static Event generateBirthEvent(int year, Person person) {
        Location birthPlace = ResourcePack.getRandomLocation();
        return new Event(person.getDescendant(), person.getPersonID(), birthPlace.getLatitude(),
                birthPlace.getLongitude(), birthPlace.getCountry(), birthPlace.getCity(),
                "Birth", year);
    }

    public static Event generateDeathEvent(int year, Person person) {
        Location deathPlace = ResourcePack.getRandomLocation();
        return new Event(person.getDescendant(), person.getPersonID(), deathPlace.getLatitude(),
                deathPlace.getLongitude(), deathPlace.getCountry(), deathPlace.getCity(),
                "Death", year);
    }

    public static Event generateMarriageEvent(int year, Person person) {
        Location weddingPlace = ResourcePack.getRandomLocation();
        return new Event(person.getDescendant(), person.getPersonID(), weddingPlace.getLatitude(),
                weddingPlace.getLongitude(), weddingPlace.getCountry(), weddingPlace.getCity(),
                "Marriage", year);
    }

    public String getEventID() {
        return eventID;
    }

    public void setEventID(String eventID) {
        this.eventID = eventID;
    }

    public String getDescendant() {
        return descendant;
    }

    public void setDescendant(String userName) {
        this.descendant = userName;
    }

    public String getPersonID() {
        return personID;
    }

    public void setPersonID(String personID) {
        this.personID = personID;
    }

    public double getLatitude() {
        return latitude;
    }

    public void setLatitude(double latitude) {
        this.latitude = latitude;
    }

    public double getLongitude() {
        return longitude;
    }

    public void setLongitude(double longitude) {
        this.longitude = longitude;
    }

    public String getCountry() {
        return country;
    }

    public void setCountry(String country) {
        this.country = country;
    }

    public String getCity() {
        return city;
    }

    public void setCity(String city) {
        this.city = city;
    }

    public String getEventType() {
        return eventType;
    }

    public void setEventType(String eventType) {
        this.eventType = eventType;
    }

    public int getYear() {
        return year;
    }

    public void setYear(int year) {
        this.year = year;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Event)) return false;
        Event event = (Event) o;
        return getYear() == event.getYear() &&
                Objects.equals(getEventID(), event.getEventID()) &&
                Objects.equals(getDescendant(), event.getDescendant()) &&
                Objects.equals(getPersonID(), event.getPersonID()) &&
                Objects.equals(getCountry(), event.getCountry()) &&
                Objects.equals(getCity(), event.getCity()) &&
                Objects.equals(getEventType(), event.getEventType());
    }

    @Override
    public int hashCode() {

        return Objects.hash(getEventID(), getDescendant(), getPersonID(), getLatitude(), getLongitude(), getCountry(), getCity(), getEventType(), getYear());
    }
}
