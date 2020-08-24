package response;

/**
 * ErrorResponse is a class that communicates back to the client with the appropriate response
 *
 * @author Kameron Lightheart
 *
 * 2/13/19
 */
public class ErrorResponse extends requests.JsonPacket {
    private String errorMessage;

    public ErrorResponse(String errorMessage) {
        this.errorMessage = errorMessage;
    }
}
