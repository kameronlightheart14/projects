package request;

/**
 * Request is sent to server with needed information to login and access other pages
 *
 * @author Kameron Lightheart
 *
 * 2/13/19
 */
public class LoginRequest extends requests.JsonPacket {
    private String userName;
    private String password;

    public LoginRequest(String userName, String password) {
        this.userName = userName;
        this.password = password;
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
}
