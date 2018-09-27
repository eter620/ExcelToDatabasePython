from import_excel import ImportExcel
from db_functions import DB
from export_excel import ExportExcel

"""
This program is designed to upload an excel sheet into a database
and print out data from the database into an excel sheet
"""


def main():

    option = ''
    currentDB = input("Enter Database to connect to(If t doesn't exist one will be created):\n")
    connectedDB = DB(currentDB)
    ex = ExportExcel()
    wbToImport = ImportExcel()

    while option != '0':
        print("\n1.Upload Excel File\n2.Create Table and fill with data from Excel Sheet\n"
                    "3.Add new rows to Table using uploaded Excel file\n"
                    "4.Manually add new row to table\n"
                    "5.Display rows in a table\n6.Export table to Excel File\n"
                    "7.Search Database\n8.Delete Row\n"
                    "9.Exit the program")
        option = input("Select option:\n")

        if option == '1':
            print("Please include file extension")
            excelFile = input("Enter Excel File Name:\n")
            wbToImport.changeExcelFile(excelFile)

        elif option == '2':
            if wbToImport.getExcel()!= 0:
                tableName = input("Enter table name:\n")
                col = wbToImport.getColumns()
                rows = wbToImport.getRows()
                connectedDB.createTable(tableName, col)
                connectedDB.addData(tableName, col, rows)
            else:
                print("Please upload an excel file")

        elif option == '3':
            if wbToImport.getExcel() != 0:
                connectedDB.getAllTableNames()
                tableName = input("Enter table name to update:\n")
                col = wbToImport.getColumns()
                rows = wbToImport.getRows()
                connectedDB.addData(tableName, col, rows)
            else:
                print("Please upload an excel file")

        elif option == '4':
            connectedDB.getAllTableNames()
            tableName = input("Enter table to add row to:\n")
            colNames = connectedDB.getTablCol(tableName)
            print(colNames)
            dataToAdd = []
            for col in colNames:
                data = input("Enter data for " + col + ":\n")
                dataToAdd.append(data)
                rowData = [dataToAdd]
            connectedDB.addData(tableName, colNames, rowData)

        elif option == '5':
            connectedDB.getAllTableNames()
            tableName = input("Enter table to display rows:\n")
            connectedDB.displayTableRows(tableName)

        elif option == '6':
            connectedDB.getAllTableNames()
            tableName = input("Enter table export:\n")
            col = connectedDB.getTablCol(tableName)
            rows = connectedDB.getTableRows(tableName)
            ex.createNewWorkBook()
            ex.addColumnsToWorkSheet(col)
            ex.appendData(rows)
            wbName = input("Please enter name of workbook to save:\n")
            ex.saveWorkBook(wbName)

        elif option == '7':
            searchWord = input("Enter word to search for:\n")
            connectedDB.searchAll(searchWord)

        elif option == '8':
            connectedDB.getAllTableNames()
            tableName = input("Enter table name to delete row from:\n")
            connectedDB.displayTableRows(tableName)
            rowToDelete = input("Enter index of row to delete:\n")
            connectedDB.deleteRow(tableName,rowToDelete)
            connectedDB.displayTableRows(tableName)

        elif option == '9':
            print("Good Bye")
            connectedDB.closeDB()
            exit(0)

        else:
            print("Invalid option")


main()
