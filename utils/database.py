from settings import DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME
import mysql.connector

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class DatabaseUtil(metaclass=Singleton):
    def __init__(self):
        self.host = DATABASE_HOST
        self.username = DATABASE_USER
        self.password = DATABASE_PASSWORD
        self.database = DATABASE_NAME
        self.connection = None

    @classmethod
    def getInstance(cls):
        if cls not in cls._instances:
            cls._instances[cls] = cls()
        return cls._instances[cls]

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database
            )
            print("Database connection successful")
        except mysql.connector.Error as error:
            print(f"Error connecting to database: {error}")


    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            print("Database connection closed")


    def execute_query(self, query, params=None):
        self.connect()
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            self.connection.commit()
            print("Query executed successfully")
            return cursor.rowcount
        except mysql.connector.Error as error:
            print(f"Error executing query: {error}")
        finally:
            cursor.close()
            self.disconnect()

    
    def fetch_data(self, query, params=None):
        self.connect()
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as error:
            print(f"Error fetching data: {error}")
        finally:
            cursor.close()
            self.disconnect()