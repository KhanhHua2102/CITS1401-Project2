"""
This program that can read the data from
a CSV (comma-separated values) file and return different interesting
analytical results.
Author: Khanh Hua Quang
Student ID: 22928469
"""

def main(inputFile,queryLocId,d1,d2):
    
    # open input file in read mode and append data into a list
    with open(inputFile, "r") as file:
        header = file.readline().split(",")          
        temp = file.readlines()
        locationListTemp = []
        locationList = []
        for line in temp:
            locationList.append(line[:-1].split(","))

    # define column position
    locIdPos = 0
    xPos = 1
    yPos = 2
    categoryPos = 3
    for index in range(4):
        if header[index].lower() == "locid":
            locIdPos = index
            break
    for index in range(4):
        if header[index].lower() == "latitude":
            xPos = index
            break
    for index in range(4):
        if header[index][:-1].lower() == "longitude":
            yPos = index
            break
    for index in range(4):
        if header[index].lower() == "category":
            categoryPos = index
            break

    # compare the locId input with locId in locationList to add x, y, category of that locId to a list
    def compareLoc(locId):
        outputList = []
        for location in locationList:
            if locId.lower() == location[locIdPos].lower():
                outputList.append(float(location[xPos]))
                outputList.append(float(location[yPos]))
                outputList.append(location[categoryPos].lower())
        return outputList

    # process raw parameters to handle exceptions
    x1 = compareLoc(queryLocId)[0]
    y1 = compareLoc(queryLocId)[1]
    mainCategory = compareLoc(queryLocId)[2]
    d1 = float(d1)
    d2 = float(d2)

    # define whether a specific location is in the area
    def isInArea(x1, x2, y1, y2, d1, d2):
        return x1 - d1 < x2 < x1 + d1 and y1 - d2 < y2 < y1 + d2

    # handle duplicated queryLocId and missing data
    def inCorretedData(location):
        return location[locIdPos].lower() == queryLocId.lower() or location[locIdPos][1:] == '' or location[locIdPos] == '' or location[xPos] == '' or location[yPos] == '' or location[categoryPos] == '' or location[locIdPos].lower() == "n/a"  or location[xPos].lower() == "n/a" or location[yPos].lower() == "n/a" or location[categoryPos].lower() == "n/a"

    # return locList list
    locList = []
    def locListFunc():
        locListStrip = []
        for location in locationList:
            if inCorretedData(location):
                continue
            x2 = float(location[xPos])
            y2 = float(location[yPos])
            if isInArea(x1, x2, y1, y2, d1, d2):
                locList.append(location[locIdPos].upper()) 
        # output strip list
        for locId in locList:
            locListStrip.append(locId.strip())
        return locListStrip
        
    # return simLocList list
    simLocList = []
    def simLocListFunc():
        simLocListStrip = []
        for locId in locList:
            if compareLoc(locId)[2].lower().strip() == mainCategory:
                simLocList.append(locId)
        # output strip list
        for locId in simLocList:
            simLocListStrip.append(locId.strip())
        return simLocListStrip
    
    # return the distance to main location point
    def distanceFunc(x1, x2, y1, y2):
        return round(((((x2 - x1)**2) + (y2 - y1)**2)) ** (1/2), 4)

    # return distSorted list
    distSorted = []
    def distSortedFunc():
        for locId in simLocList:
            x2  = compareLoc(locId)[0]
            y2  = compareLoc(locId)[1]
            distance = distanceFunc(x1, x2, y1, y2)
            distSorted.append(distance)
        return sorted(distSorted)

    # calculate the average
    def average(input):
        if input == 0 or len(input) == 0:
            return 0
        return round(sum(input) / len(input), 4)

    # calculate the standard deviation
    def standardDeviation(input):
        if input == 0 or len(input) == 0:
            return 0
        accumulate = 0
        for element in input:
            accumulate += (element - average(input)) ** 2
        return round((accumulate / len(input)) ** (1/2), 4)
    
    # return avgstd list
    avgstd = []
    def avgstdFunc():
        distSorted = distSortedFunc()
        avg = average(distSorted)
        std = standardDeviation(distSorted)
        avgstd.append(avg)
        avgstd.append(std)
        return avgstd

    return locListFunc(), simLocListFunc(), distSortedFunc(), avgstdFunc()

# IMPORTANT: handle exeptions, also delete print(), main()
# NEED TO REMOVE 
locList, simLocList, distSorted, avgstd = main("/Users/khanhhuaquang/OneDrive - The University of Western Australia/UWA Learning/Semester 2/CITS1401/Project 1/Locations-sample-Project1 copy.csv", "L83", "1.5", 2.2)
print(locList)
print(simLocList)
print(distSorted)
print(avgstd)
# NEED TO REMOVE


