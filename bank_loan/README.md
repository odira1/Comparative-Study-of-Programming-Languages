<b> Banking Simulation - Exploring Erlang's concurrency model. </b>

Reads a set of banks and customers for the purpose of completing loans.
Each Customer and Banks runs as an indivisual Erlang Process. 
Customers request loans to bank as until their goal is fulfilled. 
Banks issues and denies loans as per the funds available.

prerequisites: Installation of Erlang and updating the environment variable. 

Instructions to run the project:

    Open shell
    cd inside project location.
    Type erl.
    Type c(money). c(customer). c(bank).
    To run money:start().
