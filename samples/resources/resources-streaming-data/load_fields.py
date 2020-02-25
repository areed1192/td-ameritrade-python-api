import win32com.client as win32
import pprint
import json

xlApp = win32.GetActiveObject("Excel.Application")
xlBook = xlApp.Workbooks("Stream_Table.xlsx")
xlSheet = xlBook.Worksheets("Response_CSV_Writer")
xlTable = xlSheet.ListObjects(1)

xlUpper = xlTable.ListColumns("Endpoint_Upper").DataBodyRange
xlConve = xlTable.ListColumns("Field_Name_NoSpace").DataBodyRange
xlField = xlTable.ListColumns("Field_ID").DataBodyRange

fields_conv = {}

for index, xlCell in enumerate(xlUpper):
    if xlCell.Value not in fields_conv.keys():
        fields_conv[xlCell.Value] = {}
    else:
        if isinstance(xlField[index - 1].Value, float):
            key = str(int(xlField[index - 1].Value))
        else:
            key = xlField[index - 1].Value

        fields_conv[xlCell.Value][key] = xlConve[index - 1].Value

pprint.pprint(fields_conv)

with open("fields_conv.json","w") as infile:
    json.dump(fields_conv, infile)