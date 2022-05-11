'''
Created on 23 mars 2020
This program plays all csv traces of the directory given as argument
against the reference implementation of the scanette and on the 49 mutants.
The argument may also be a single csv file.

This program must be executed in a directory which includes the "resources" subdirectory.

It can be run in optimized mode, which means that once a mutant is killed, the remaining test
cases will skip this mutant. When played in non-optimized mode, all test cases (i.e. csv files)
are played against all mutants.

@author: ledru
License: MIT
'''
import os 
import sys
import time

# *** Configuration variables, set up by the user ***
# Maybe these global variables should be exported to a config.py file...
# The jars are located in the directory absolutePath and listed in otherJarsNames
# AbsolutePath must be adapted to the local configuration
absolutePath = "C:/Users/ledru/workspaces/Eclipse2019Philae/datasets/scanette/replay/"
#We make the hypothesis that the jar with scanette is located at directory absolutePath. This can be changed.
scanetteJarPath = absolutePath
# List of jars that must be in the class path (with scanette.jar or the mutant jar
otherJarsNames = ["../lib/ScanetteTestReplay.jar","../lib/json-simple.jar","../lib/junit-4.12.jar"]

#Main program
def main():
    optimizedMode = True

    dir2Xplore=GetDir2Explore()
    executeTraceOnMutants(dir2Xplore,optimizedMode)
    
#Returns the first argument or '.' if the first argument is missing
def GetDir2Explore():
    result = "."
    if (len(sys.argv) > 1) :
        result = sys.argv[1]
    return result

# Returns a list of csvFiles located at filePath
# filePath maybe a directory of a csv file
def GetListOfCSVfiles(filePath):
    if os.path.isfile(filePath)  and filePath.endswith(".csv"):
        #The parameter corresponds to a single csv file
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
        print('No csv file at location: '+filePath)
    return result
    
#computes the character corresponding to the code   
def retChar(returnCode): 
    if returnCode == 0:
        rc = "."
    elif returnCode == 1:
        rc = "F"
    elif returnCode == -1:
        rc = "X"
    else:
        rc = "?"
        print("The java program return code was not 0, 1 or -1. This may reveal a problem while invoking Java. Maybe the absolutePath variable should be modified.")
    return rc

#prints a line with the 49 statuses of mutants
def printMutantsStatus(mutantsStat):
    print("Mutants status:     ", end= '')
    for i in mutantsStat: print(i, end= '')
    print(" Score: "+str(mutantsStat.count('K')))

def init_timer():
    initial_seconds = time.time() 
    local_time = time.ctime(initial_seconds)
    print("Initial time:", local_time)
    return(initial_seconds)    

def print_current_duration(initial_seconds):
    intermediate_seconds = time.time() 
#    intermediate_time = time.ctime(intermediate_seconds)
    print("Duration : ",intermediate_seconds - initial_seconds)    

def print_current_time_and_duration(initial_seconds):
    current_seconds = time.time() 
    current_time = time.ctime(current_seconds)
    print("Time:", current_time," Duration : ",current_seconds - initial_seconds)    

# osClassPathSep() depends on the os: ":" for linux, ";" for Windows (os.name =='nt')
def osClassPathSep():
    result = ";" 
    if os.name != "nt": #'nt' means 'windows'
        result = ":"
    return result

#executes jar_name on test case csv_file and returns the letter corresponding to the return code
#detailed return messages are stored in resultFile and errorFile
def executeCsvFile(csv_file,jar_name,other_Jars,output_Directory):
    scanetteJar = scanetteJarPath+jar_name
    classpath = other_Jars+scanetteJar
    resultFile = output_Directory+"/result_"+jar_name+".txt"
    errorFile = output_Directory+"/errorFile_"+jar_name+".txt"
    commande = "java -cp "+classpath+" fr.philae.ScanetteTraceExecutor "+csv_file +" > "+resultFile+" 2> "+errorFile
    returnCode = os.system(commande)
    return retChar(returnCode)

#Main function : plays the csv files on all mutants
def executeTraceOnMutants(dir2Explore,optiMode):
    #Initialize timer, shared classpath entries, results directory 
    initial_sec=init_timer()
    otherJars=""
    for jj in otherJarsNames:
        otherJars+=absolutePath+jj+osClassPathSep() # otherJars is a list of jars ended by ";" (or ":" under linux)

    outputDir="results"
    if not os.path.exists(outputDir):
        print('Creating directory',outputDir)
        os.makedirs(outputDir)
    else :
        print('Directory ',outputDir,'already exists. Proceeding with the existing directory')

    #Mutant status takes value a for 'alive' and 'K' for 'Killed'
    #The element at index 0 is empty (first mutant is at index 1
    mutantsStatus = [' ']+['a' for i in range(1,50)]
    printMutantsStatus(mutantsStatus)
    print()

    fileProcessed = 0
    for csvFile in GetListOfCSVfiles(dir2Explore) :
        (fpath, fName) = os.path.split(csvFile)
        fileProcessed += 1
        print("Processing "+str(fileProcessed)+"th CSV file ",fName)
        # Execute the correct program
        returnChar = executeCsvFile(csvFile,"scanette.jar",otherJars,outputDir)
        # The retCharList is a list whose first element is the return char of the correct program 
        #  and the next ones correspond to the return char of the mutants
        retCharList = [returnChar]         
        # Execute the mutants   
        for ii in range(1,50):
            if (mutantsStatus[ii]=='a') or not optiMode: # Only try to kill the alive mutants in optimized mode
                returnChar = executeCsvFile(csvFile,"scanette-mu"+str(ii)+".jar",otherJars,outputDir)
                retCharList = retCharList+[returnChar]
                    #Check if mutant killed
                if returnChar != retCharList[0] :
                    mutantsStatus[ii]='K'
            else:
                retCharList = retCharList+['-']
        #Print results of the current csv file        
        print("Correct Program : "+retCharList[0]+"  ", end= '')
        for i in retCharList[1:50]: print(i, end= '')
        print()
        printMutantsStatus(mutantsStatus)
        print_current_duration(initial_sec)
        print()
    #final result
    print("Score : "+str(mutantsStatus.count('K'))+" mutants killed for path "+GetDir2Explore())
    print_current_time_and_duration(initial_sec)

#Main program
if __name__ == '__main__' :
    main()
