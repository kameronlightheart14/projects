package model;

import java.util.Objects;

/**
 * User data object. Contains credentials information like userName, passowrd, etc.
 *
 * @author Kameron Lightheart
 */
public class User extends Model {
    private String userName; // Unique userName
    private String password; // User's password (non-empty string)
    private String email; // User's email address (non-empty string)
    private String firstName; // User's first name (non-empty string)
    private String lastName; // User's last name (non-empty string)
    private String gender; // User's gender (string: "f" or "m")
    private String personID; // Unique Person ID assigned to this user's generated Person object
    // (non-empty string)

    public User(String userName, String password, String email, String firstName, String lastName,
                String gender, String personID) {
        this.userName = userName;
        this.password = password;
        this.email = email;
        this.firstName = firstName;
        this.lastName = lastName;
        this.gender = gender;
        this.personID = personID;
    }

    public Person generatePerson() {
        return new Person(personID, userName, firstName, lastName,
                gender, "", "", "");
    }

    public String getUsername() {
        return userName;
    }

    public void setUsername(String userName) {
        this.userName = userName;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
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

    public String getPersonID() {
        return personID;
    }

    public void setPersonID(String personID) {
        this.personID = personID;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof User)) return false;
        User user = (User) o;
        return Objects.equals(getUsername(), user.getUsername()) &&
                Objects.equals(getPassword(), user.getPassword()) &&
                Objects.equals(getEmail(), user.getEmail()) &&
                Objects.equals(getFirstName(), user.getFirstName()) &&
                Objects.equals(getLastName(), user.getLastName()) &&
                Objects.equals(getGender(), user.getGender()) &&
                Objects.equals(getPersonID(), user.getPersonID());
    }

    @Override
    public int hashCode() {

        return Objects.hash(getUsername(), getPassword(), getEmail(), getFirstName(), getLastName(), getGender(), getPersonID());
    }
}
