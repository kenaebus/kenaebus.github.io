package contact;
import java.util.HashMap;
import java.util.Map;

public class RevisedContactService {
    
    // Stores contacts by unique contactID
    private final Map<String, Contact> contactMap;


    /**
	 * The contact service shall be able to add contacts with a unique ID.
	 * The contact service shall be able to delete contacts per contact ID.
	 * The contact service shall be able to update contact fields per contact ID. The following fields are updatable:
	 * 		-firstName
	 * 		-lastName
	 * 		-Number
	 * 		-Address
	 */
	
	// Initializers
    public ContactService() {
        contactMap = new HashMap<>();
    }

     /**
     * Adds a new contact to the map if the ID is unique.
     * 
     * @param contact Contact object to add
     * @return true if added successfully, false if duplicate ID
     */

     public boolean addContact( Contact c) {
        String contactID = contact.getContactID();

        if (contactMap.containsKey(contactID)) {
            return false;  // ContactID already exists
        }
        contactMap.put(contactID, c);
        return truel
     }

     /**
     * Deletes a contact by contact ID.
     * 
     * @param contactID ID of the contact to delete
     * @return true if contact was found and deleted, false otherwise
     */
     public boolean deleteContact(String contactID) {
        return contactMap.remove(contactID) != null;
     }


     /**
     * Updates contact fields individually by ID.
     * Only non-null and valid inputs will be applied.
     * 
     * @param contactID ID of the contact to update
     * @param firstName New first name (nullable)
     * @param lastName New last name (nullable)
     * @param phoneNumber New phone number (nullable)
     * @param address New address (nullable)
     * @return true if contact exists and update was applied, false otherwise
     */
    public boolean updateContact(String contactID, String firstName, String lastName,
                                 String phoneNumber, String address) 
    {
        Contact c = contactMap.get(contactID);
        if (c == null) {
            return false;
        }

        try {
             if (firstName != null) c.setFirstName(firstName);
            if (lastName != null) c.setLastName(lastName);
            if (phoneNumber != null) c.setPhoneNumber(phoneNumber);
            if (address != null) c.setAddress(address);
        } catch (IllegalArgumentException e) {
            System.err.println("Update failed: " + e.getMessage());
            return false;
        }
        return true;
    }

    /**
     * Retrieves a contact by ID.
     * 
     * @param contactID Unique ID of the contact
     * @return Contact object or null if not found
     */
    public Contact getContact(String contactID) {
        return contactMap.get(contactID);
    }

}
