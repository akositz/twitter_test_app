from psycopg2 import pool

#the connect takes the longest time!!!!!
#use connection pooling!!!!!
#get connections from the pool (1-10 in the pool), if nothing in the pool anymore, then we create a new one

#def connect():
#    return psycopg2.connect(database="learning", user="postgres", password="andi", host="localhost")

#here we create a pool of connections
class Database:
    __connection_pool = None #not inside the __init__ method, belongs to the class, not one of its objects
    # __ 2 underscores, nobody can it access now!

    #@staticmethod #without self and cls
    @classmethod
    def initialise(cls, **kwargs):
        cls.__connection_pool= pool.SimpleConnectionPool(1,
                                                         10,
                                                         **kwargs)
        #cls.__connection_pool= pool.SimpleConnectionPool(1,10,database="learning",user="postgres",
                                                         #password="andi",host="localhost")
    @classmethod
    def get_connection(cls):
        return cls.__connection_pool.getconn()

    @classmethod
    def return_connection(cls, connection):
        Database.__connection_pool.putconn(connection)

    @classmethod
    def close_all_connections(cls):
        Database.__connection_pool.closeall()

class CursorFromConnectionFromPool: #this is for the with clause!!!!!
    def __init__(self):
        self.connection = None
        self.cursor = None

    def __enter__(self): #we enter the with statement!!!!
        #self.connection = Database.connection_pool.getconn()
        self.connection = Database.get_connection()
        self.cursor = self.connection.cursor()
        return self.cursor


    def __exit__(self, exc_type, exc_value, exc_traceback): #we exit the with clause!
        if exc_value is not None:
            self.connection.rollback()
        else:
            self.cursor.close()
            self.connection.commit()
        #Database.connection_pool.putconn(self.connection) #here we put it back into the pool
        Database.return_connection(self.connection)  # here we put it back into the pool