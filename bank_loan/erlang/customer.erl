%%%-------------------------------------------------------------------
%%% @author odira
%%% @copyright (C) 2019, <COMPANY>
%%% @doc
%%%
%%% @end
%%% Created : 12. Jun 2019 11:20 PM
%%%-------------------------------------------------------------------
-module(customer).
-author("odira").

%% API
-export([start/3]).


start(Process, Customer, Loan) ->
    timer:sleep(100),
%%    io:format("customer process working ~p ~n", [self()]),
    make_request(Process, Customer, Loan).

make_request(Process, Customer, Loan, []) ->
%%  io:format("No banks can service this customer anymore ~n"),

  case (element(2, Customer) - Loan >= 0) of
    true ->
    Process ! {self(), "Notifications", "customer_notenough", element(1, Customer), element(2, Customer) - Loan};
    false ->
%%    io:format("~p could only get ~p ~n",[Customer, element(2, Customer) - Loan])
    exit(normal)
  end,

  exit(normal);

make_request(Process, Customer, Loan, Banks) ->
  case (Loan == 0) of
    true ->

%%      io:format("~p has reached the objective of ~p dollar(s). Woo Hoo! ~n", [element(1, Customer), element(2, Customer)]),
      Process ! {self(), "Notifications", "customer", [Customer]},
      Process ! {self(), "goal_reached", element(1, Customer), element(2, Customer)},
      exit(normal);
    false ->
      random:seed(),
      Loan_amount = rand:uniform(50),
      case (Loan < Loan_amount) of
        true ->
%%          io:format("----------- selecting another loan amount ~n"),
          make_request(Process, Customer, Loan, Banks);
        false ->
          Selected_bank_name = lists:nth(rand:uniform(length(Banks)), Banks),
%%          io:format("Selected_Banks: ~p", [Selected_bank_name]),
          Selected_bank_process = whereis(element(1, Selected_bank_name)),
%%          io:format("Choosen Bank: ~p", [Selected_bank_process]),
          make_request(Process, Loan, Customer, Selected_bank_name, Selected_bank_process, Loan_amount, Banks)
      end
  end.

make_request(Process, Loan, Customer, Bank, Bank_Pid, Loan_amount, Banks) ->
  Process ! {self(), "loan_request", element(1, Customer), Loan_amount, element(1, Bank)},
  Bank_Pid ! {self(), Loan_amount},

  receive
    {Pid, "approved"} ->
%%      io:format("~p approves a loan of ~p dollar(s) from ~p ~n", [Bank, Loan_amount, Customer]),
      Process ! {self(), "loan_approved", element(1, Customer), Loan_amount, element(1, Bank)},
      make_request(Process, Customer, Loan - Loan_amount, Banks);
    {Pid, "denied"} ->
%%      io:format("~p denies a loan of ~p dollars from ~p ~n", [Bank, Loan_amount, Customer]),
      Process ! {self(), "loan_denied", element(1, Customer), Loan_amount, element(1, Bank)},
      make_request(Process, Customer, Loan, lists:delete(Bank,Banks))
  end.

make_request(Process, Customer, Loan) ->
  Process ! {self(), "bank_request"},
  receive
    {Pid, [Banks]} ->
      make_request(Process, Customer, Loan, Banks)
  end.
