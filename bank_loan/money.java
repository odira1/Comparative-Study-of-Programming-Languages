import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;
import java.util.concurrent.ThreadLocalRandom;

class Customer implements Runnable{
    String name;
    volatile Integer loan;
    HashMap<String, Bank> banks;
    Thread thread;
    Random rand = new Random();
    ArrayList<String> keysAsArray;


    volatile Integer recievedLoan;
    Integer loanCounter;
    Integer randomLoan;
    boolean approvalStatus = false;

    Customer(String Name, Integer Loan, HashMap Banks){
        name = Name;
        loan = Loan;
        loanCounter = Loan;
        banks = Banks;
        keysAsArray = new ArrayList<>(Banks.keySet());


        thread = new Thread(this, name);
        thread.start();

    }

    public void run(){
        recievedLoan = 0;
        boolean check = false;

            while (loan - recievedLoan != 0 && !keysAsArray.isEmpty()) {
                if (check == true){
                    if (loan - recievedLoan == 1){
                        randomLoan = 1;
                    }else if (loan - recievedLoan > 1){
                        randomLoan = ThreadLocalRandom.current().nextInt(1, loan - recievedLoan);
                    }
                    else{
                        break;
                    }
                }else{
                    randomLoan = ThreadLocalRandom.current().nextInt(1, 50);
                }




                boolean checkRandom = (randomLoan + recievedLoan) > loan;
                if (checkRandom) {
                    check = true;
                    continue;
                } else {
                    String key = keysAsArray.get(rand.nextInt(keysAsArray.size()));
                    if (this.banks.get(key).loanRequest(this, randomLoan)) {
                        updateRecievedLoan(randomLoan);
                        loanCounter = loanCounter - recievedLoan;
                        check = false;
                    } else {
                        keysAsArray.remove(key);
                    }
                }
            }


            if (loan - recievedLoan == 0) {
                money.addFinalMessage(Thread.currentThread().getName() + " has reached the objective of " + recievedLoan + " dollar(s). Woo Hoo!");
            } else {
                money.addFinalMessage(Thread.currentThread().getName() + " was only able to borrow " + recievedLoan + " dollar(s). Boo Hoo!");
            }
    }

    private void updateRecievedLoan(Integer randomLoan) {
        this.recievedLoan += randomLoan;
    }


}

















class Bank implements Runnable{
    String name;
    Integer funds;
    Thread thread;
    static boolean flag = true;
    String message = null;
    Random rand = new Random();

    Bank(String Name, Integer Funds){
        name = Name;
        funds = Funds;
        thread = new Thread(this, name);
        thread.start();

    }

    public void run(){
        try {
            Thread.sleep(5000);


//            while (flag){
//                if (message != null){
//                    money.printMessage(message);
//                    message = null;
//                }
//            }

        } catch (InterruptedException e){
            e.printStackTrace();
        }

        money.addFinalMessage(Thread.currentThread().getName() + " has " + funds + " dollar(s) remaining.");
        //System.out.println(name + "exiting");
    }

    public synchronized boolean loanRequest(Customer customer, Integer Amount){
        money.printMessage(Thread.currentThread().getName() + " requests a loan of "+ Amount + " dollar(s) from " + this.name);
        boolean result = false;
        try {
            Thread.sleep(rand.nextInt((100 - 10) + 1) + 10);
            if (funds - Amount >= 0){
                money.printMessage(this.name + " approves a loan of " + Amount + " dollars from " + Thread.currentThread().getName());
                updateFunds(funds - Amount);
                result = true;
            }else {
                money.printMessage(this.name + " denies a loan of " + Amount + " dollars from " + Thread.currentThread().getName());
                result = false;
            }

        } catch (Exception e) {
            e.printStackTrace();
        }



        return result;
    }

    public void updateFunds(Integer newFunds){
        this.funds = newFunds;
    }

}































public class money extends Thread{
    static HashMap<String, Integer> banks = new HashMap<>();
    static HashMap<String, Integer> customers = new HashMap<>();
    static HashMap<String, Bank> bankObject = new HashMap<>();
    static ArrayList<String> finalMessages = new ArrayList<>();
    static ArrayList<Thread> customerThreads = new ArrayList<>();
    static ArrayList<Thread> bankThreads = new ArrayList<>();
    static Thread mainThread;



    public static synchronized void printMessage(String Message){
        System.out.println(Message);
    }

    public static synchronized void addFinalMessage(String Message){
        finalMessages.add(Message);
    }

    public synchronized void printFinalMessages(){
        for (String finalMessage : finalMessages){
            System.out.println(finalMessage);
        }
    }

    public static void readFiles() throws Exception {
        FileReader customerFile = new FileReader("src/customers.txt");
        FileReader bankFile = new FileReader("src/banks.txt");
        BufferedReader reader = new BufferedReader(customerFile);

        System.out.println("\n ** Customers and loan objectives ** \n");
        String line = reader.readLine();
        while(line != null)
        {
            line = line.replace("{", "");
            line = line.replace("}", "");
            line = line.replace(".", "");
            String[] tempLine = line.split(",");
            customers.put(tempLine[0],Integer.parseInt(tempLine[1]));
            System.out.println(line.replace(",",": "));
            line = reader.readLine();

        }

        reader = new BufferedReader(bankFile);
        System.out.println("\n ** Banks and financial resources ** \n");
        line = reader.readLine();
        while(line != null)
        {
            line = line.replace("{", "");
            line = line.replace("}", "");
            line = line.replace(".", "");
            String[] tempLine = line.split(",");
            banks.put(tempLine[0],Integer.parseInt(tempLine[1]));
            System.out.println(line.replace(",",": "));
            line = reader.readLine();

        }
        System.out.println("\n\n");
        reader.close();


    }


    public static void main (String args[]) throws InterruptedException {

        try{
            readFiles();
            new money().start();
        } catch (Exception e){
            e.printStackTrace();
        }

    }

    @Override
    public void run() {
        for (Map.Entry<String, Integer> entry : banks.entrySet()){
            Bank bank = new Bank(entry.getKey(), entry.getValue());
            bankObject.put(entry.getKey(), bank);
            bankThreads.add(bank.thread);

        }

        for (Map.Entry<String, Integer> entry : customers.entrySet()){
            Customer customer = new Customer(entry.getKey(), entry.getValue(), bankObject);
            customerThreads.add(customer.thread);
        }



        for (Thread t : customerThreads){
            try {
                t.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        for (Thread t : bankThreads)
        {
            try {
                t.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        printFinalMessages();

    }
}
