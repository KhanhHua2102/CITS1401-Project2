"""
This is a computer program that can read the data from a CSV (comma-separated values)
file provided to it and return different interesting analytical results.
Author: Khanh Hua Quang
Student ID: 22928469
"""

def readFile(inputFile):
    try:
        with open (inputFile, "r") as file:
            header = file.readline()[:-1].split(",")
            temp = file.readlines()
            locationList = []
            for line in temp:
                locationList.append(line[:-1].split(","))
    except EOFError:
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
    return round(((((x2 - x1)**2) + (y2 - y1)**2)) ** (1/2), 4)

def isInRadius(x1, y1, x2, y2, radius):
    return distance(x1, y1, x2, y2) < radius

def LDCountFunc(inputFile, queryLocId, radius):
    LDCount = [{'P': 0, 'H': 0, 'R': 0, 'C': 0, 'S': 0}, {'P': 0, 'H': 0, 'R': 0, 'C': 0, 'S': 0}]
    for location in readFile(inputFile)[1]:
        radius = float(radius)
        x2 = float(location[1])
        y2 = float(location[2])
        
        x1 = float(element(queryLocId[0], inputFile)[0])
        y1 = float(element(queryLocId[0], inputFile)[1])
        if isInRadius(x1, y1, x2, y2, radius):
            LDCount[0][location[3]] = LDCount[0].get(location[3]) + 1

        x1 = float(element(queryLocId[1], inputFile)[0])
        y1 = float(element(queryLocId[1], inputFile)[1])
        if isInRadius(x1, y1, x2, y2, radius):
            LDCount[1][location[3]] = LDCount[1].get(location[3]) + 1
        
    return LDCount

def similarity(A, B):
    numerator = (A.get("P")*B.get("P")) + (A.get("H")*B.get("H")) + (A.get("R")*B.get("R")) + (A.get("C")*B.get("C")) + (A.get("S")*B.get("S"))
    denominator1 = (A.get("P")**2 + A.get("H")**2 + A.get("R")**2 + A.get("C")**2 + A.get("S")**2)**(1/2)
    denominator2 = (B.get("P")**2 + B.get("H")**2 + B.get("R")**2 + B.get("C")**2 + B.get("S")**2)**(1/2)
    result = round(numerator / (denominator1 * denominator2), 4)
    return result

def simScoreFunc():
    return

def DCommonFunc():
    return

def LDCloseFunc():
    return


def main(inputFile, querylocId, radius):
    return LDCountFunc(inputFile, querylocId, radius)

main("Locations.csv", ["L26", "L52"], 3.5)


# IMPORTANT: Round results to 4 decimal, header name variation, matching locId
# NEED TO REMOVE 
LDCount = main("Locations.csv", ["L26", "L52"], 3.5)
print(LDCount)
# print(simScore)
# print(DCommon)
# print(LDClose)
# NEED TO REMOVE 