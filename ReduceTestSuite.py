'''
Created on 30 mars 2020

Takes as input a directory with test cases stored in individual csv files, an abstract function, and a boolean to take subsumption into account.
The abstract function is given as the 2nd argument. By default, it is OpNames_Set. By default, subsumption is False.

It uses the abstract function to group csv files in clusters, and chooses one test case per cluster.

It displays the copy commands that are executed to copy the selected test case to the directory reducedTS-name of abstract function

Example:

ReduceTestSuite.py ../traces/otherTraces/projectedTraces/1026-steps OpNames_Seq_NoSt

it computes 11 clusters, creates directory reducedTS-OpNames_Seq_NoSt and copies the reduced test suite to that directory
If that directory already exists and is not empty, it halts the program and does not copy the reduced test suite.

If subsumption is activated, the clusters which are subsummed by another (larger) one, are deleted. This reduces the number of clusters.

@author: ledru
License: MIT
'''
import os
import sys
import csv
import time
from shutil import copy


def main():
    (Dir2Xplore,absFunc) = GetArgs()
    
    ComputeSigDictAndReduce(Dir2Xplore,absFunc,0,"")
    #ComputeSigDictAndReduce(Dir2Xplore,"OpNames_Set",0,"")
    #ComputeSigDictAndReduce(Dir2Xplore,"OpNamesAndRet_Set",0,"")
    #ComputeSigDictAndReduce(Dir2Xplore,"OpNamesAndAbsRet_Set",0,"")
    #ComputeSigDictAndReduce(Dir2Xplore,"OpNames_Bag",0,"")
    #ComputeSigDictAndReduce(Dir2Xplore,"OpNamesAndRet_Bag",0,"")
    #ComputeSigDictAndReduce(Dir2Xplore,"OpNamesAndAbsRet_Bag",0,"")
    #ComputeSigDictAndReduce(Dir2Xplore,"OpNames_Seq",0,"")
    #ComputeSigDictAndReduce(Dir2Xplore,"OpNamesAndRet_Seq",0,"")
    #ComputeSigDictAndReduce(Dir2Xplore,"OpNamesAndAbsRet_Seq",0,"")
    #ComputeSigDictAndReduce(Dir2Xplore,"OpNames_Seq_NoSt",0,"")
    #ComputeSigDictAndReduce(Dir2Xplore,"OpNamesAndRet_Seq_NoSt",0,"")
    #ComputeSigDictAndReduce(Dir2Xplore,"OpNamesAndAbsRet_Seq_NoSt",0,"")

def ComputeSigDictAndReduce(dir2Reduce,absFunction,subsumption,my_outputDir):
    local_time = time.ctime(time.time())
    print(str(local_time)+" Computing signatures with abstract function "+absFunction+" ...")
    (ListOfCSVFiles,absDirPath)=GetListOfCSVfiles(dir2Reduce)
    sigDict = BuildSigDict(ListOfCSVFiles,absFunction)
    
    intermediate_time = time.ctime(time.time())
    print(str(intermediate_time)+" Building Clusters...")
    if subsumption>0 :
        subSumptionFunction = findSubsumption(absFunction,subsumption)
    else:
        subSumptionFunction = NoSub 
    cl=BuildClusters(sigDict,subSumptionFunction)    
    print(str(intermediate_time)+" Reducing testsuite.")
    # If the user does not define an output dir, the default is absDirPath/reducedTS
    if subsumption==1:
        subsumptionString= "_sub"
    elif subsumption==2:
        subsumptionString= "_su2"
    else:
        subsumptionString= ""
    if my_outputDir=="":
        outputDir=os.path.join(absDirPath,"reducedTS-"+absFunction+subsumptionString)
    res=CreateOutputDir(outputDir)
    if res=="OK":
        ReduceTestSuite(cl,absDirPath,outputDir)  
    else :
        print(res)  
    final_time = time.ctime(time.time())
    print(final_time)
    return res

#Returns the first argument or '.' if the first argument is missing
def GetArgs():
    result = "."
    absFunction = "OpNames_Set"
    if (len(sys.argv) > 1):
        result = sys.argv[1]
    if (len(sys.argv) > 2):
        absFunction = sys.argv[2]
    return (result,absFunction)

