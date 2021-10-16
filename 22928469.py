"""
This is a computer program that can read the data from a CSV (comma-separated values)
file provided to it and return different interesting analytical results.
-----------------------
Author: Khanh Hua Quang
Student ID: 22928469
-----------------------
"""

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

    # invalid queryLocId input - not list type
    if type(queryLocId) != list:
        print("Invalid queryLocId input!")
        return True

    # invalid queryLocId input - duplicated locId in locList
    for locId in queryLocId:
        count = 0
        for line in readFile(inputFile)[1]:
            if getLocId(locId) == getLocId(line[locIdPos]):
                count += 1
                if count > 1:
                    break
        if count != 1:
            print("Invalid queryLocId")
            return True

    # invalid radius input
    if radius <= 0:
        print("Invalid radius")
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

# get locId number from locID
def getLocId(locId):
    for char in locId:
        if char.isdigit():
            index = locId.index(char)
            return locId[index:].strip()
    print("Not found locId")
    return None

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
    headerPos = header(inputFile)
    locIdPos, xPos, yPos, categoryPos = list(headerPos)

    LDCount = [{'P': 0, 'H': 0, 'R': 0, 'C': 0, 'S': 0}, {'P': 0, 'H': 0, 'R': 0, 'C': 0, 'S': 0}]
    radius = float(radius)

    locList = readFile(inputFile)[1]
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
    return LDCount

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
    DCommon = {'P': [], 'H': [], 'R': [], 'C': [], 'S': []}

    latitude = []
    longitude = []
    for i in range(len(queryLocId)):
        temp = element(queryLocId[i], inputFile)
        latitude.append(float(temp[0]))
        longitude.append(float(temp[1]))

    radius = float(radius)

    locList = readFile(inputFile)[1]
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
    headerPos = header(inputFile)
    locIdPos, xPos, yPos, categoryPos = list(headerPos)
    temp = [{'P': [], 'H': [], 'R': [], 'C': [], 'S': []}, {'P': [], 'H': [], 'R': [], 'C': [], 'S': []}]
    LDClose = [{}, {}]

    # add latitude and longitude of queryLocId into a list
    latitude = []
    longitude = []
    for i in range(len(queryLocId)):
        latitude.append(element(queryLocId[i], inputFile)[0])
        longitude.append(element(queryLocId[i], inputFile)[1])

    radius = float(radius)

    locList = readFile(inputFile)[1]

    for line in locList:
        if isDuplicated(line[locIdPos], inputFile):
            continue
        locId = line[locIdPos]

        if getLocId(locId) != getLocId(queryLocId[0]) and getLocId(locId) != getLocId(queryLocId[1]):
            try:
                x2 = float(line[xPos])
                y2 = float(line[yPos])
            except ValueError:
                continue

            for i in range(len(queryLocId)):
                if isInRadius(latitude[i], longitude[i], x2, y2, radius):
                    temp[i][line[categoryPos]].append(line[locIdPos])

    for i in range(len(queryLocId)):
        for key in temp[i].keys():
            if len(temp[i][key]) > 0:

                queryLocId12 = element(queryLocId[i] , inputFile)
                latitude1 = float(queryLocId12[0])
                longitude1 = float(queryLocId12[1])
                minLoc = temp[i][key][0]
                x2  = element(minLoc, inputFile)[0]
                y2  = element(minLoc, inputFile)[1]
                minDistance = distance(latitude1, longitude1, x2, y2)

                locIdList = temp[i][key]
                for locId in locIdList:
                    if locIdList.index(locId) == 0:
                        continue
                    x2  = element(locId, inputFile)[0]
                    y2  = element(locId, inputFile)[1]
                    if distance(latitude1, longitude1, x2, y2) < minDistance:
                        minLoc = locId
                        minDistance = distance(latitude1, longitude1, x2, y2)

                LDClose[i][key] = minLoc, minDistance
    return LDClose

# main function calling other functions
def main(inputFile, queryLocId, radius):
    if handleInvalidInput(inputFile, queryLocId, radius):
        return None, None, None, None
    else:
        return LDCountFunc(inputFile, queryLocId, radius), simScoreFunc(LDCountFunc(inputFile, queryLocId, radius)), DCommonFunc(inputFile, queryLocId, radius), LDCloseFunc(inputFile, queryLocId, radius)

# NEED TO REMOVE 
# IMPORTANT: invalid input, invalid value
LDCount, simScore, DCommon, LDClose = main("Locations copy.csv", ["L26", "L52"], 3.5)
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