"""
This is a computer program that can read the data from a CSV (comma-separated values)
file provided to it and return different interesting analytical results.
-----------------------
Author: Khanh Hua Quang
Student ID: 22928469
-----------------------
"""

# seperate locId into 2 parts
def getLocId(locId):
    for char in locId:
        if char.isdigit():
            index = locId.index(char)
            return locId[:index].upper(), locId[index:].strip()
    print("Not found locId")
    return None

# handle invalid input, if True then terminate and print out error
def handleInvalidInput(inputFile, queryLocId, radius):
    # invalid input file
    try:
        file = open(inputFile, "r")
    except EOFError:
        print("Invalid inputFile!")
        return True
    except FileNotFoundError:
        print("Invalid inputFile!")
        return True

    # missing header error
    headerPos = header(inputFile)
    locIdPos = headerPos[0]
    if len(headerPos) < 4:
        print("Missing header")
        return True

    # invalid queryLocId input - not 2 queryLocId provided
    if len(queryLocId) != 2:
        print("Invalid queryLocId input! - not 2 queryLocId provided")
        return True

    # invalid queryLocId input - not list type
    if type(queryLocId) != list:
        print("Invalid queryLocId input! - not list type")
        return True

    # invalid queryLocId input - duplicated or missing locId in locList
    for locId in queryLocId:
        count = 0
        for line in readFile(inputFile)[1]:
            if getLocId(locId) == getLocId(line[locIdPos]):
                count += 1
                if count > 1:
                    break
        if count != 1:
            print("Invalid queryLocId input! - duplicated or missing locId")
            return True

    # invalid radius input
    if radius <= 0:
        print("Invalid radius input!")
        return True
    try:
        radius = float(radius)
    except ValueError:
        print("Invalid radius input!")
        return True
    except SyntaxError:
        print("Invalid radius input!")
        return True

# read file and return header list, locList
def readFile(inputFile):
    with open (inputFile, "r") as file:
        header = file.readline().strip("\n").split(",")
        temp = file.readlines()
        locList = []
        for line in temp:
            locList.append(line.strip("\n").split(","))
        
        # process raw data in file - strip spaces and uppercase
        for line in range(len(locList)):
            for item in range(len(locList[line])):
                locList[line][item] = locList[line][item].upper().strip()
    return header, locList

# define header position in case of random header
def header(inputFile):
    header = readFile(inputFile)[0]
    headerPos = []
    headerNameList = ["LOCID", "LATITUDE", "LONGITUDE", "CATEGORY"]
    for headerName in headerNameList:
        for index in range(len(header)):
            if headerName in header[index].upper():
                headerPos.append(index)
    return headerPos

# compare locId input with locId in locList to add x, y, category element of that locId to outputList
def element(locIdInput, inputFile):
    headerPos = header(inputFile)
    locIdPos, xPos, yPos, categoryPos = list(headerPos)
    locList = readFile(inputFile)[1]
    outputList = []

    for line in locList:
        locId = line[locIdPos]
        if getLocId(locIdInput) == getLocId(locId):
            try:
                outputList.append(float(line[xPos]))
                outputList.append(float(line[yPos]))
            except ValueError:
                continue
            outputList.append(line[categoryPos])
    return outputList

# calculate distance using x1, y1, x2, y2
def distance(x1, y1, x2, y2):
    distance = round(((((x2 - x1)**2) + (y2 - y1)**2)) ** (1/2), 4)
    return distance

# determine if locId is in radius or not
def isInRadius(x1, y1, x2, y2, radius):
    return distance(x1, y1, x2, y2) < radius

# determine if locId is duplicated in locList or not
def isDuplicated(locId, inputFile):
    headerPos = header(inputFile)
    locIdPos = headerPos[0]
    locList = readFile(inputFile)[1]
    count = 0
    for line in locList:
        if locId == line[locIdPos]:
            count += 1
            if count > 1:
                return True
    return False

# count locId in radius for each category
def LDCountFunc(inputFile, queryLocId, radius):
    radius = float(radius)
    headerPos = header(inputFile)
    locIdPos, xPos, yPos, categoryPos = list(headerPos)
    locList = readFile(inputFile)[1]

    LDCount = [{}, {}]
    for i in range(2):
        for line in locList:
            if LDCount[i].get(line[categoryPos]) == None:
                LDCount[i][line[categoryPos]] = 0

    locIdDict = [{}, {}]
    for i in range(2):
        for line in locList:
            if locIdDict[i].get(line[categoryPos]) == None:
                locIdDict[i][line[categoryPos]] = []

    for line in locList:
        if isDuplicated(line[locIdPos], inputFile):
            continue
        try:
            x2 = float(line[xPos])
            y2 = float(line[yPos])
        except ValueError:
            continue

        for i in range(len(queryLocId)):
            if len(element(queryLocId[i], inputFile)) == 0:
                continue
            latitude1 = float(element(queryLocId[i], inputFile)[0])
            longitude1 = float(element(queryLocId[i], inputFile)[1])
            if isInRadius(latitude1, longitude1, x2, y2, radius):
                LDCount[i][line[categoryPos]] = LDCount[i].get(line[categoryPos]) + 1
                
                if line[locIdPos] != queryLocId[i]:
                    locIdDict[i][line[categoryPos]].append(line[locIdPos])
    
    return LDCount, locIdDict

