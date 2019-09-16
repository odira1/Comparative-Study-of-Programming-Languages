<b> Banking Simulation - Exploring Erlang's concurrency model. </b>

<li> Reads a set of banks and customers for the purpose of completing loans. </li>
<li> Each Customer and Banks runs as indivisual erlang processes. </li>
<li> Customers request loans to banks until their goals are reached. </li>
<li> Banks issue and deny loans as per the funds available.</li> <br/>

prerequisites: Installation of Erlang and updating the environment variable. 

Instructions to run the project:

    Open shell
    cd inside project location.
    Type erl.
    Type c(money). c(customer). c(bank).
    To run money:start().
