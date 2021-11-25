import mysql.connector
from mysql.connector import Error
import pandas as pd
from Assistance_Program_Entity import AssistanceProgramEntity

"""
MySQL wrapper class AssistanceProgramDB
"""


class AssistanceProgramDB:

    def __init__(self):
        self.connection = None

    def run_query_insert_and_create(self, query):
        """
        The function sends a query request that demands a commit call.
        :param query: The query to be sent
        :return: None
        """
        self.connection = self.connect_to_server()
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            print("Query was successful")
            self.connection.close()
            cursor.close()
        except Error as err:
            print(f"Error: '{err}'")
            self.connection.close()
            cursor.close()

    def run_query_select(self, query):
        """
        The function sends a select query request.
        :param query: a select query to be sent
        :return: None
        """
        self.connection = self.connect_to_server()
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            print("Query was successful")
            output = cursor.fetchall()
            self.connection.close()
            cursor.close()
            return output
        except Error as err:
            print(f"Error: '{err}'")
            self.connection.close()
            cursor.close()
            return None

    def connect_to_server(self):
        """
        The function creates a connection to the SQL DB
        :return: The connection
        """
        connection = None
        try:
            connection = mysql.connector.connect(
                host="localhost",  # host name
                user="root",  # your user name
                passwd="password",  # your password
                database="mydatabase"  # your database
            )
        except Error as err:
            print(f"Error: '{err}'")
        return connection

    def create_the_table(self):
        """
        The DB creation. Initialized only once.
        :return: None
        """
        self.run_query_insert_and_create("USE mydatabase")
        self.run_query_insert_and_create("CREATE TABLE assistanceProgram (url VARCHAR(500) PRIMARY KEY, "
                                         "Assistance_Program_name  VARCHAR(255),"
                                         "Eligible_treatments  VARCHAR(1000), status VARCHAR(6), Grant_Amount INT)")

    def delete_table(self):
        """
        The function deletes the DB.
        :return: None
        """
        self.run_query_insert_and_create("DROP TABLE assistanceProgram")

    def retrieve_primary(self):
        """

        :return: The primary keys values currently in the table
        """
        query = "SELECT url FROM assistanceProgram"
        return self.run_query_select(query)

    def write(self, entities):
        """
        The function writes the given Assistance Programs entities to the DB
        :param entities: AssistanceProgramEntity objects
        :return: None
        """
        for entity in entities:
            if not isinstance(entity, AssistanceProgramEntity):
                print(f"wrong entity format of type " + type(entity))
            query = "REPLACE INTO assistanceProgram " \
                    "VALUES('" + entity.url + "','" + entity.name + "','" + entity.eligible_treatments + "','" \
                    + entity.status + "','" + str(entity.grant_amount) + "')"
            self.run_query_insert_and_create(query)

    def retrieve(self, urls):
        """
        The function returns the required entities identified by their website urls
        :param urls: The requested urls
        :return: A list of the requested entities in a AssistanceProgramEntity format
        """
        entities = []
        for name in urls:
            query = "SELECT * FROM assistanceProgram WHERE url = '" + name + "'"
            entity = self.run_query_select(query)
            if not entity:  # the primary key does not exist
                entities.append(None)
            else:
                entities.append(AssistanceProgramEntity(entity[0][0], entity[0][1],
                                                        entity[0][2], entity[0][3], entity[0][4]))
        return entities

    def delete(self, urls):
        """
        The function deletes the required entities identified by their website urls
        :param urls: The requested urls
        :return: None
        """
        for name in urls:
            query = "DELETE FROM assistanceProgram WHERE url = '" + name + "'"
            self.run_query_insert_and_create(query)

    def retrieve_table(self):
        """

        :return: The current DB
        """
        self.connection = self.connect_to_server()
        query = "SELECT * FROM assistanceProgram"
        table = pd.read_sql(query, self.connection)
        self.connection.close()
        return table.iloc[:, 1:]
