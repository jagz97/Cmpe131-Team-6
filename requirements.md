## Functional Requirements


1. login (Nicholas)
2. logout (Nicholas)
3. Create New Account (Hector)
4. Delete an Account (Hector)
5. Add to cart (Nicholas)
6. User Profile (Hector)
7. Add item to seller (Jagjit)
8. User Rating (Hector)
9. Add Pictures for items (Jagjit)
10. Splash Page (Jagjit)
11. Find Items (Jagjit)
12. Buy item (Nicholas)
13. View all listed items (Jagjit)
14. Mailgun Api (Jagjit)

## Non-functional Requirements

1. Compatibility on Phone (Hector)
2. UI Interactive Support (All of us)
3. multilingual support (Jagjit)
4. Dark mode (Nicholas)

## Use Cases

1. Add to cart
- **Pre-condition:** User is looking at an item/product and if they decide they want save the item for purchase

- **Trigger:** The user clicks a button and the item will be added to their personalized cart

- **Primary Sequence:**
  
  1. User first clicks on item they are interested in
  2. User clicks the "Add to cart" button
  3. A login page is brought up 
  4. User types usernamne and password
  5. User logs into their account
  6. Item is aded to cart

- **Primary Postconditions:** User is back at items page

- **Alternate Sequence:** User is already logged into account
  
  1. User clicks on item they are interested in
  2. User clicks the "Add item to car" button
  3. Item is added to cart
  4. User is brought back to items page

- **Alternate Sequence:** User does not have an account
  
  1. User first clicks on item they are interested in
  2. User clicks the "Add to cart" button
  3. A login page is brought up 
  4. User clicks on create an account
  5. User creates an account
  6. User logs into their account
  7. Item is aded to cart

2. Buy Items

