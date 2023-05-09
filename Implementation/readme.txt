PythonAnywhere Domain Name: sc19rab.pythonanywhere.com (Entrypoint -> https://sc19rab.pythonanywhere.com/)

PythonAnywhere Domain Admin Endpoint: https://sc19rab.pythonanywhere.com/admin/
Service Admin Page Username: ammar
Service Admin Page Email: m.a.alsalka@leeds.ac.uk
Service Admin Page Password: ?9testpassword9!


############################## HOW TO USE PAYFRIEND ##############################
1. In order to use the service and process transactions, a user has to first register on PayFriend through requesting the https://sc19rab.pythonanywhere.com/signup/ endpoint with a username and a password in the form data body.
------------------------------------------------------------------------------------------------
POST https://sc19rab.pythonanywhere.com/signup/
email:test@leeds.com
Password:testpassword
------------------------------------------------------------------------------------------------

2. Then, to process a transaction, a user has to do so through requesting the https://sc19rab.pythonanywhere.com/pay/ endpoint, where the form data body contains the user account details and the transaction details.
------------------------------------------------------------------------------------------------
POST https://sc19rab.pythonanywhere.com/pay/ 
email:test@leeds.com
Password:testpassword
value:10.05
company:BA
city:London
postcode:L45PQ
currency:GBP
country:United Kingdom
------------------------------------------------------------------------------------------------

3. To delete a transaction which was processed by the PayFriend service, a user can do so through requesting the https://sc19rab.pythonanywhere.com/transactions/<TRANSACTION ID> endpoint, where the <TRANSACTION ID> path in the URL links to the transaction to be deleted.
------------------------------------------------------------------------------------------------
DELETE https://sc19rab.pythonanywhere.com/pay/ba881d16-a93c-4ce9-9f2d-a946fd287714 (example transaction ID)
------------------------------------------------------------------------------------------------