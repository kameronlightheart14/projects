package model;

import java.util.Objects;

public class Person extends Model {

    private String personID; //Unique identifier for this person (non-empty string)
    private String descendant; // descendent user of person
    private String firstName; // Person’s first name (non-empty string)
    private String lastName; // Person’s last name (non-empty string)
    private String gender; // Person's gender (string: "f" or "m")
    private String father; // ID of person’s father (possibly null)
    private String mother;// ID of person’s mother (possibly null)
    private String spouse; // ID of person’s spouse (possibly null)

    public Person(String descendant, String firstName, String lastName, String gender,
                  String father, String mother, String spouse) {
        this.personID = Model.generateUUID();
        this.descendant = descendant;
        this.firstName = firstName;
        this.lastName = lastName;
        this.gender = gender;
        this.father = father;
        this.mother = mother;
        this.spouse = spouse;
    }

    public Person(String personID, String descendant, String firstName, String lastName,
                  String gender, String father, String mother, String spouse) {
        this.personID = personID;
        this.descendant = descendant;
        this.firstName = firstName;
        this.lastName = lastName;
        this.gender = gender;
        this.father = father;
        this.mother = mother;
        this.spouse = spouse;
    }

    public static Person generateUserPerson(User user) {
        return new Person(user.getUsername(), user.getFirstName(),
                user.getLastName(), user.getGender(), "", "", "");
    }

    public String getPersonID() {
        return personID;
    }

    public void setPersonID(String personID) {
        this.personID = personID;
    }

    public String getDescendant() {
        return descendant;
    }

    public void setDescendant(String descendant) {
        this.descendant = descendant;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public String getGender() {
        return gender;
    }

    public void setGender(String gender) {
        this.gender = gender;
    }

    public String getFatherID() {
        return father;
    }

    public void setFatherID(String father) {
        this.father = father;
    }

    public String getMotherID() {
        return mother;
    }

    public void setMotherID(String mother) {
        this.mother = mother;
    }

    public String getSpouseID() {
        return spouse;
    }

    public void setSpouseID(String spouse) {
        this.spouse = spouse;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Person)) return false;
        Person person = (Person) o;
        return Objects.equals(getPersonID(), person.getPersonID()) &&
                Objects.equals(getDescendant(), person.getDescendant()) &&
                Objects.equals(getFirstName(), person.getFirstName()) &&
                Objects.equals(getLastName(), person.getLastName()) &&
                Objects.equals(getGender(), person.getGender()) &&
                Objects.equals(getFatherID(), person.getFatherID()) &&
                Objects.equals(getMotherID(), person.getMotherID()) &&
                Objects.equals(getSpouseID(), person.getSpouseID());
    }

    @Override
    public int hashCode() {

        return Objects.hash(getPersonID(), getDescendant(), getFirstName(), getLastName(), getGender(), getFatherID(), getMotherID(), getSpouseID());
    }
}
