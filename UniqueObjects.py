'''
Created on 29 avr. 2020
This script takes a csv file, a directory with csv files, or an Agilkia json file..
It modifies the name of "caisse" and "scan" objects in the csv/json file or 
in all csv files of the directory, by adding the number of their session. 
This should avoid interactions between sessions.

When a directory is selected, by default, it puts all the resulting files in separate files.
The GUI or the API allows to put them into a single file.

This (quick and dirty) script only makes sense in the scannette example
(because it refers to "caisse" and "scan" objects.

Improved in May 2021 : now also supports JSON Agilkia input file.
@author: ledru
License: MIT
'''
import os
import sys
from pathlib import Path
import agilkia

def main():
    
   dir2Xplore=GetDir2Explore()
   MakeUniqueObjects(dir2Xplore,False)

#Returns the first argument or '.' if the first argument is missing
def GetDir2Explore():
    result = "."
    if (len(sys.argv) > 1) :
        result = sys.argv[1]
    return result

# Returns a list of csvFiles located at filePath
# filePath maybe a directory or a csv or a JSON file
def GetListOfCSVfiles(filePath):
    if os.path.isfile(filePath)  and filePath.endswith(".csv"):
        #The parameter corresponds to a single csv file
        result=[filePath]
    elif os.path.isfile(filePath)  and filePath.endswith(".json"):
        #The parameter is a single json file
        result=[filePath]
    elif os.path.isdir(filePath):
        # if filePath is a directory, retrieve only the csv files
        listOfFiles=os.listdir(filePath)
        result=[]
        for ff in listOfFiles:
            csvpath = os.path.join(filePath,ff)
            if os.path.isfile(csvpath) and ff.endswith(".csv"):
                result = result+[csvpath]
    else:
        result = []
    if result==[]:
        print('No csv or JSON file at location: '+filePath)
    return result

# The first argument is a single csv file or a directory
# The second argument tells if the result must be put in a single file
# whose name is based on the directory name, or in separate files
# This function does not process json files (which are processed by MakeUniqueObjectsJSON.
def MakeUniqueObjectsCSV(filePath,singleResultFile):
    for csvFile in  GetListOfCSVfiles(filePath):
        f = open(csvFile,'r') # opens the file given as argument.
        if singleResultFile==False:
            absDirPath = os.path.abspath(os.path.dirname(csvFile))
            (shortFileName, fileExtension) = os.path.splitext(os.path.basename(csvFile))
            outputFileName = os.path.join(absDirPath,shortFileName+"-U.csv") #the output file is the input file with suffix -U (for Unique)
        else:
            absDirPath = os.path.abspath(os.path.dirname(csvFile))
            (previousPath, shortName) = os.path.split(absDirPath)
            outputFileName = os.path.join(absDirPath,shortName+"-U.csv") #the output file is in the directory given as parameter and has teh name of the directory followed by -U (Unique)
        g = open(outputFileName,'a') #Open the file in append mode.
        for line in f:
            clientIndx=line.find("client")
            outputLine=line
            if (clientIndx != -1):
                endOfClientNb=line.find(",",clientIndx)
                clientNb=line[(clientIndx+6):endOfClientNb]
                outputLine = outputLine.replace("caisse","caisse"+clientNb+"_") 
                outputLine = outputLine.replace("scanner","canner") # protect string "scanner"
                outputLine = outputLine.replace("scan","scan"+clientNb+"_") 
                outputLine = outputLine.replace("canner","scanner") 

            print(outputLine,end='',file=g)
        f.close()
        g.close()

# The first argument is a single json file (directories are for future work.
# The second argument is not taken into account
def MakeUniqueObjectsJSON(filePath,singleResultFile):
    tr_set = agilkia.TraceSet.load_from_json(Path(filePath))
    for tr in tr_set:
        for evt in tr:
            sessionID=evt.meta_data.get('sessionID', None) 
            object=evt.meta_data.get('object', None)
            clientNb=sessionID[6:]
            object=object.replace("caisse","caisse"+clientNb+"_") 
            object=object.replace("scan","scan"+clientNb+"_") 
            evt.meta_data["object"]=object
    absDirPath = os.path.abspath(os.path.dirname(filePath))
    (shortFileName, fileExtension) = os.path.splitext(os.path.basename(filePath))
    outputFileName = os.path.join(absDirPath,shortFileName+"-U.json") #the output file is the input file with suffix -U (for Unique)
    tr_set.save_to_json(Path(outputFileName))

# If the argument is a csv file or a directoru, we call MakeUniqueObjectsCSV.
# If it is a json file, we call MakeUniqueObjectsJSON
def MakeUniqueObjects(filePath,singleResultFile):
    print("Processing "+filePath)
    if filePath.endswith(".json"):
        MakeUniqueObjectsJSON(filePath, singleResultFile)
    else:
        MakeUniqueObjectsCSV(filePath,singleResultFile)
    print("Done!")

    
#Main program
if __name__ == '__main__' :
    main()
