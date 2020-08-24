package request;

import model.AuthToken;
import model.User;

/**
 * Request is sent to server
 *
 * @author Kameron Lightheart
 *
 * 2/13/19
 */
public class RegisterRequest extends requests.JsonPacket {
    private String userName; // Unique userName
    private String password; // User's password (non-empty string)
    private String email; // User's email address (non-empty string)
    private String firstName; // User's first name (non-empty string)
    private String lastName; // User's last name (non-empty string)
    private String gender; // User's gender (string: "f" or "m")

    public RegisterRequest(String userName, String password, String email, String firstName, String lastName, String gender) {
        this.userName = userName;
        this.password = password;
        this.email = email;
        this.firstName = firstName;
        this.lastName = lastName;
        this.gender = gender;
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
}
