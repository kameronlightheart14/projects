package model;

import java.util.Objects;

/**
 * AuthToken data object. Contains a unique token string and the userName to give access
 *
 * @author Kameron Lightheart
 */
public class AuthToken extends Model {
    private String userName;
    private String token;

    public AuthToken(String token, String userName) {

        this.token = token;
        this.userName = userName;
    }

    public String getToken() {
        return token;
    }

    public void setToken(String token) {
        this.token = token;
    }

    public String getUserName() {
        return userName;
    }

    public void setUserName(String userName) {
        this.userName = userName;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof AuthToken)) return false;
        AuthToken authToken = (AuthToken) o;
        return Objects.equals(getUserName(), authToken.getUserName()) &&
                Objects.equals(getToken(), authToken.getToken());
    }

    @Override
    public int hashCode() {

        return Objects.hash(getUserName(), getToken());
    }
}
