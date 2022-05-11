'''
Created on 25 mars 2020
This program takes as argument a csv file grouping several client sessions
It produces the csv files corresponding to each individual client session.
Example:

ProjectionCSV.py ../traces/otherTraces/1026-steps.csv

The resulting files are stored in directory
../traces/otherTraces/projectedTraces/1026-steps

The script is inefficient because it reads the full trace for each client.
A better script with linear complexity is possible.
@author: ledru
License: MIT
'''
import sys
import os
import csv

def main():
    nb=GenerateCSVProjections(sys.argv[1]) 
    print(str(nb)+" testcases were generated.")   

def GenerateCSVProjections(filePath):
    (targetDir,shortname,extension)=CreateOutputDir(filePath)
    with open(filePath,'r') as csv_file:
        MyReader = csv.reader(csv_file, delimiter=',', quotechar='|')
    # builds the list of client numbers    
        clientList = GetClientNbs(MyReader)
    # For each client, 
        for nb in clientList:
#       select the relevant events build a csv file
            clientData = []
            csv_file.seek(0) # Resets the reader to start again reading at the start of the file
            for rec in MyReader:
                if (rec[2]).strip() == "client"+str(nb) :
                    clientData.append(rec)
            #       save as a csv file
            targetFile = os.path.join(targetDir,shortname+'-Client'+str(nb)+extension)
            SaveCSVTrace(targetFile,clientData)
    return len(clientList)
        
def GetClientNbs(my_reader):
    ClientNbsList = []
    for rec in my_reader:
        clientName = (rec[2]).strip()
        clientNb = clientName[6:]
        if clientNb not in ClientNbsList:
            ClientNbsList.append(clientNb)
    return(ClientNbsList) 


def SaveCSVTrace(outputFilePath,outputClientData):
    with open(outputFilePath,'w',newline='') as csvfile:
        myWriter = csv.writer(csvfile,delimiter=',')
        for line in outputClientData:
             myWriter.writerow(line)

# Creates an output directory whose name and path is projectedTraces/the name of the csv file given as argument
def CreateOutputDir(fpath):
    absDirPath = os.path.abspath(os.path.dirname(fpath))
    (shortFileName, fileExtension) = os.path.splitext(os.path.basename(fpath))
    outputDir=os.path.join(absDirPath,'projectedTraces',shortFileName)
    if not os.path.exists(outputDir):
        print('Creating directory',outputDir)
        os.makedirs(outputDir)
    else :
        print('Directory ',outputDir,'already exists. Proceeding with the existing directory...')
    return (outputDir,shortFileName,fileExtension)

#Main program
if __name__ == '__main__' :
    main()





 