# Returns a list of csvFiles located at filePath
# filePath maybe a directory of a csv file
def GetListOfCSVfiles(filePath):
    if os.path.isfile(filePath)  and filePath.endswith(".csv"):
        #The parameter corresponds to a single csv file
        result=[filePath]
        absDirPath=os.path.abspath(os.path.dirname(filePath))
    elif os.path.isdir(filePath):
        listOfFiles=os.listdir(filePath)
        result=[]
        absDirPath = os.path.abspath(filePath)
        for ff in listOfFiles:
            csvpath = os.path.join(filePath,ff)
            if os.path.isfile(csvpath) and ff.endswith(".csv"):
                result = result+[csvpath]
    else:
        result = []
        absDirPath = ""
    if result==[]:
        print('No csv file at location: '+filePath)
    return (result,absDirPath)

# returns the set of operation names 
# for a given csv file
# The set is transformed into a sorted list.
def GetOpNames(my_reader):
    listOfNames = [(evt[4]).strip() for evt in my_reader]
    listOfNames = list(set(listOfNames))
    listOfNames.sort()
    return listOfNames  

# returns the set of operation names and return results
# for a given csv file
# The set is transformed into a sorted list.
def GetOpNamesAndReturn(my_reader):
    listOfNames = [(evt[4]).strip()+(str(evt[6])).strip() for evt in my_reader]
    listOfNames = list(set(listOfNames))
    listOfNames.sort()
    return listOfNames  

def abstractReturn (resultOfEvt):
    try:
        if float(resultOfEvt)>0:
            res = '>0'
        elif float(resultOfEvt)<0:
            res = '<0'
        else:
            res = '=0'
    except ValueError:
        res = '**'
    return res

# returns the set of operation names and an abstraction of the return results
# for a given csv file
# The set is transformed into a sorted list.
def GetOpNamesAndAbstractReturn(my_reader):
    listOfNames = [(evt[4]).strip()+abstractReturn((str(evt[6])).strip()) for evt in my_reader]
    listOfNames = list(set(listOfNames))
    listOfNames.sort()
    return listOfNames  

# returns the bag of operation names
# for a given csv file
def GetOpNamesBag(my_reader):
    listOfNames = [(evt[4]).strip() for evt in my_reader]
    listOfNames.sort()
    return listOfNames 

# returns the bag of operation names and abstract return results
# for a given csv file
def GetOpNamesAndReturnBag(my_reader):
    listOfNames = [(evt[4]).strip()+(str(evt[6])).strip() for evt in my_reader]
    listOfNames.sort()
    return listOfNames 

# returns the bag of operation names and return results
# for a given csv file
def GetOpNamesAndAbstractReturnBag(my_reader):
    listOfNames = [(evt[4]).strip()+abstractReturn((str(evt[6])).strip()) for evt in my_reader]
    listOfNames.sort()
    return listOfNames 


# returns the sequence of operation names
# for a given csv file
def GetOpNamesSequence(my_reader):
    listOfNames = [(evt[4]).strip() for evt in my_reader]
    return listOfNames 

# returns the set of operation names and return results
# for a given csv file
def GetOpNamesAndReturnSequence(my_reader):
    listOfNames = [(evt[4]).strip()+(str(evt[6])).strip() for evt in my_reader]
    return listOfNames 

# returns the set of operation names and return results
# for a given csv file
def GetOpNamesAndAbstractReturnSequence(my_reader):
    listOfNames = [(evt[4]).strip()+abstractReturn((str(evt[6])).strip()) for evt in my_reader]
    return listOfNames 

# This function must be combined with one of the above functions which return a sequence
# Given a sequence, removes consecutive replicates
# [ 'a', 'b', 'b', 'b', 'a', 'a'] gives [ 'a', 'b', 'a']
def RemoveConsecutiveReplicates(myList):
    result = []
    previous = ""
    for i in myList:
        if i != previous:
            result.append(i)
            previous = i            
    return result

# returns True if pref is a prefix of seq
def prefix(my_pref,my_seq):
    if len(my_pref) > len(my_seq):
        return False
    result = True
    i = 0
    while i<len(my_pref) and result==True :
        result = result and (my_pref[i]==my_seq[i])
        i+=1
    return result

