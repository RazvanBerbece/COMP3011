# PayPal Payment Service Background Research

## Description of service
PayPal is an online payment service that allows users to pay for online or physical goods without using an actual credit/debit card or any financial detail. The PayPal account balance comes from either funding the account with money using a credit/debit card, bank transfers or transfers from other accounts. PayPal is also known to be very secure, fast, and flexible when it comes to ways of funding the account.

In some sense, PayPal can be considered as a middleman for online payments, making purchases simpler by not requiring users to input their financial details every time they make a payment.

Businesses can set up PayPal accounts to allow their customers to pay for their services directly, as PayPal can be integrated into web apps through the PayPal REST API. 
The PayPal REST API can handle invoicing, orders, payments, payouts, subscriptions, and many other features programmatically through HTTP requests and responses, which makes it a great tool for a business to integrate in their software to support multiple payment platforms.

## Data flow diagram
![PayPal Payment Service Dataflow Diagram](dataflow_diagram.png?raw=true "PayPal Payment Service Dataflow Diagram")

## Description of data flow
The PayPal payment service is integrated into various flight businesses’ applications through their PayPal REST API. 

PayPal provides a gateway to their service through the ‘paypal.com/checkoutnow’ endpoint which can be requested using HTTP GET requests populated with various query data (e.g.: auth token from flight business, payment method, price, session ID). The PayPal Checkout Now resource then links to the PayPal Login resource, as users need to be logged in to finalise a payment. The login resource can be read (GET login form) and POSTed to (filled in login form) to execute the login method.

Optionally, the PayPal Login resource also links to the PayPal Signup resource, for users who do not have a PayPal account and who need to create one to finalise the payment. Method wise, the same REST operations apply as for the login resource (GET the form, POST the filled in new account form).

Finally, both the login and signup resources link to the PayPal Checkout Now resource, which is the final point of payment, at which the user can press a button to finalise the payment using funds available in their account (via a POST request). 

## Notes
- Will use the sandboxed PayPal REST API to integrate this payment method into the solution
