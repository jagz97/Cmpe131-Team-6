## Functional Requirements

1. login
2. logout
3. Create New Account
4. Delete an Account
5. Add to cart
6. User Profile
7. Add item to seller 
8. User Rating
9. Add Pictures for items
10. Splash Page
11. Find Items
12. Buy item

## Non-functional Requirements

1. Compatibility on Phone
2. UI Interactive Support
3. Multilingual Support
4. non-functional

## Use Cases

1. Splash Page

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
 
2. Find Items

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