# returns True if my_shortseq can be found in my_seq after deleting some of its elements
# e.g. [B,C,E] is matched by [A,B,C,D,E,F] because the elements of the short sequence appear in the same order in the big sequence
def matchedBy(my_shortseq,my_seq):
    result = True
    i=0
    j=0
    while i<len(my_shortseq) and j<len(my_seq):
        if my_shortseq[i]==my_seq[j]:
            i+=1
            j+=1
        else : 
            j+=1
    if i==len(my_shortseq):
        result = True
    else :
        result = False
    return result


# returns True if my_sub is a subset of my_set
def subset(my_sub,my_set):
    result = True
    for i in my_sub:
        if i not in my_set:
            result = False
    return result

# returns True if my_sub is a subbag of my_bag, i.e. all elements of the first bag are included in the second one.
# bags are represented by sorted lists with repetition of elements
def subbag(my_sub,my_bag):
    result = True
    i=0
    j=0
    while i<len(my_sub) and j<len(my_bag) and result==True:
        if my_sub[i]==my_bag[j]:
            i+=1
            j+=1
        elif my_sub[i]>my_bag[j]:
            j+=1
        elif my_sub[i]<my_bag[j]:
            result=False
    if j==len(my_bag) and i<len(my_sub):
        result=False
    return result

# Function which always returns False; i.e. the subsumption relation is empty
def NoSub(my_sub,my_bag):
    return False

def ComputeSig(my_reader,absFunction):
    if absFunction == "OpNames_Set":
        sigResult = GetOpNames(my_reader)
    elif absFunction == "OpNamesAndRet_Set":
        sigResult = GetOpNamesAndReturn(my_reader)
    elif absFunction == "OpNamesAndAbsRet_Set":
        sigResult = GetOpNamesAndAbstractReturn(my_reader)
    elif absFunction == "OpNames_Bag":
        sigResult = GetOpNamesBag(my_reader)
    elif absFunction == "OpNamesAndRet_Bag":
        sigResult = GetOpNamesAndReturnBag(my_reader)
    elif absFunction == "OpNamesAndAbsRet_Bag":
        sigResult = GetOpNamesAndAbstractReturnBag(my_reader)
    elif absFunction == "OpNames_Seq":
        sigResult = GetOpNamesSequence(my_reader)
    elif absFunction == "OpNamesAndRet_Seq":
        sigResult = GetOpNamesAndReturnSequence(my_reader)
    elif absFunction == "OpNamesAndAbsRet_Seq":
        sigResult = GetOpNamesAndAbstractReturnSequence(my_reader)
    elif absFunction == "OpNames_Seq_NoSt":
        sigResult = GetOpNamesSequence(my_reader)
        sigResult = RemoveConsecutiveReplicates(sigResult)
    elif absFunction == "OpNamesAndRet_Seq_NoSt":
        sigResult = GetOpNamesAndReturnSequence(my_reader)
        sigResult = RemoveConsecutiveReplicates(sigResult)
    elif absFunction == "OpNamesAndAbsRet_Seq_NoSt":
        sigResult = GetOpNamesAndAbstractReturnSequence(my_reader)
        sigResult = RemoveConsecutiveReplicates(sigResult)
    else:
        print("Unknown abstraction function!")
        sigResult = []
    return (sigResult)

def findSubsumption(absFunction,subsume):
    if absFunction == "OpNames_Set":
        subFunction = subset
    elif absFunction == "OpNamesAndRet_Set":
        subFunction = subset
    elif absFunction == "OpNamesAndAbsRet_Set":
        subFunction = subset
    elif absFunction == "OpNames_Bag":
        subFunction = subbag
    elif absFunction == "OpNamesAndRet_Bag":
        subFunction = subbag
    elif absFunction == "OpNamesAndAbsRet_Bag":
        subFunction = subbag
    elif absFunction == "OpNames_Seq":
        if subsume==2:
            subFunction = matchedBy
        else:
            subFunction = prefix
    elif absFunction == "OpNamesAndRet_Seq":
        if subsume==2:
            subFunction = matchedBy
        else:
            subFunction = prefix
    elif absFunction == "OpNamesAndAbsRet_Seq":
        if subsume==2:
            subFunction = matchedBy
        else:
            subFunction = prefix
    elif absFunction == "OpNames_Seq_NoSt":
        if subsume==2:
            subFunction = matchedBy
        else:
            subFunction = prefix
    elif absFunction == "OpNamesAndRet_Seq_NoSt":
        if subsume==2:
            subFunction = matchedBy
        else:
            subFunction = prefix
    elif absFunction == "OpNamesAndAbsRet_Seq_NoSt":
        if subsume==2:
            subFunction = matchedBy
        else:
            subFunction = prefix
    else:
        print("Unknown abstraction function!")
        subFunction = NoSub
    return (subFunction)


