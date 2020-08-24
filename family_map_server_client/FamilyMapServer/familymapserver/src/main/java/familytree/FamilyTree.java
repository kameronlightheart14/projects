package familytree;

import java.sql.Connection;
import java.util.ArrayList;

import dao.DataAccessException;
import dao.Database;
import dao.EventDao;
import dao.PersonDao;
import dao.ResourcePack;
import model.Event;
import model.Person;

public class FamilyTree {
    private FamilyTreeNode userNode;
    private String rootUsername;
    public static final String MARRIAGE = "Marriage";
    public static final int GENERATION_GAP = 25;
    public static final int MARRIAGE_OFFSET = 5;
    public static final int DEATH_OFFSET = 20;
    public static final int FIRST_BIRTH_YEAR = 2010;
    public static final String MALE = "m";
    public static final String FEMALE = "f";
    private int numNodes = 0;
    private int numEvents = 0;

    public FamilyTree(Person userPerson) {
        numNodes += 1;
        rootUsername = userPerson.getDescendant();
        userNode = new FamilyTreeNode(userPerson);
        Event birth = Event.generateBirthEvent(FIRST_BIRTH_YEAR, userPerson);
        numEvents += 1;
        userNode.addEvent(birth);
        userNode.setBirthYear(FIRST_BIRTH_YEAR);
    }

    public ArrayList<FamilyTreeNode> addSpousePair(FamilyTreeNode childNode,
                                                   ArrayList<FamilyTreeNode> toAddPeople) {
        numNodes += 2;
        // 1. Create father
        Person father = new Person(rootUsername,
                ResourcePack.getRandomMaleName(), childNode.getPerson().getLastName(),
                MALE, "", "", "");
        String fatherID = father.getPersonID();
        // 2. Create mother to match
        Person mother = new Person(rootUsername,
                ResourcePack.getRandomFemaleName(), ResourcePack.getRandomLastName(),
                FEMALE, "", "", fatherID);
        // Link father to mother
        father.setSpouseID(mother.getPersonID());
        FamilyTreeNode fatherNode = new FamilyTreeNode(father);
        FamilyTreeNode motherNode = new FamilyTreeNode(mother);

        int birthYear = childNode.getBirthYear() - GENERATION_GAP;
        int anniversary = childNode.getBirthYear() - MARRIAGE_OFFSET;
        int deathYear = birthYear +  DEATH_OFFSET;

        fatherNode.setBirthYear(birthYear);
        motherNode.setBirthYear(birthYear);

        // Generate Events for FatherNode
        Event fatherBirth = Event.generateBirthEvent(birthYear, father);
        Event marriage = Event.generateMarriageEvent(anniversary, father);
        Event fatherDeath = Event.generateDeathEvent(deathYear, father);
        numEvents += 3;
        fatherNode.addEvent(fatherBirth);
        fatherNode.addEvent(marriage);
        fatherNode.addEvent(fatherDeath);

        // Generate Events for MotherNode
        Event motherBirth = Event.generateBirthEvent(birthYear, mother);
        marriage = new Event(marriage.getDescendant(), mother.getPersonID(), marriage.getLatitude(),
                marriage.getLongitude(), marriage.getCountry(), marriage.getCity(),
                MARRIAGE, anniversary);
        Event motherDeath = Event.generateDeathEvent(deathYear, mother);
        numEvents += 3;
        motherNode.addEvent(motherBirth);
        motherNode.addEvent(marriage);
        motherNode.addEvent(motherDeath);
        // 3. link to child node
        childNode.getPerson().setFatherID(father.getPersonID());
        childNode.getPerson().setMotherID(mother.getPersonID());
        childNode.setFatherNode(fatherNode);
        childNode.setMotherNode(motherNode);
        // 4 commit parents to database
        toAddPeople.add(fatherNode);
        toAddPeople.add(motherNode);

        ArrayList<FamilyTreeNode> FMNodes = new ArrayList<>();
        FMNodes.add(fatherNode);
        FMNodes.add(motherNode);

//        System.out.printf("Child: %s Father: %s mother: %s\n", childNode.getPerson().getFirstName(),
//                father.getFirstName(), mother.getFirstName());

        return FMNodes;
    }

    public void addGenerations(int numGenerations) throws DataAccessException {
        ArrayList<FamilyTreeNode> toAddPeople = new ArrayList<>();
        toAddPeople.add(userNode);
        if (numGenerations == 0) {
            return;
        }
        // Add first generation
        ArrayList<FamilyTreeNode> currentGen = new ArrayList<>();
        currentGen.addAll(addSpousePair(userNode, toAddPeople));
        // If numGenerations > 1 keep adding generations
        for (int i = 0; i < numGenerations - 1; ++i) {
            ArrayList<FamilyTreeNode> FMNext = new ArrayList<>();
            for (FamilyTreeNode currentNode : currentGen) {
                FMNext.addAll(addSpousePair(currentNode, toAddPeople));
            }
            currentGen = FMNext;
        }
        commitTree(toAddPeople);
    }

    public void commitTree(ArrayList<FamilyTreeNode> toAddPeople) throws DataAccessException {
        Database db = new Database();
        try {
            Connection conn = db.openConnection();
            PersonDao personDao = new PersonDao(conn);
            EventDao eventDao = new EventDao(conn);
            for (FamilyTreeNode personNode : toAddPeople) {
                personDao.insert(personNode.getPerson());
                for (Event event : personNode.getEvents()) {
                    eventDao.insert(event);
                }
            }
            db.closeConnection(true);
        } catch (DataAccessException e) {
            db.closeConnection(false);
            throw e;
        }
    }

    public int getNumNodes() {
        return numNodes;
    }

    public void setNumNodes(int numNodes) {
        this.numNodes = numNodes;
    }

    public int getNumEvents() {
        return numEvents;
    }

    public void setNumEvents(int numEvents) {
        this.numEvents = numEvents;
    }
}
