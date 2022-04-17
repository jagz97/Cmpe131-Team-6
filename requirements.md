## Functional Requirements

1. login
2. logout
3. Create New Account
4. Delete an Account
5. Add to cart
6. Update User Profile
7. Add item to seller 
8. Add User Rating
9. Add Pictures for items
10. Splash Page
11. Find Items
12. Buy item

## Non-functional Requirements

1. Compatibility on Phone
2. UI Interactive Support
3. 
4. 

## Use Cases

1. Update User Profile
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

2. Add User Rating
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
