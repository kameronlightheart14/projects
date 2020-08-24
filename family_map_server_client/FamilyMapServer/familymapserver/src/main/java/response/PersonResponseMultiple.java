package response;

import java.util.ArrayList;

import model.Person;

public class PersonResponseMultiple extends requests.JsonPacket {
    private ArrayList<Person> data;

    public PersonResponseMultiple(ArrayList<Person> data) {
        this.data = data;
    }

    public ArrayList<Person> getData() {
        return data;
    }

    public void setData(ArrayList<Person> data) {
        this.data = data;
    }
}
