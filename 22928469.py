"""
This is a computer program that can read the data from a CSV (comma-separated values)
file provided to it and return different interesting analytical results.
Author: Khanh Hua Quang
Student ID: 22928469
"""

def handleInvalidInput(inputFile, queryLocId, radius):
    try:
        file = open(inputFile, "r")
        radius = float(radius)
    except ValueError:
        print("Invalid radius input!")
        return True
    except SyntaxError:
        print("Invalid radius input!")
        return True
    except EOFError:
        print("Invalid inputFile!")
        return True
    except FileNotFoundError:
        print("Invalid inputFile!")
        return True

def readFile(inputFile):
    try:
        with open (inputFile, "r") as file:
            header = file.readline()[:-1].split(",")
            temp = file.readlines()
            locationList = []
            for line in temp:
                locationList.append(line[:-1].split(","))
    except EOFError:
        print("Invalid inputFile!")
        return
    except FileNotFoundError:
        print("Invalid inputFile!")
        return
    return header, locationList

def header(header):
    # define column position in case of random header
    headerPos = []
    for index in range(6):
        if header[index].lower() == "locid":
            headerPos.append(index)
    for index in range(6):
        if header[index].lower() == "latitude":
            headerPos.append(index)
    for index in range(6):
        if header[index].lower() == "longitude":
            headerPos.append(index)
    for index in range(6):
        if header[index].lower() == "category":
            headerPos.append(index)
    for index in range(6):
        if header[index].lower() == "reviews":
            headerPos.append(index)
    for index in range(6):
        if header[index].lower() == "rankreview":
            headerPos.append(index)
    return headerPos[0], headerPos[1], headerPos[2], headerPos[3], headerPos[4], headerPos[5]

# compare the locId input with locId in locationList to add x, y, category element of that locId to a list
def element(locId, inputFile):
    headerPos = header(readFile(inputFile)[0])
    locationList = readFile(inputFile)[1]
    locIdPos = headerPos[0]
    xPos = headerPos[1]
    yPos = headerPos[2] 
    categoryPos = headerPos[3] 
    reviewsPos = headerPos[4] 
    rankPos = headerPos[5]
    outputList = []
    for location in locationList:
        if locId.lower() == location[locIdPos].lower():
            try:
                outputList.append(float(location[xPos]))
                outputList.append(float(location[yPos]))
            except:
                continue
            outputList.append(location[categoryPos].lower())
            try:
                outputList.append(float(location[reviewsPos]))
                outputList.append(float(location[rankPos]))
            except:
                continue
    return outputList

def distance(x1, y1, x2, y2):
    distance = round(((((x2 - x1)**2) + (y2 - y1)**2)) ** (1/2), 4)
    return distance

def isInRadius(x1, y1, x2, y2, radius):
    return distance(x1, y1, x2, y2) < radius

def LDCountFunc(inputFile, queryLocId, radius):
    LDCount = [{'P': 0, 'H': 0, 'R': 0, 'C': 0, 'S': 0}, {'P': 0, 'H': 0, 'R': 0, 'C': 0, 'S': 0}]
    for location in readFile(inputFile)[1]:
        radius = float(radius)
        x2 = float(location[1])
        y2 = float(location[2])
        
        latitude1 = float(element(queryLocId[0].strip(), inputFile)[0])
        longitude1 = float(element(queryLocId[0].strip(), inputFile)[1])
        if isInRadius(latitude1, longitude1, x2, y2, radius):
            LDCount[0][location[3]] = LDCount[0].get(location[3]) + 1

        latitude1 = float(element(queryLocId[1].strip(), inputFile)[0])
        longitude2 = float(element(queryLocId[1].strip(), inputFile)[1])
        if isInRadius(latitude1, longitude2, x2, y2, radius):
            LDCount[1][location[3]] = LDCount[1].get(location[3]) + 1
        
    return LDCount

def similarity(A, B):
    numerator = (A.get("P")*B.get("P")) + (A.get("H")*B.get("H")) + (A.get("R")*B.get("R")) + (A.get("C")*B.get("C")) + (A.get("S")*B.get("S"))
    denominator1 = (A.get("P")**2 + A.get("H")**2 + A.get("R")**2 + A.get("C")**2 + A.get("S")**2)**(1/2)
    denominator2 = (B.get("P")**2 + B.get("H")**2 + B.get("R")**2 + B.get("C")**2 + B.get("S")**2)**(1/2)
    result = round(numerator / (denominator1 * denominator2), 4)
    return result

