package response;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.util.ArrayList;

import model.Event;

public class EventResponseMultiple extends requests.JsonPacket {
    private ArrayList<Event> data;

    public EventResponseMultiple(ArrayList<Event> data) { this.data = data; }

    public ArrayList<Event> getData() {
        return data;
    }

    public void setData(ArrayList<Event> data) {
        this.data = data;
    }
}
