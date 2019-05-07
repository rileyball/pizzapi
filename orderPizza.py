from pizzapy import *
import re
import os
import sys
import time

#clear method
def clear():
	if sys.platform == "linux" or sys.platform == "posix":
		clearorcls = "clear"
		os.system(clearorcls)
	else:
		clearorcls = "cls"
		os.system(clearorcls)

#Main method
clear()

#Establishing person
name = input("What is your first and last name? ")
firstAndLast = re.split(" ", name)
if len(firstAndLast) == 2:
	wrongFirst = False
while len(firstAndLast) != 2:
	clear()
	wrongFirst = True
	name = input("Put in your first AND last name: ")
	firstAndLast = re.split(" ", name)
email = input("What is your email address? ")
while email.find("@") == -1:
	clear()
	if wrongFirst == False:
		print("What is your first and last name? "+ name)
	else:
		print("Put in your first AND last name: "+ name)
	email = input("Enter a valid address: ")
phone = input("What is your phone number? ")
if phone.find("-") != -1:
	phone = re.sub("-", "", phone)
print("Now I need your address")
address = input("Format as 'street number street name','city','state','zip': ")

cust = Customer(firstAndLast[0],firstAndLast[1],email,phone,address)

#Find closest dominos
closest_Dominos = StoreLocator.find_closest_store_to_customer(cust)
menu = closest_Dominos.get_menu()


print("Thank you! Sending you to menu now")
time.sleep(2.5)

#Create order

clear()
orderInput = input("Type name of the item to search: ")
print(menu.search(Name=orderInput))
orderInput = input("Type code of item to add to your cart! ")
if orderInput != "":
	order = Order.begin_customer_order(cust, closest_Dominos)
	order.add_item(orderInput)
while orderInput != "Done":
	clear()
	orderInput = input("Type name of the item to search or type Done to exit: ")
	if orderInput != "" or orderInput != "Done":
		print(menu.search(Name=orderInput))
		orderInput = input("Type code of item to add to your cart! ")
		if orderInput != "Done":
			order.add_item(orderInput)
	else:
		print("Great! Sending you to credit card info now!")
		time.sleep(2)

clear()
creditNumber = input("What is your credit card number? ")
if creditNumber.find("-") != -1:
	creditNumber = re.sub("-", "", creditNumber)
creditExp = input("What is the expiration date? ")
if creditExp.find("/") != -1:
	creditExp = re.sub("/","", creditExp)

creditCCV = input("What is the CCV on the back? ")

yesno = input("Is the zip on your card the same as your address Y/N: ")
if yesno.upper() == "Y":
	if (address[address.rfind(",")+1]) == " ":
		creditZip = address[address.rfind(",")+2:len(address)]
	else:
		creditZip = address[address.rfind(",")+1:len(address)]
else:
	creditZip = input("Well what is the input then? ")

card = CreditCard(creditNumber,creditExp,creditCCV,creditZip)
yesno = input("Are you sure you would like to place this order? (Y/N) ")
if yesno.upper() == "Y":
	closest_Dominos.place_order(order, card)
else:
	print("Well... goodbye? ")