def simScoreFunc(LDCount):
    A = LDCount[0]
    B = LDCount[1]
    return similarity(A, B)

def DCommonFunc(inputFile, queryLocId, radius):
    DCommon = {'P': [], 'H': [], 'R': [], 'C': [], 'S': []}
    for location in readFile(inputFile)[1]:
        radius = float(radius)
        latitude1 = float(element(queryLocId[0].strip(), inputFile)[0])
        longitude1 = float(element(queryLocId[0].strip(), inputFile)[1])
        latitude2 = float(element(queryLocId[1].strip(), inputFile)[0])
        longitude2 = float(element(queryLocId[1].strip(), inputFile)[1])
        x2 = float(location[1])
        y2 = float(location[2])
        if isInRadius(latitude1, longitude1, x2, y2, radius) and isInRadius(latitude2, longitude2, x2, y2, radius):
            DCommon[location[3]].append(location[0])
        
    return DCommon

def LDCloseFunc(inputFile, queryLocId, radius):
    temp = [{'P': [], 'H': [], 'R': [], 'C': [], 'S': []}, {'P': [], 'H': [], 'R': [], 'C': [], 'S': []}]
    LDClose = [{}, {}]
    latitude1 = float(element(queryLocId[0].strip(), inputFile)[0])
    longitude1 = float(element(queryLocId[0].strip(), inputFile)[1])
    latitude2 = float(element(queryLocId[1].strip(), inputFile)[0])
    longitude2 = float(element(queryLocId[1].strip(), inputFile)[1])
    radius = float(radius)

    for location in readFile(inputFile)[1]:
        if location[0] != queryLocId[0].strip() and location[0] != queryLocId[1].strip():
            x2 = float(location[1])
            y2 = float(location[2])
            if isInRadius(latitude1, longitude1, x2, y2, radius):
                temp[0][location[3]].append(location[0]) 
            if isInRadius(latitude2, longitude2, x2, y2, radius):
                temp[1][location[3]].append(location[0])
        else:
            continue

    for i in range(2):
        for key in temp[i].keys():
            if len(temp[i][key]) > 0:
                minLoc = temp[i][key][0]
                latitude1 = float(element(queryLocId[i].strip(), inputFile)[0])
                longitude1 = float(element(queryLocId[i].strip(), inputFile)[1])
                x2  = element(minLoc, inputFile)[0]
                y2  = element(minLoc, inputFile)[1]
                minDistance = distance(latitude1, longitude1, x2, y2)
                
                locIdList = temp[i][key]
                for locId in locIdList:
                    if locId != queryLocId[i]:
                        latitude1 = float(element(queryLocId[i].strip(), inputFile)[0])
                        longitude1 = float(element(queryLocId[i].strip(), inputFile)[1])
                        x2  = element(locId, inputFile)[0]
                        y2  = element(locId, inputFile)[1]
                        if distance(latitude1, longitude1, x2, y2) < minDistance:
                            minLoc = locId
                            minDistance = distance(latitude1, longitude1, x2, y2)
                    else:
                        continue
                if minLoc != 0:
                    LDClose[i][key] = minLoc, minDistance
    
    return LDClose


def main(inputFile, queryLocId, radius):
    if handleInvalidInput(inputFile, queryLocId, radius):
        return None, None, None, None
    else:
        return LDCountFunc(inputFile, queryLocId, radius), simScoreFunc(LDCountFunc(inputFile, queryLocId, radius)), DCommonFunc(inputFile, queryLocId, radius), LDCloseFunc(inputFile, queryLocId, radius)


# IMPORTANT: invalid input, file open error handle, invalid value, random row id, missing header, case insensitive, locID unique, header name variation, matching locId, strip, random header
# NEED TO REMOVE 
# LDCount, simScore, DCommon, LDClose = main("Locations.csv", ["L26", "L52"], 3.5)
LDCount, simScore, DCommon, LDClose = main ("Locat22ions.csv" , ["L89", "L15"], "4.3")
print(LDCount)
print(simScore)
print(DCommon)
print(LDClose)
# NEED TO REMOVE 