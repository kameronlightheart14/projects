package response;

/**
 *  LoginResponse is a class that communicates back to the client with the appropriate response
 *
 * @author Kameron Lightheart
 *
 * 2/13/19
 */
public class LoginResponse extends requests.JsonPacket {
    private String authToken;
    private String userName;
    private String personID;

    public LoginResponse(String authToken, String userName, String personID) {
        this.authToken = authToken;
        this.userName = userName;
        this.personID = personID;
    }

    public String getAuthToken() {
        return authToken;
    }

    public void setAuthToken(String authToken) {
        this.authToken = authToken;
    }

    public String getUserName() {
        return userName;
    }

    public void setUserName(String userName) {
        this.userName = userName;
    }

    public String getPersonID() {
        return personID;
    }

    public void setPersonID(String personID) {
        this.personID = personID;
    }
}
