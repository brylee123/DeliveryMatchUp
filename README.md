# DeliveryMatchUp
Quick script to document, calculate, and archive Caviar and DoorDash orders. Mainly used to double check if the commissions and restaurant pay-outs are correct.

Run Pre-Process:
1. Cashier In
2. Operations > In House Charge > Create In House Statements
3. Copy-Paste Invoice into caviar.txt and doordash.txt
4. Make note of the totals of each and subtract from sales that week.

Running the Program:
5. Retrieve order_items.csv and pickup_order_items.csv from Caviar Dashboard
6. In Terminal, execute: ./run.sh
7. During runtime, enter the data displayed on DoorDash Dashboard

Finish up the Process:
8. Operations > Receive Payments > Caviar/DoorDash
9. Pay with cash
10. Revenue Center > Close EDC Batch
11. Cashier Out
