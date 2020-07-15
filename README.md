# DeliveryMatchUp
Quick script to document, calculate, and archive Caviar and DoorDash orders. Mainly used to double check if the commissions and restaurant pay-outs are correct.

Run Process:
1. Cashier In
2. Operations > In House Charge > Create In House Statements
3. Copy-Paste Invoice into caviar.txt and doordash.txt
4. Make note of the totals of each and subtract from sales that week
5. Retrieve order_items.csv and pickup_order_items.csv from Caviar Dashboard
6. In Terminal, execute: ./run.sh
7. During runtime, enter the data displayed on DoorDash Dashboard
8. Operations > Receive Payments > Caviar/DoorDash
9. Pay with cash
10. Revenue Center > Close EDC Batch
11. Cashier Out

What it does and assumptions made:
- Displays date range starting with last batched date to last delivery date recorded
- Compares POS totals with Dashboard totals
- Assumes maximum of 20% commission (worst case is all delivery 20%, best case is all pickup 5%)
- Assumes a 5% subtotal error between POS and Dashboard
- Once program has run, it'll archive and clear all data files into folders labeled with their appropriate dates
