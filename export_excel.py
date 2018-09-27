import openpyxl
from excel import Excel


"""
This class receives data from the database and inputs it into an excel sheet
Function Descriptions:
createNewWorkBook: creates a new workbook
addColumnsToWorkSheet: Adds the columns to the current sheet
appendData: Adds data to the end of the current excel sheet
saveWorkBook: saves the current workbook

"""


class ExportExcel(Excel):

    """
 initializes the work book and work sheet to 0
    """
    def __init__(self):
        super(ExportExcel,self).__init__()

    """
    creates a new workbook and sets the work sheet to the active tab
    """
    def createNewWorkBook(self):
        self._wb = openpyxl.Workbook()
        self._ws = self._wb.active

    """
    creates the columns from colNames
    colNames must be a list
    Over wrights the 1st row in order to preserve styles
    """
    def addColumnsToWorkSheet(self,colNames):
        count = 1
        for col in colNames:

            self._ws.cell(row= 1, column = count).value = col

            count += 1

    """
    Adds data to the end of the current sheet 

    """
    def appendData(self,rowData):
        for row in rowData:
            self._ws.append(row)

    """
    saves the current work book as the name passed in
    checks to see if file type was added ands it if it is missing
    """
    def saveWorkBook(self, wbName):

        fileExt = ".xlsx"

        if wbName.find(fileExt) == -1:


            self._wb.save(wbName + ".xlsx")
        else:

            self._wb.save(wbName)