- **Pre-condition:** User has item added into cart and is ready to purchase (meaning that the user already has an account"

- **Trigger:** With an item already in a cart, the user will click a "checkout cart" button to buy items

- **Primary Sequence:** User has an account and is logged in without payment information
  
  1. User clicks "checkout item" to begin checkout scenario
  2. User is brought to a page to input payment information (credit card info)
  3. User is brought to input shipping information page
  4. User is brought to confirmation page
  5. User is brought to "order is confirmed" page

- **Primary Postconditions:** User clicks on "home" button to return to homepage

- **Alternate Sequence:** User has payment information inputed
  
  1. User clicks on "checkout item"
  2. User confirms payment information
  3. User confirms shipping information
  4. User is brought to confirmation page
  5. User is brought to "order is confirmed" page

3. Update User Profile
-**Summary**: A user visiting their profile will edit their profile and save the changes.

-**Actors**: The user visiting the web store and the system

- **Pre-condition:** the user needs to be signed in to an account in order to access the user profile page

- **Trigger:** the user profile button is pressed from the toolbar dropdown menu.

- **Primary Sequence:**
  
  1. The system loads the user profile, fills in text fields with current user information, and loads submit button
  2. The user will be able to scroll through their user profile and see different details about their profile
  3. The user selects any number of text fields and updates the information.
  4. The user clicks the save changes button.
  5. The system verifies the required text fields are filled in, the username and email are not taken
  6. The system verifies that the password fields are either all empty, or all filled in
  7. The system verifies the current password is equal to the current password inputted and that the new password and the confirmation password are equal
  8. The system updates the database with the new user object.

- **Primary Postconditions:**
  
  1. The user profile is displayed with the new information

- **Alternate Sequence:**
  
  1. The user leaves a required text field empty.
  2. The user presses the save changes button.
  3. The system checks if all required fields are filled in.
  4. The system flashes an error message at the top of the screen.

- **Alternate Sequence:**
  
  1. The user inputs a username or email that is taken
  2. The user presses the save changes button.
  3. The system checks is all required fields are filled in.
  4. The system checks if the email and username are unique.
  5. The system flashes an error message at the top of the screen.
  
 - **Alternate Sequence:**
  
  1. The user inputs an incorrect current password
  2. The user presses the save changes button.
  3. The system checks is all required fields are filled in.
  4. The system checks if the email and username are unique.
  5. The system checks if the inputted current password hash matches the current password hash.
  6. The system flashes an error message at the top of the screen.
  
   - **Alternate Sequence:**
  
  1. The user inputs a new password and a confirmation for new password that do not match
  2. The user presses the save changes button.
  3. The system checks is all required fields are filled in.
  4. The system checks if the email and username are unique.
  5. The system checks if the inputted current password hash matches the current password hash.
  6. The system checks if the two passwords are equal.
  7. The system flashes an error message at the top of the screen.
  

4. Add User Rating
- **Summary**: A user adds a rating and review for a product.

- **Actors**: The user visiting the web store and the system

- **Pre-condition:** the user needs to be signed in to an account

- **Trigger:** the user clicks on the add rating button/ edit rating button on the product page/card

- **Primary Sequence:**

  1. The user is taken to another page for adding a review.
  2. The system loads the text field, integer field, and the submit button.
  3. The user selects a star rating out of 5 stars
  4. The user can type in a review in the text box or leave it blank if they do not want to leave a review
  5. The user clicks on the confirm button to finish adding the rating.
  6. The system verifies that all required fields are filled in.
  7. The system verifies that the rating is from 0 to 5 stars.
  8. The system stores the rating in the database.
  9. The system loads the product page with the new review loaded in.
  
- **Primary Postconditions:**

  1. The user is returned to the page for the item.
  2. The system displays a list of all reviews for the product on the product page.

- **Alternate Sequence:**

  1. The user clicks on the cancel button
  2. The system loads the product page.
  
- **Alternate Sequence:**
  
  1. The user leaves a required field empty.
  2. The user presses the submit button
  3. The system checks if all required fields are filled in.
  4. The system flashes an error message at the top of the page.

- **Alternate Sequence:**
  
  1. The user inputs a star rating that is not from 0 to 5
  2. The user presses the submit button
  3. The system checks if all required fields are filled in.
  4. The system checks if the star rating is from 0 to 5
  5. The system flashes an error message at the top of the page.

5. Splash Page

-**Summary**: A user visiting the web store will be prompted with a welcome window to signup for newsletter.

-**Actors**: The user visiting the web store

- **Pre-condition:**
	- The user has access to internet to sucessfully land on website page.
  - The user is visitng website on Chrome Web Browser.
	

- **Trigger:** User visits the website using the URL link.

- **Primary Sequence:**
  
  1. System loads the welcome window.
  2. System displays a newsletter signup form.
  3. User enters a valid email address.
  4. User sumbit the request by pressing subscribe button.
  5. System adds user to the newsletter mailing list.
  6. System loads and displays the homepage.
  6. User is presented with the homepage of website.

- **Primary Postconditions:** 
  The user gets redirected to the homepage of the store.
  

- **Alternate Sequence:** 
  
  1. The user does not specify/select a language and presses continue to store.
  3. System loads and displays the homepage.
  3. User is presented with homepage of website.
 
6. Find Items

- **Summary**: A user can easily look for the available items using search/find items button.

- **Actors**: The user visiting the web store

- **Pre-condition:**
	- The user has selected the selected the desired language or exited the splash/welcome page.
	
- **Trigger:** User clicks the search button.

- **Primary Sequence:**
  
  1. System displays the search bar for user to type in and searh for items.
  2. User enters the desired name of item/items to be searched.
  3. User presses the search button.
  4. System searches for the items in the store.
  5. System returns matching item/items from the search.
  6. User is displayed with the items matching the search.
  
- **Primary Postconditions:** 

  The user gets displayed with the matching items returned by the search.
  OR
  The user gets displayed with no results.
    - No matching items were found.
   
- **Alternate Sequence:** 
  
  1. The user entered the item name that does not match available items in store.
  2. System searches for item in the store and returns no results.
  3. System displays message saying no items found.
  4. System prompts user to search for different items.

- **Alternate Sequence:** 
  
  1. The user does not enter anything into the search bar and presses search button.
  2. System searches for item in the store and returns all the available items.
  3. User gets displayed with all the available items.