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
- **Pre-condition:** User is looking at an item/product and if they decide they want save the item for purchase

- **Trigger:** <can be a list or short description> The user clicks a button and the item will be added to their personalized cart

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

- **Alternate Sequence <optional>:** User does not have an account
  
  1. User first clicks on item they are interested in
  2. User clicks the "Add to cart" button
  3. A login page is brought up 
  4. User clicks on create an account
  5. User creates an account
  6. User logs into their account
  7. Item is aded to cart

2. Buy Items

- **Pre-condition:** User has item added into cart and is ready to purchase (meaning that the user already has an account"

- **Trigger:** <can be a list or short description> With an item already in a cart, the user will click a "checkout cart" button to buy items

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
