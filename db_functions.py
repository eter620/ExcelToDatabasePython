import sqlite3
import pandas as pd
import re

"""
This class holds all the functions necessary to interact with the database
Summary of Functions:
createTable: adds a new table to the database
closeDB: Closes the connection to the current database
addData: adds rows of data to a table 
displayTableRows: Displays the rows of a table 
getAllTableNames: Gets the names of each table in the database
getTablCol: Returns the column names for a table  
"""


class DB:

    """
    connects to the database sent to it and creates a new one if it doesn't exist
    sets the cursor to the current database
    """
    def __init__(self, dataBase):
        self.db = sqlite3.connect(dataBase)
        self.cursor = self.db.cursor()

    """
    creates a table using tableName as it's name and colNames being the columns added
    colNames must be a list
    sets up table so each column can be NULL
    """
    def createTable(self,tableName, colNames):
        # creates the sql statement by concatenating sql commands with the strings in the colNames list
        try:
            tableSetup = "CREATE TABLE \"" + tableName + "\" ("

            # automatically sets all columns to text, will change later
            for col in colNames:
                tableSetup += "\"" + col + "\" TEXT,"

            tableSetup = re.sub(r'(.*),', r'\1)', tableSetup) # uses regex to change the last , to a )
            self.cursor.execute(tableSetup) # sends newly created sql command to the database
            self.db.commit() # must be called after any change to the database in order to save the change
        except:
            print("An error occurred createTable")

    """
    closes the database. must use before closing program
    """
    def closeDB(self):
        self.db.close()

    """
    add rows to the table selected by tableName. colNames is each column name
    rowData is all rows to be added
    colNames must be a list and rowData must be a list containing each row as a tuple
    """
    def addData(self, tableName, colNames, rowData):
        #creates the SQL command by con catenating in each column name
         try:
            dataToAdd = "INSERT INTO \"" + tableName + "\" ("

            for col in colNames:
                dataToAdd += "\"" + col + "\" ,"

            dataToAdd = re.sub(r'(.*),', r'\1)', dataToAdd)  # uses regex to change the last , to a )
            dataToAdd += " VALUES ("

            for num in range(len(colNames)):
                dataToAdd += "?," # instead of hard coding in each value to add I use a ? which is the substitution sign

            dataToAdd = re.sub(r'(.*),', r'\1)', dataToAdd)  # uses regex to change the last , to a )

            # because I use a ? where a value is supposed to be the strings in each tuple of rowData are substituted in order
            self.cursor.executemany(dataToAdd, rowData) #executemany is used to add multiple rows at once
            self.db.commit() # must be called after any change to the database in order to save the change
         except:
             print("An error occurred addData")


    """
    prints out all rows in a single table
    """
    def displayTableRows(self,tableName):
        # uses pandas to display the data in a neat format
        print(pd.read_sql_query("SELECT * from ({t})".format(t=tableName), self.db))


    """
    prints out all table names in the database
    """
    def getAllTableNames(self):
        # uses pandas to display the data in a neat format
        print(pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", self.db))

    """
    returns the columns in a table
    """
    def getTablCol(self, tableName):
        colList = []
        try:
            self.cursor.execute("SELECT * FROM {t}".format(t=tableName))
            colNames = self.cursor.description # gets the description for each column
            for col in colNames:
                colList.append(col[0]) # the first string in the description is the name of the column and it is added to a list
            return colList
        except:
            print("An error occurred")


    """
    returns the rows in a table
    """
    def getTableRows(self, tableName):
        found = []
        self.cursor.execute("SELECT * FROM {t}".format(t=tableName))
        for row in self.cursor:
                found.append(row) # adds each row to a list
        return found


    """
    search entire data base and returns each row containing the search word
    """
    def searchAll(self, searchWord):
        search = False
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        for tableRow in self.cursor.fetchall():
            found = []
            colist = []
            table = tableRow[0]
            self.cursor.execute("SELECT * FROM {t}".format(t=table))

            colNames = self.cursor.description
            for col in colNames:
                colist.append(col[0])

            for row in self.cursor:
                if searchWord in row:
                    found.append(row)

            if found != []:
                search = True
                print(table)
                print(pd.DataFrame(found, columns = colist))

        if not search:
            print("\'" + searchWord +"\' not found")
    """
    deletes a row by turning a table into a pandas dataframe then deletes the row by it's index
    and replaces the table in the database with the dataframe
    """
    def deleteRow(self,tableName, id):
        try:

            df = pd.read_sql("select * from {t}".format(t=tableName), self.db)
            df.drop(df.index[int(id)], inplace=True)
            df.to_sql(tableName, self.db, if_exists="replace",index = False)


        except:
            print("An error ocurred")