# calculate the similarity between A and B
def similarity(A, B):
    listA = list(A.values())
    listB = list(B.values())
    numerator = sum(listA[i] * listB[i] for i in range(len(listA)))
    denominator1 = sum(value * value for value in listA)**(1/2)
    denominator2 = sum(value * value for value in listB)**(1/2)
    try:
        result = round(numerator / (denominator1 * denominator2), 4)
    except ZeroDivisionError:
        print("Error divide by zero")
        return 0
    return result

# return similarity for 2 lists from LDCount
def simScoreFunc(LDCount):
    A = LDCount[0]
    B = LDCount[1]
    return similarity(A, B)

# return a dictionary with locI for each category
def DCommonFunc(inputFile, queryLocId, radius):
    headerPos = header(inputFile)
    locIdPos, xPos, yPos, categoryPos = list(headerPos)
    locList = readFile(inputFile)[1]

    DCommon = {}
    for line in locList:
        if DCommon.get(line[categoryPos]) == None:
            DCommon[line[categoryPos]] = []

    latitude = []
    longitude = []
    for i in range(len(queryLocId)):
        temp = element(queryLocId[i], inputFile)
        latitude.append(float(temp[0]))
        longitude.append(float(temp[1]))

    radius = float(radius)

    for line in locList:
        if isDuplicated(line[locIdPos], inputFile):
            continue
        try:
            x2 = float(line[xPos])
            y2 = float(line[yPos])
        except ValueError:
            continue

        locInRange = True
        for locId in range(len(queryLocId)):
            if not isInRadius(latitude[locId], longitude[locId], x2, y2, radius):
                locInRange = False

        if locInRange:
            locId = line[locIdPos]
            DCommon[line[categoryPos]].append(locId)
        
    return DCommon

# return 2 dictionaries with the closest locId and it's distance from queryLocId
def LDCloseFunc(inputFile, queryLocId, radius):
    radius = float(radius)
    LDClose = [{}, {}]

    # add latitude and longitude of queryLocId into a list
    latitude = []
    longitude = []
    for i in range(len(queryLocId)):
        latitude.append(float(element(queryLocId[i], inputFile)[0]))
        longitude.append(float(element(queryLocId[i], inputFile)[1]))

    temp = LDCountFunc(inputFile, queryLocId, radius)[1]
    for i in range(len(queryLocId)):
        for key in temp[i].keys():
            for locId in temp[i][key]:
                if locId != queryLocId[i].upper():
                    x2  = element(locId, inputFile)[0]
                    y2  = element(locId, inputFile)[1]
                    if len(temp[i][key]) < 1 or key not in LDClose[i].keys() or distance(latitude[i], longitude[i], x2, y2) < LDClose[i][key][1]:
                        LDClose[i][key] = locId, distance(latitude[i], longitude[i], x2, y2)
            
    return LDClose

# main function calling other functions
def main(inputFile, queryLocId, radius):
    if handleInvalidInput(inputFile, queryLocId, radius):
        return None, None, None, None
    else:
        return LDCountFunc(inputFile, queryLocId, radius)[0], simScoreFunc(LDCountFunc(inputFile, queryLocId, radius)[0]), DCommonFunc(inputFile, queryLocId, radius), LDCloseFunc(inputFile, queryLocId, radius)

# NEED TO REMOVE 
# IMPORTANT:
# LDCount, simScore, DCommon, LDClose = main("shuffle.csv", ["L26", "l52"], 3.5)
# print(LDCount)
# print(simScore)
# print(DCommon)
# print(LDClose)
# print("\n")
LDCount, simScore, DCommon, LDClose = main("locations copy.csv", ["L26", "l52"], 3.5)
print(LDCount)
print(simScore)
print(DCommon)
print(LDClose)
# LDCount1 = [{'P': 1, 'H': 3, 'R': 2, 'C': 2, 'S': 3}, {'P':3, 'H': 2, 'R': 1, 'C': 0, 'S': 2}]
# simScore1 = 0.7711
# DCommon1 = {'P': ['L26'], 'H': ['L52', 'L22'], 'R': ['L88'],'C': [], 'S': ['L30']}
# LDClose1 = [{'H': ('L77', 2.3034), 'R': ('L88', 0.7736), 'C':('L29', 2.0607), 'S': ('L65', 1.556)}, 
# {'P': ('L46', 2.4717),'H': ('L22', 1.4374), 'R': ('L88', 2.5338), 'S': ('L30',2.0482)}]
# NEED TO REMOVE