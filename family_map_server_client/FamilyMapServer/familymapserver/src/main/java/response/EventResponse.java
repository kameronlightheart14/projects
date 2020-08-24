package response;

import model.Event;

/**
 * EventResponse is a class that communicates back to the client with the appropriate response
 *
 * @author Kameron Lightheart
 *
 * 2/13/19
 */
public class EventResponse extends requests.JsonPacket {
    private String descendant; // Unique id for the event
    private String eventID; //  to which this person belongs
    private String personID; // ID of person to which this event belongs
    private double latitude; // Latitude of event’s location
    private double longitude; // Longitude of event’s location
    private String country; // Country in which event occurred
    private String city; // City in which event occurred
    private String eventType; // Type of event (birth, baptism, christening, marriage, death, etc.)
    private int year; // Year in which event occurred

    public EventResponse(String descendant, String eventID, String personID, double latitude, double longitude, String country, String city, String eventType, int year) {
        this.descendant = descendant;
        this.eventID = eventID;
        this.personID = personID;
        this.latitude = latitude;
        this.longitude = longitude;
        this.country = country;
        this.city = city;
        this.eventType = eventType;
        this.year = year;
    }

    public Event generateEvent() {
        return new Event(eventID, descendant, personID, latitude, longitude, country, city, eventType, year);
    }

    public String getDescendant() {
        return descendant;
    }

    public void setDescendant(String descendant) {
        this.descendant = descendant;
    }

    public String getEventID() {
        return eventID;
    }

    public void setEventID(String eventID) {
        this.eventID = eventID;
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
}
