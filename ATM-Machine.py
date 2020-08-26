#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 22:06:00 2019

@author: ashwinak


(Game: ATM machine) 
Use the Account class created in Exercise 7.3 to simulate an ATM machine. 
Create ten accounts in a list with the ids 0, 1, ..., 9, and an initial balance of $100. 
The system prompts the user to enter an id. If the id is entered incorrectly, ask the user to enter a correct id. 
Once an id is accepted, the main menu is displayed as shown in the sample run. 
You can enter a choice of 1 for viewing the current balance, 2 for withdrawing money, 3 for depositing money, and 4 for exiting the main menu. 
Once you exit, the system will prompt for an id again. So, once the system starts, it won’t stop.

"""

class Account:
    def __init__(self,id=0,balance=100.0,annual_interest_rate=0.0):
        self.__id= id
        self.__balance = balance
        self.__annual_interest_rate = annual_interest_rate
        
    def getID(self):
        return self.__id
    
    def setID(self,id):
        self.__id = id

    def getBalance(self):
        return self.__balance

    def setBalance(self,balance):
        self.__balance = balance

    def getAnnual_Interest_Rate(self):
        return self.__annual_interest_rate

    def setAnnual_Interest_Rate(self,annual_interest_rate):
        self.__annual_interest_rate = annual_interest_rate
    
    def getMonthlyInterestRate(self):
        MonthlyInterestRate = self.__annual_interest_rate / 12
        return MonthlyInterestRate
        
    def getMonthlyInterest(self):
        MonthlyInterest = (self.__annual_interest_rate / 1200) * self.__balance
        return MonthlyInterest
        
    def withdraw(self,withdraw):
        self.__balance = self.__balance - withdraw
                
    def deposit(self,deposit):
        self.__balance = self.__balance + deposit

try:
#    i=0
#    for i in range (0,10):
#        ch = chr(ord('A') + i)
#        ch = Account(i,100)
#        i+=1
    A = Account()        
    ID = eval(input("Enter account ID: "))    
    while True:
        if ID < 10:
            print("")
            print("Main Menu\n")
            print("1: check balance\n")
            print("2: withdraw\n")
            print("3: deposit\n")
            print("4: exit\n")
            choice = eval(input("Enter a choice: "))
            if choice == 1:
                print("\nThe balance is",A.getBalance())
            elif choice == 2:
                w = eval(input("Enter the amount to withdraw: "))
                A.withdraw(w)
                print("The balance is",A.getBalance())
            elif choice == 3:
                d = eval(input("Enter the amount to deposit: "))
                A.deposit(d)
                print("The balance is",A.getBalance())
            else:
                A = Account()
                ID = eval(input("Enter account ID: "))
        else:
            ID = eval(input("Enterr correct account ID between 0 to 9: "))
        
                
except KeyboardInterrupt:
    print("\nThe user Interrupted...")

except TypeError:
    print("TypeError Encountered...")
except:
    print("Error encountered")
