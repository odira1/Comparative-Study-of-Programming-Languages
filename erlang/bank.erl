%%%-------------------------------------------------------------------
%%% @author odira
%%% @copyright (C) 2019, <COMPANY>
%%% @doc
%%%
%%% @end
%%% Created : 12. Jun 2019 11:21 PM
%%%-------------------------------------------------------------------
-module(bank).
-author("odira").

%% API
-export([start/3]).

start(Process, Bank, Fund) ->
  timer:sleep(100),
%%  io:format("bank process working ~p~n", [self()]),
  handle_loans(Process, Bank, Fund).

handle_loans(Process, Bank, Fund) ->
  receive
    {Pid, Loan_amount} ->

      case (Loan_amount =< Fund) of
        true ->
%%          io:format("sensing a loan request ~n"),
          Pid ! {self(), "approved"},
          handle_loans(Process, Bank, Fund - Loan_amount);
        false ->
%%          io:format("Loan Denied. ~n"),
          Pid ! {self(), "denied"},
          handle_loans(Process, Bank, Fund)
      end

    after 3000 ->
    Process ! {self(), "Notifications", "bank", Bank, Fund}

  end.
