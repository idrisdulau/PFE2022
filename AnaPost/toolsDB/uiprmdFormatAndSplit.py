#------------------------------------------------------------------
# Code written by Idris DULAU, Rodin DUHAYON and DUBRASQUET-DUVAL Guillaume.
# For the use of Dr. Marie Beurton-Aimar and Phd. student Kévin Réby.
#------------------------------------------------------------------

import sys
import os
import subprocess
import json

#region 1 : Ensure split rate value consistency
#-----------------------------------------------
splitRate = 0
if len(sys.argv) == 1:
    splitRate = 90
    print("Defaultly chosen 90% split rate")
elif (type(int(sys.argv[1])) != int) or (int(sys.argv[1]) > 99) :
        print('Select an integer value under 100')
        print('Quit processing')
        sys.exit()
else:
    splitRate = int(sys.argv[1])

inputSentence = str("Proceed to split values with " +  str(splitRate) +  "% train and " +  str(100-int(splitRate)) + "% val ? (y/n) : ")

tmp = 1
while(tmp):
    yn = input(inputSentence)

    if(yn == 'N' or yn == 'n'):
        print('Quit processing')
        sys.exit()

    if(yn == 'Y' or yn == 'y'):
        tmp = 0
    
    if tmp != 0:
        print("write either y or n")
#-----------------------------------------------
#endregion

#region 2 : Read filenames through UI-PRMD folders and setup future storage
#-----------------------------------------------
correctdbPath = "../DB/correctPositions/"
corArrListFiles = []
corArrListFiles = os.listdir("./"+correctdbPath)
corArrListFiles.sort() #Sort filenames

incorrectdbPath = "../DB/incorrectPositions/"
incArrListFiles = []
incArrListFiles = os.listdir("./"+incorrectdbPath)
incArrListFiles.sort()

globalFolder = "uiprmd"
subprocess.run(["mkdir", globalFolder]) 

trainFolder = globalFolder+"/uiprmd_train"
subprocess.run(["mkdir", trainFolder]) 

valFolder = globalFolder+"/uiprmd_val"
subprocess.run(["mkdir", valFolder]) 
#-----------------------------------------------
#endregion 

#region 3 : Configuration values 
#-----------------------------------------------
nbJoints = 22

corLabel = "correct"
corLabelIndex = 1 #correct = 1 / incorrect = 0
trainArrLabelNames = []
trainArrLabelData = []

incLabel = "incorrect"
incLabelIndex = 0 #correct = 1 / incorrect = 0
valArrLabelNames = []
valArrLabelData = []
#-----------------------------------------------
#endregion 

#region 4 : For each correctPositions format file, generates a new UI file in json/kinetics format
#-----------------------------------------------
splitCount = 0
for curFileIndex in range (len(corArrListFiles)):
    arrData = [] 
    #-----------------------------------------------
    #Open one file to read in it
    f = open(correctdbPath+corArrListFiles[curFileIndex], "r")

    #For a file, store a string per line
    lines = f.readlines() 

    #Split and crop elements of a line and store in array
    frameIndex = 1
    for lineIndex in range (len(lines)):
        arrOneFrame = lines[lineIndex].split() 
        arrOneFrame_5digits = [] 
        for i in range(len(arrOneFrame)):
            arrOneFrame_5digits.append(arrOneFrame[i][:5]) 

        x = { "frame_index": frameIndex, "skeleton": [{ "pose": arrOneFrame_5digits }]}
        arrData.append(x)
        frameIndex+=1
    #-----------------------------------------------

    #-----------------------------------------------
    #For a file dump the json format in a new file
    final = {"data": arrData, "label": corLabel, "label_index": corLabelIndex}
    z = json.dumps(final)
    new_filename = "UI_"+str(curFileIndex+1)
    new_file = new_filename +".json"
    subprocess.run(["touch", new_file])
    with open(new_file, 'w') as outfile:
        outfile.write(z)
    if(splitCount < splitRate):
        subprocess.run(["mv", new_file, trainFolder])
        splitCount += 1
        #Storage for next step labels file process
        trainArrLabelNames.append(new_filename)
        trainArrLabelData.append({"label": corLabel, "label_index": corLabelIndex})
    else:
        subprocess.run(["mv", new_file, valFolder])
        valArrLabelNames.append(new_filename)
        valArrLabelData.append({"label": corLabel, "label_index": corLabelIndex})

    #-----------------------------------------------
#-----------------------------------------------
#endregion

#region 5 : For each incorrectPositions format file, generates a new UI file in json/kinetics format
#-----------------------------------------------
splitCount = 0
for curFileIndex in range (len(incArrListFiles)):
    arrData = [] 
    #-----------------------------------------------
    #Open one file to read in it
    f = open(incorrectdbPath+incArrListFiles[curFileIndex], "r")

    #For a file, store a string per line
    lines = f.readlines() 

    #Split and crop elements of a line and store in array
    frameIndex = 1
    for lineIndex in range (len(lines)):
        arrOneFrame = lines[lineIndex].split() 
        arrOneFrame_5digits = [] 
        for i in range(len(arrOneFrame)):
            arrOneFrame_5digits.append(arrOneFrame[i][:5]) 

        x = { "frame_index": frameIndex, "skeleton": [{ "pose": arrOneFrame_5digits }]}
        arrData.append(x)
        frameIndex+=1
    #-----------------------------------------------

    #-----------------------------------------------
    #For a file dump the json format in a new file
    final = {"data": arrData, "label": incLabel, "label_index": incLabelIndex}
    z = json.dumps(final)
    new_filename = "UI_"+str(curFileIndex+1+100)
    new_file = new_filename +".json"
    subprocess.run(["touch", new_file])
    with open(new_file, 'w') as outfile:
        outfile.write(z)
    if(splitCount < splitRate):
        subprocess.run(["mv", new_file, trainFolder])
        splitCount += 1
        #Storage for next step labels file process
        trainArrLabelNames.append(new_filename)
        trainArrLabelData.append({"label": incLabel, "label_index": incLabelIndex})
    else:
        subprocess.run(["mv", new_file, valFolder])
        valArrLabelNames.append(new_filename)
        valArrLabelData.append({"label": incLabel, "label_index": incLabelIndex})
    #-----------------------------------------------
#-----------------------------------------------
#endregion

#region 6 : Generate the train label files
#-----------------------------------------------
#Generate the label file
trainLabelFile = "uiprmd_train_label.json"
#Concat dictionnary inside dictionnary
finalDict = {}
for i in range (len(trainArrLabelNames)):
    finalDict = dict(finalDict, **{trainArrLabelNames[i]: trainArrLabelData[i]})

output = json.dumps(finalDict)
with open(globalFolder+"/"+trainLabelFile, 'w') as outfile:
    outfile.write(output)
#-----------------------------------------------
#endregion

#region 7 : Generate the val label files
#-----------------------------------------------
#Generate the label file
valLabelFile = "uiprmd_val_label.json"
#Concat dictionnary inside dictionnary
finalDict = {}
for i in range (len(valArrLabelNames)):
    finalDict = dict(finalDict, **{valArrLabelNames[i]: valArrLabelData[i]})

output = json.dumps(finalDict)
with open(globalFolder+"/"+valLabelFile, 'w') as outfile:
    outfile.write(output)
#-----------------------------------------------
#endregion