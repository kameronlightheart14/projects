package response;

import java.util.Objects;

/**
 * Basic response class handles responses that just need to relay back a message
 *
 * @author Kameron Lightheart
 *
 * 2/15/19
 */
public class BasicResponse extends requests.JsonPacket {
    private String message;

    public BasicResponse(String message) {
        this.message = message;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof BasicResponse)) return false;
        BasicResponse that = (BasicResponse) o;
        return Objects.equals(message, that.message);
    }

    @Override
    public int hashCode() {

        return Objects.hash(message);
    }
}
