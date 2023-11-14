# class TaxiLagbe:
#   def __init__(self,num,area):
#     self.num=num
#     self.area=area
#     self.list1=[]
#     # self.difflist=[]
#     self.tk=0
#   def addPassenger(self,*name_id):
#     # self.list1=[]
#     self.name_id=name_id
#     for i in self.name_id:
#       if (len(self.list1))<4:
#         self.list1.append(i.split("_"))
#       else:
#         print(f"Taxi Full! No more passengers can be added.")
#       difflist=i.split("_")
#       print(f"Dear {difflist[0]}!Welcome to TaxiLagbe.")
#       # print(self.list1)
#   def printDetails(self):
#     print(f"Trip info for Taxi number:{self.num}.\nThis taxi can only cover the {self.area} arae.")
#     print(f"Total passenger:{int(len(self.list1))}\nPassenger lists:")
#     for i in range(len(self.list1)):
#       if(i==len(self.list1)-1):
#         print(self.list1[i][0]) if self.list1[i][0]!=self.list1[i][len(self.list1[i])-1] else print(self.list1[i][0])
#         self.tk+=int(self.list1[i][1])
#         continue
#       print(self.list1[i][0],end=",") if self.list1[i][0]!=self.list1[i][len(self.list1[i])-1] else print(self.list1[i][0])
#       self.tk+=int(self.list1[i][1])
#     print(f"Total collected fare: {self.tk} Taka")
#     # for j in self.list1:
#     #   print(j[0],end=",") if j[0]!=j[len(j)-1] else print(j[0])
#     #   self.tk+=int(j[1])
#     # print(f"Total collected fare: {self.tk} Taka")


# taxi1 = TaxiLagbe('1010-01', 'Dhaka')
# print('-------------------------------')
# taxi1.addPassenger('Walker_100', 'Wood_200','Matt_100')
# taxi1.addPassenger('Wilson_105')
# print('-------------------------------')
# taxi1.printDetails()
# print('-------------------------------')
# taxi1.addPassenger('Karen_200')
# print('-------------------------------')
# taxi1.printDetails()
# print('-------------------------------')
# taxi2 = TaxiLagbe('1010-02', 'Khulna')
# taxi2.addPassenger('Ronald_115', 'Parker_215')
# print('-------------------------------')
# taxi2.printDetails()


# def test(*something):
#     for i in something:
#       print(i)

# test("Air Jordan", 2)


class Shopidify:
  def __init__(self, name = "Guest"):
    self.name = name
    if self.name == "Guest":
      print(f"Welcome to Shopidify")
    else:
      print(f"Welcome {self.name} to Shopidify")
    self.cart = []
    self.count = 0
  def add_to_cart(self, *args):
    if type(args[0]) is str and len(args) == 1:
      self.cart.append(args[0])
      self.cart.append(int(1))
    elif type(args[0]) is str:
      for i in args:
        self.cart.append(i)
    else:
      self.cart += args[0]

  def display_cart(self):
    print(f"Items in the cart for {self.name}: ")
    for i in range(0, len(self.cart)-1, 2):
      print(f"- {self.cart[i]}: {self.cart[i+1]}x")
  def checkout(self):
    print(f"Checkout completed for {self.name}")
    self.count += 1
  def display_history(self):
    print(f"Purchase history for {self.name}:\nTransaction {self.count}:")
    for i in range(0,len(self.cart)-1, 2):
      print(f"- {self.cart[i]}: {self.cart[i+1]}x")
guest_account = Shopidify()
print("1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
john_account = Shopidify("John")
print("2xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
guest_account.add_to_cart("Air Jordan", 2)
print("test")
print(guest_account.cart)
guest_account.add_to_cart("Luffy Action Figure")
guest_account.display_cart()
print("3xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
john_account.add_to_cart(["Chocolate Chip Cookies", 3,"Goku Action Figure",2,"Dumbbells-5kg",2])
john_account.display_cart()
print("4xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
guest_account.add_to_cart("Air Jordan")
guest_account.display_cart()
print("5xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
guest_account.checkout()
print("6xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
guest_account.display_history()
print("7xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
john_account.checkout()
print("8xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
john_account.display_history()
print("9xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
print(john_account.cart)