# builds a mapping between test cases (csv files) and signatures
def BuildSigDict(ListOfCSVFiles,absFunction):
    mySigDict={}
    for ff in ListOfCSVFiles:
        (shortFileName, fileExtension) = os.path.splitext(os.path.basename(ff))
        with open(ff,'r') as csv_file:
            MyReader = csv.reader(csv_file, delimiter=',', quotechar='|')
            # builds the list of operations  
            signature=ComputeSig(MyReader,absFunction)
            mySigDict[shortFileName]=signature
    print()
    print()
    return (mySigDict)

# build the range of mySigDict (the list of different signatures)
# each if these values corresponds to a new cluster.
#The range is sorted (which makes it easier to compare with the result of other clusterings)
def BuildValSetasList(mySigDict):
    valSetasList=[]
    for j in mySigDict.values():
        if j not in valSetasList:  
            valSetasList.append(j)
    print("Number of clusters : "+str(len(valSetasList)))
    valSetasList.sort()
    return(valSetasList)

# use the mapping to construct the clusters and choose one test case per cluster.
def BuildClusters(mySigDict,subsumedBy):
    # Extract the range of mySigDict, which corresponds to the set of clusters signatures 
    valSetasList = BuildValSetasList(mySigDict)
    # perform additional modifications of valSetasList
    i=0
    
    while i<len(valSetasList):
        j=i+1
        while j<len(valSetasList):
        
            if subsumedBy(valSetasList[j],valSetasList[i]):
                #j is a subset of i so j should be deleted from the list
                #j does not change its value but now points to the next element of the list
                valSetasList.pop(j)
            
            elif subsumedBy(valSetasList[i],valSetasList[j]):
                #i is a subset of j, so i should be deleted, and j reset to i+1
                # the value of i does not change but now points to the next element of the list
                valSetasList.pop(i)
                j=i+1
            else:
                #neither i nor j is a subset of the other; j should be incremented
                j=j+1
        #j has reached the end of the list, the next i should be explored
        i=i+1
    print("Number of clusters after subsumption: "+str(len(valSetasList)))
    
        
    #build "clusters", the inverse mapping of valSetasList, as a list of tuples (cluster,list of test cases)
    #and print his mapping
    clusters=[]
    for val in valSetasList:
        testCases = [k for k,v in mySigDict.items() if v == val]
        clusters.append((val,testCases))
        print(val)
        print(testCases)
    print()
    #print the abstractions, i.e. the signatures of the clusters
    print("Signatures of clusters")
    for val in valSetasList:
        print(val)
    # print the results
    print("Number of clusters : "+str(len(valSetasList)))
    return(clusters)

# Creates an output directory if it does not already exist
def CreateOutputDir(outputDir):
    result = "OK"
    if not os.path.exists(outputDir):
        print('Creating directory',outputDir)
        os.makedirs(outputDir)
    else :
        print('Directory ',outputDir,'already exists. Proceeding with the existing directory.Checking if it is empty...')
        if len(os.listdir(outputDir))>0:
            print ("Directory is not empty. Halting the program! No reduced test suite was saved.")
            result = "Directory not empty!"
    return result

def ReduceTestSuite(clusters,absDirPath,outputDir):    
    # pick the first test case of each cluster (cl[1][0]) and generate the copy command
    for cl in clusters:
        fpath=os.path.join(absDirPath,cl[1][0])
        print("copy "+fpath+".csv "+outputDir) 
        copy(fpath+".csv",outputDir)
    print()
    # print the number of clusters a second time because the first one might be out of screen
    print("Number of test cases : "+str(len(clusters)))
    
    
#Main program
if __name__ == '__main__' :
    main()
