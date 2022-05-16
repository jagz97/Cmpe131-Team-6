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

## Non-functional Requirements

1. Compatibility on Phone (Hector)
2. UI Interactive Support (All of us)
3. multilingual support (Jagjit)
4. Dark mode (Nicholas)

## Use Cases

1. Add to cart

- **Summary:** Before buying an item, a user must be able to add an item to a cart and then they are able to buy their item. This function, add to cart, makes it so the user can add the item to their cart. 

- **Actors:** The user looking to add an item they are interested into a cart

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

- **Summary:** A user that is looking to buy an item would run through this function, adding in their payment information and checking out would bring them to a confirmation screen. 

-**Actors:** The users looking to purchase an item in their cart.

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
- **Pre-condition:** the user needs to be signed in to an account in order to access the user profile page

- **Trigger:** the user profile button is pressed that will appear on either a sidebar or a topbar. 

- **Primary Sequence:**
  
  1. The user will be able to scroll through their user profile and see different details about their profile
  2. The user clicks on the edit button next to the variable they want to update
  3. The user types in what they want to update the variable to in the text box that appears
  4. The user clicks on the confirm button.

- **Primary Postconditions:**
  
  1. The user profile is updated with the new variable, and the user profile also displays the new variable.

- **Alternate Sequence:**
  
  1. The user inputs a new variable which does not meet requirements which could be length requirements or specific character type requirements.
  2. The text box displays an error message.
  3. The confirm button is disabled until the textbox contains valid input.

- **Alternate Sequence:**
  
  1. The user clicks on the cancel button
  2. The textbox to enter the new variable disappears.

4. Add User Rating
- **Pre-condition:** the user needs to be signed in to an account and must have purchased an item in order to add a rating for the item

- **Trigger:** the user clicks on the add rating button/ edit rating button  on the item page

- **Primary Sequence:**

  1. The user is taken to another page for adding a review.
  2. The user selects a star rating out of 5 stars
  3. The user can type in a review in the text box or leave it blank if they do not want to leave a review
  4. The user clicks on the confirm button to finish adding the rating.
  
- **Primary Postconditions:**

  1. The user is returned to the page for the item.
  2. The item's average rating is updated and the number of ratings for the item is updated.

- **Alternate Sequence:**

  1. The user clicks on the cancel button
  2. An "are you sure you want to leave this review" message pops up.
  3. The user clicks on the "leave" button to return to the item page.

5. Splash Page

-**Summary**: A user visiting the web store will be prompted with a welcome window to choose region and language.

-**Actors**: The user visiting the web store

- **Pre-condition:**
	- The user has access to internet to sucessfully land on website page.
  - The user is visitng website on Chrome Web Browser.
	

- **Trigger:** User visits the website using the URL link.

- **Primary Sequence:**
  
  1. System loads the welcome window.
  2. System displays two options to choose from; select country/region and language.
  3. User selects the desired region/country and chooses the desired language.
  4. User sumbits the request by pressing go button.
  5. System switches the language to desired language selected by the user.
  6. System loads and displays the homepage.
  6. User is presented with the homepage in the selcted language.

- **Primary Postconditions:** 
  The user gets displayed with the homepage in the selected language.
  OR
  The user gets displayed with homepage in the default language. 

- **Alternate Sequence:** 
  
  1. The user does not speficy/select a language and presses the close button.
  2. System automatically selects the default language.
  3. System loads and displays the homepage.
  3. User is presented with homepage in default language.
 
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