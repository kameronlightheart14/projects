package dao;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Random;
import java.util.Scanner;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import model.Location;

public class ResourcePack {
    public static final ArrayList<String> fnames;
    public static final ArrayList<Location> locations;
    public static final ArrayList<String> mnames;
    public static final ArrayList<String> lnames;

    static {
        fnames = new ArrayList<>();
        locations = new ArrayList<>();
        mnames = new ArrayList<>();
        lnames = new ArrayList<>();

        try {
            // Read in data files as text
            Scanner scanner1 = new Scanner( new File("C:/Users/kamer/Desktop/CS 240/CS 240 Repo/FamilyMapServer/familymapserver/src/main/resources/locations.json") );
            String locationsStr = scanner1.useDelimiter("\\A").next();
            scanner1.close();
            Scanner scanner2 = new Scanner( new File("C:/Users/kamer/Desktop/CS 240/CS 240 Repo/FamilyMapServer/familymapserver/src/main/resources/fnames.json") );
            String fnamesStr = scanner2.useDelimiter("\\A").next();
            scanner2.close();
            Scanner scanner3 = new Scanner( new File("C:/Users/kamer/Desktop/CS 240/CS 240 Repo/FamilyMapServer/familymapserver/src/main/resources/mnames.json") );
            String mnamesStr = scanner3.useDelimiter("\\A").next();
            scanner3.close();
            Scanner scanner4 = new Scanner( new File("C:/Users/kamer/Desktop/CS 240/CS 240 Repo/FamilyMapServer/familymapserver/src/main/resources/snames.json") );
            String lnamesStr = scanner4.useDelimiter("\\A").next();
            scanner4.close();
            // Parse Locations from JSON array
            JSONArray jsonarray = new JSONArray(locationsStr);
            for (int i = 0; i < jsonarray.length(); i++) {
                JSONObject jsonobject = jsonarray.getJSONObject(i);
                String country = jsonobject.getString("country");
                String city = jsonobject.getString("city");
                double latitude = jsonobject.getDouble("latitude");
                double longitude = jsonobject.getDouble("longitude");
                locations.add(new Location(country, city, latitude, longitude));
            }
            // Parse female names from JSON string
            jsonarray = new JSONArray(fnamesStr);
            for (int i = 0; i < jsonarray.length(); ++i) {
                fnames.add(jsonarray.getString(i));
            }
            // Parse males names from JSON string
            jsonarray = new JSONArray(mnamesStr);
            for (int i = 0; i < jsonarray.length(); ++i) {
                mnames.add(jsonarray.getString(i));
            }

            jsonarray = new JSONArray(lnamesStr);
            for (int i = 0; i < jsonarray.length(); ++i) {
                lnames.add(jsonarray.getString(i));
            }
        } catch(FileNotFoundException e) {
            e.printStackTrace();
        } catch(JSONException e) {
            e.printStackTrace();
        }
    }
    public static Location getRandomLocation() {
        Random rand = new Random();
        int randomInt = rand.nextInt(locations.size());
        return locations.get(randomInt);
    }
    public static String getRandomFemaleName() {
        Random rand = new Random();
        int randomInt = rand.nextInt(fnames.size());
        return fnames.get(randomInt);
    }
    public static String getRandomMaleName() {
        Random rand = new Random();
        int randomInt = rand.nextInt(mnames.size());
        return mnames.get(randomInt);
    }
    public static String getRandomLastName() {
        Random rand = new Random();
        int randomInt = rand.nextInt(lnames.size());
        return lnames.get(randomInt);
    }
}
