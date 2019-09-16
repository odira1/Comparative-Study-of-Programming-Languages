%%%-------------------------------------------------------------------
%%% @author odira
%%% @copyright (C) 2019, <COMPANY>
%%% @doc
%%%
%%% @end
%%% Created : 12. Jun 2019 11:18 PM
%%%-------------------------------------------------------------------
-module(money).
-author("odira").

%% API
-export([start/0]).

start() ->
  {_, Customers} = file:consult("customers.txt"),
  {_, Banks} = file:consult("banks.txt"),
  ets:new(toprint_customer, [set,named_table]),
  ets:new(toprint_customerNE, [set, named_table]),
  ets:new(toprint_bank, [set, named_table]),
  io:format("~n ** Customers and loan objectives ** ~n~n"),
  lists:foreach(fun list_customers/1, Customers),
  io:format("~n ** Banks and Financial resources ** ~n~n"),
  lists:foreach(fun list_banks/1, Banks),
  master(Banks, Customers).

list_customers({Customer, Total_funds}) ->
  io:format("~p: ~p~n",[Customer, Total_funds]).

list_banks({Bank, Total_loan}) ->
  io:format("~p: ~p~n",[Bank, Total_loan]).

master(Banks, Customers) ->
  io:format("~n"),
  create_bank_process(Banks),
  create_customer_process(Customers),

  self() ! handle_request([Banks], [Customers]).


create_bank_process([]) ->
  io:format("");
%%  io:format("~n~n Processes: ~n ~p ~n~n", [registered()]);

create_bank_process([Current_Bank|Other_Banks]) ->
  Current_Bank_Name = element(1, Current_Bank),
  register(Current_Bank_Name, spawn(bank, start, [self(), Current_Bank_Name, element(2, Current_Bank)])),
  create_bank_process(Other_Banks).

create_customer_process([]) ->
  io:format("");
%%  io:format("~n~n Processes: ~n ~p ~n~n", [registered()]);

create_customer_process([Current_Customer|Other_Customers])  ->
  Current_Customer_Name = element(1, Current_Customer),
  register(Current_Customer_Name, spawn(customer, start, [self(), Current_Customer, element(2, Current_Customer)])),
  create_customer_process(Other_Customers).

print_list([]) ->
  io:format("");

print_list([Head|Tail]) ->
  io:format("~p has reached the objective of ~p dollar(s). Woo Hoo! ~n", [element(1, Head), element(2, Head)]),
  print_list(Tail).

print_list_bank([]) ->
  io:format("");

print_list_bank([Head|Tail]) ->
  io:format("~p has ~p dollar(s) remaining. ~n", [element(1, Head), element(2, Head)]),
  print_list_bank(Tail).

print_list_ne([]) ->
  io:format("");

print_list_ne([Head|Tail]) ->
  io:format("~p was only able to borrow ~p dollar(s). Boo Hoo! ~n", [element(1, Head), element(2, Head)]),
  print_list_ne(Tail).

handle_request([Banks], [Customers])  ->
  receive
    {Pid, "bank_request"} ->
      Pid ! {self(), [Banks]},
%%      io:format("bank request handled for ~p ~n", [Pid]),
      handle_request([Banks], [Customers]);
    {Pid, "loan_request", Customer, Loan_amount, Bank} ->
      io:format("~p requests a loan of ~p dollar(s) from ~p ~n", [Customer, Loan_amount, Bank]),
      handle_request([Banks], [Customers]);
    {Pid, "loan_approved", Customer, Loan_amount, Bank} ->
      io:format("~p approves a loan of ~p dollars from ~p ~n", [Bank, Loan_amount, Customer]),
      handle_request([Banks], [Customers]);
      {Pid, "loan_denied", Customer, Loan_amount, Bank} ->
      io:format("~p denies a loan of ~p dollars from ~p ~n", [Bank, Loan_amount, Customer]),
      handle_request([Banks], [Customers]);
      {Pid, "goal_reached", Customer, Loan} ->
%%      io:format("~p has reached the objective of ~p dollar(s). Woo Hoo! ~n", [Customer, Loan]),
      handle_request([Banks], [Customers]);
      {Pid, "Notifications", "customer", [Message]} ->
      add_message(Message),
      handle_request([Banks], [Customers]);
    {Pid, "Notifications", "bank", Bank, Fund} ->
      add_message(Bank, Fund),
      handle_request([Banks], [Customers]);
      {Pid, "Notifications", "customer_notenough", Name, Fund} ->
        add_message_ne(Name, Fund),
        handle_request([Banks], [Customers])

      after 3000 ->
          print_list(ets:tab2list(toprint_customer)),
          print_list_ne(ets:tab2list(toprint_customerNE)),
          print_list_bank(ets:tab2list(toprint_bank))
  end.

add_message(Message) ->
%%  io:format("~p", [Message]),
  ets:insert(toprint_customer, [Message]).

add_message(Bank, Fund) ->
  Message = {Bank, Fund},
  ets:insert(toprint_bank, Message).

add_message_ne(Name, Fund) ->
  Customer = {Name, Fund},
  ets:insert(toprint_customerNE, Customer).




