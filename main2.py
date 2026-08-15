#   include in bank management system 
#  1) Bank Account
#  2) deposit money
#  3) withdraw money
#  4) details 
#  5) update details 
#  6) delete account 

#  ab ham ek jsonn - (javascript object notation) file ko create karrenge ki jab bhi hamara system band ho toh joh details h vo gayab na ho jaye vo details kahi pe save rahe 

#  iss data. json file ka path pata honna chahiye kyuki yham isko baar baar access karenge issiliye path ko import kiya hai 

#  ab hame ek dummy data create krma pdega jisse koi bhi update karna ho toh hame apnne mainn data mein naa jaana pde .. tohh ham saare change apne dummy data pe krengee ab jab finally saare updates ho jayenge tab ham isko update kardenge apne json file mein 

# json meinn objects key-value pair ki form meinn create hote hai aur dictionay mein bhi key-value pair hota hai



# import json
# import random
# import string
# from pathlib import Path


# class Bank:
#     database = 'data.json'
#     data = []

#     def __init__(self):
#         try:
#             if Path(Bank.database).exists():
#                 with open(Bank.database) as fs:
#                     Bank.data = json.loads(fs.read())
#             else:
#                 print("No such file exists")
#         except Exception as err:
#             print(f"an execption occured as {err}")

#     @classmethod
#     def __update(cls):
#         with open(cls.database, 'w') as fs:
#             fs.write(json.dumps(Bank.data))

#     @classmethod
#     def __accountgenerate(cls):
#         # k=  yehh value hoti hai random generation ki  kitne apko chahiye 
#         alpha=random.choices(string.ascii_letters,k=3)
#         num= random.choices(string.digits,k=3)
#         spchar = random.choices("!@#$%^&*", k = 3)
#         id = alpha+num+spchar
#         random.shuffle(id)
#         return "".join(id)
 

#     def Createaccount(self):
#         info = {
#             "name": input("tell your account holder name:- "),
#             "age": int(input("tell your age:- ")),
#             "email" : input("tell your email:- "),
#             "pin" : int(input("tell your 4 number pin :- ")),
#             "account" : Bank.__accountgenerate(),
#             "balance": 0
#         }

#         if info['age'] < 18 or len(str(info['pin']))!= 4:
#             print("Sorry you cannot create your account")
#         else:
#             print("Account has been created successfully")
#             for i in info:
#                 print(f"{i} : {info[i]}")
#             print("Please note down your account number ")
#             Bank.data.append(info)
            
#             Bank.__update()
#     #  iss updatee function kaam hai ki joh bhi data hamne create kiya hai jsonn ke andar usko yeh updatee kar dega json ke andar 


# #  money deposite karne ke liye hame  acc no, pin yehh sb dena hoga    
#     def Depositemoney(self):
#       accnum= input("tell your account number:- ")
#       pinn= int(input("tell your account pin:- "))


#       userdata = [i for i in Bank.data if i['account'] == accnum and i['pin'] == pinn]

#       if userdata== False:
#           print("Sorry No Data Found")
#       else:
#           amount= int(input("how much you want to deposit:- "))
#           if amount> 10000 or amount < 0:
#               print(" sorry the amount is too much you can deposit below 10000 and above 0")

#           else:
#             #  print(userdata)
#              userdata[0]['balance'] += amount 
#              Bank.__update()
#              print("Amount deposited successfully")


          



#     def Withdrawmoney(self):
#       accnum= input("tell your account number:- ")
#       pinn= int(input("tell your account pin:- "))


#       userdata = [i for i in Bank.data if i['account'] == accnum and i['pin'] == pinn]

#       if userdata== False:
#           print("Sorry No Data Found")
#       else:
#           amount= int(input("how much you want to withdraw:- "))
#           if userdata[0]['balance'] < amount:
#               print("Sorry you don't have that much money ")

#           else:
#             #  print(userdata)
#              userdata[0]['balance'] -= amount 
#              Bank.__update()
#              print("Amount withdrawll is successfull")


          
#     def showdetails(self):
#         accnum= input("tell your account number:- ")
#         pinn= int(input("tell your account pin:- "))

#         userdata = [i for i in Bank.data if i['account'] == accnum and i['pin'] == pinn]
#         print("Your information arre:- \n\n\n")

#         # print(userdata)

#         for i in userdata[0]:
#             print(f"{i}:{userdata[0][i]}")
        

# #  update = name,email,pin filhal yhi 3 chizze updatee ho skti haii 
#     def updatedetails(self):
#         accnum= input("tell your account number:- ")
#         pinn= int(input("tell your account pin:- "))
        
#         userdata = [i for i in Bank.data if i['account'] == accnum and i['pin'] == pinn]

#         #  ab ham ek aur naya dummy data create karnge jismein ham user se puchnege ki tm kya kya change karna chah rrhe ho aur agr nahi karna chah reh kuchh change toh sidhe hame dedo 


#         if userdata == False:
#             print("No such user found")
#         else:
#             print("You cannot change the age,account number and balance")
#             print("fill the details for change or leave it empty if no change  ")

#             newdata= {
#                 "name" : input("please tell new account holder name or press enter  :- "),
#                 "email": input("please tell your new email or press enter :-"),
#                 "pin": input("please enter your new pin or press enter :- ")
#             }

#             if newdata['name']=="":
#                 newdata['name'] = userdata[0]['name']

#             if newdata['email']=="":
#                 newdata['email'] = userdata[0]['email']

#             if newdata['pin']=="":
#                 newdata['pin'] = userdata[0]['pin']


#             newdata['age'] = userdata[0]['age']
#             newdata['account']= userdata[0]['account']
#             newdata['balance']= userdata[0]['balance']

#             if type(newdata['pin'])==str:
#                 newdata['pin']= int(newdata['pin'])

#             for i in newdata:
#                 if newdata[i] == userdata[0][i]:
#                     continue
#                 else:
#                     userdata[0][i] = newdata[i]

#             Bank.__update()
#             print("Details updated successfully")


#     def Deleteaccount(self):
#           accnum= input("tell your account number:- ")
#           pinn= int(input("tell your account pin:- "))
                
#           userdata = [i for i in Bank.data if i['account'] == accnum and i['pin'] == pinn]

#           if userdata== False:
#               print("No such data exists")

#           else:
#               check = input("Press Y if you actually want to delete your account or press N if you don't want to delete ")
#               if check=='n' or check== 'N':
#                   print("bypassed")
#               else:
#                   index = Bank.data.index(userdata[0])
#                   Bank.data.pop(index)

#                   print("Account deleted successfully")
#                   Bank.__update()
            


# user = Bank()  # object that hold power of bank

# print(" Press 1 for Creating an account ")
# print(" Press 2 for Depositing money in the bank")
# print(" Press 3 for Withdrawing money in the bank")
# print(" Press 4  for Details")
# print("Press 5 for Updating Details ")
# print("Press 6 for Deleting Account")


# check = int(input("Tell your respose:- "))

# if check == 1:
#     user.Createaccount()


# if check == 2:
#    user.Depositemoney()

# if check == 3:
#     user.Withdrawmoney()

# if check == 4:
#     user.showdetails()

# if check == 5:
#     user.updatedetails()

# if check == 6:
#     user.Deleteaccount()




# originnal hand made code 