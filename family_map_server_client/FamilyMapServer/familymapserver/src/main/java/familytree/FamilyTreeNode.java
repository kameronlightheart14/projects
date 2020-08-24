package familytree;

import java.sql.Connection;
import java.util.ArrayList;
import java.util.Objects;

import dao.DataAccessException;
import dao.Database;
import dao.EventDao;
import dao.PersonDao;
import model.Event;
import model.Person;

/**
 * FamilyTreeNode
 *
 * @author Kameron Lightheart
 *
 * 2/22/19
 *
 */
public class FamilyTreeNode {
    private Person person;
    private FamilyTreeNode fatherNode;
    private FamilyTreeNode motherNode;
    private FamilyTreeNode spouseNode;
    private ArrayList<Event> events;
    private int birthYear;

    public FamilyTreeNode(Person person) {
        this.person = person;
        this.fatherNode = null;
        this.motherNode = null;
        this.spouseNode = null;
        events = new ArrayList<>();
    }

    public int getBirthYear() {
        return birthYear;
    }

    public void setBirthYear(int birthYear) {
        this.birthYear = birthYear;
    }

    /**
     * add the Node's person and events to the database
     */
    public void addToDatabase(Connection conn) throws DataAccessException {
        PersonDao personDao = new PersonDao(conn);
        EventDao eventDao = new EventDao(conn);
        personDao.insert(person);
        for (Event event : events) {
            eventDao.insert(event);
        }
    }

    public FamilyTreeNode getFatherNode() {
        return fatherNode;
    }

    public void setFatherNode(FamilyTreeNode fatherNode) {
        this.fatherNode = fatherNode;
    }

    public FamilyTreeNode getMotherNode() {
        return motherNode;
    }

    public void setMotherNode(FamilyTreeNode motherNode) {
        this.motherNode = motherNode;
    }

    public FamilyTreeNode getSpouseNode() {
        return spouseNode;
    }

    public void setSpouseNode(FamilyTreeNode spouseNode) {
        this.spouseNode = spouseNode;
    }

    public String getFatherID() {
        return person.getFatherID();
    }
    public String getMotherID() {
        return person.getMotherID();
    }
    public String getSpouseID() {
        return person.getSpouseID();
    }

    public void addEvent(Event event) {
        this.events.add(event);
    }

    public Person getPerson() {
        return person;
    }

    public void setPerson(Person person) {
        this.person = person;
    }

    public ArrayList<Event> getEvents() {
        return events;
    }

    public void setEvents(ArrayList<Event> events) {
        this.events = events;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof FamilyTreeNode)) return false;
        FamilyTreeNode that = (FamilyTreeNode) o;
        return getBirthYear() == that.getBirthYear() &&
                Objects.equals(getPerson(), that.getPerson()) &&
                Objects.equals(getFatherNode(), that.getFatherNode()) &&
                Objects.equals(getMotherNode(), that.getMotherNode()) &&
                Objects.equals(getSpouseNode(), that.getSpouseNode()) &&
                Objects.equals(getEvents(), that.getEvents());
    }

    @Override
    public int hashCode() {

        return Objects.hash(getPerson(), getFatherNode(), getMotherNode(), getSpouseNode(), getEvents(), getBirthYear());
    }
}
