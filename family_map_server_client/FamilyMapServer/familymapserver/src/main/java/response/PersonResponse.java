package response;

import model.Person;

public class PersonResponse extends requests.JsonPacket {
    private String descendant; //Name of user account the person belongs to
    private String personID; // to which this person belongs
    private String firstName; // Person’s first name (non-empty string)
    private String lastName; // Person’s last name (non-empty string)
    private String gender; // Person's gender (string: "f" or "m")
    private String father; // ID of person’s father (possibly null)
    private String mother;// ID of person’s mother (possibly null)
    private String spouse; // ID of person’s spouse (possibly null)

    public PersonResponse(String descendant, String personID, String firstName, String lastName, String gender, String father, String mother, String spouse) {
        this.descendant = descendant;
        this.personID = personID;
        this.firstName = firstName;
        this.lastName = lastName;
        this.gender = gender;
        this.father = father;
        this.mother = mother;
        this.spouse = spouse;
    }

    public Person generatePerson() {
        return new Person(personID, descendant, firstName, lastName, gender, father, mother, spouse);
    }

    public String getDescendant() {
        return descendant;
    }

    public void setDescendant(String descendant) {
        this.descendant = descendant;
    }

    public String getPersonID() {
        return personID;
    }

    public void setPersonID(String personID) {
        this.personID = personID;
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

    public String getFather() {
        return father;
    }

    public void setFather(String father) {
        this.father = father;
    }

    public String getMother() {
        return mother;
    }

    public void setMother(String mother) {
        this.mother = mother;
    }

    public String getSpouse() {
        return spouse;
    }

    public void setSpouse(String spouse) {
        this.spouse = spouse;
    }
}
