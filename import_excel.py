import openpyxl
from excel import Excel
from openpyxl.worksheet.write_only import WriteOnlyCell
import openpyxl.styles

"""
This Class gets and returns information from an excel sheet
Function Descriptions:
getColumns: returns the columns of the active worksheet
getRows: return all the rows in active excel sheet
"""


class ImportExcel(Excel):
    """
    initializes the work book and work sheet to 0
    """
    def __init__(self):
        super(ImportExcel,self).__init__()

    """
    returns the column names of the active excel sheet as a list
    """
    def getColumns(self):
        try:
            tableCol = []
            for row in self._ws.iter_cols(max_row=1):
                for cell in row:
                    tableCol.append(cell.value)
            return tableCol
        except:
            print("An error occurred")

    """
    returns all the rows in an excel sheet as a single list. Each individual row is a tuple.
    """
    def getRows(self):
        try:
            allRows = []
            for row in self._ws.iter_rows(min_row=2):
                tableRow = []
                for cell in row:
                    tableRow.append(cell.value)
                    # turns each row into a tuple because data added to the database must be in the form of a tuple
                rowT = tuple(tableRow)
                allRows.append(rowT) #creates a list of tuples
            return allRows
        except:
            print("An error occurred")





