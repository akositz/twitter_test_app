#import requests

#test = requests.get('http://www.example.com')

#print(test.content)


from user import User
from database import Database

Database.initialise(database="learning", host="localhost", user="postgres", password="andi")

my_user = User('h20.g@tirol.com', 'H14', 'G14', None)
my_user.save_to_db()

user_from_db = User.load_from_db_by_email('h20.g@tirol.com')
print(user_from_db)

# my_user = User('h10.g@tirol.com', 'H7', 'G7', None)

# my_user.save_to_db()

#What we have learnd!
#with statement
#tuples!!!
#private variables
#passing keyword arguments **kwargs
#connection pooling
#rollback!