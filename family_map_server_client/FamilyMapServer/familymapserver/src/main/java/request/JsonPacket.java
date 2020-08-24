package requests;

import com.google.gson.Gson;

import java.lang.reflect.Type;

/**
 * Created by eric on 2/16/19.
 */

public abstract class JsonPacket {

    /**
     * @return JSON format String with serialized information about the response
     */
    public String serialize() {
        Gson gson = new Gson();

        // build JSON string
        String jsonString = gson.toJson(this);
        return jsonString;
    }

    public static JsonPacket deserialize(String jsonPacket, Type type) {
        // deserialize json
        Gson gson = new Gson();
        JsonPacket request = gson.fromJson(jsonPacket, type);

        return request;
    }
}
