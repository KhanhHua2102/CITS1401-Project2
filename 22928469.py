"""
This is a computer program that can read the data from a CSV (comma-separated values)
file provided to it and return different interesting analytical results.
Author: Khanh Hua Quang
Student ID: 22928469
"""

# IMPORTANT: Round results to 4 decimal

def readFile(inputFile):
    try:
        with open (inputFile, "r") as file:
            header = file.readline().split(",")
            temp = file.readlines()
            locationList = []
            for line in temp:
                locationList.append(line[:-2].split(","))
    except EOFError:
        return

def isInRadius(x1, y1, x2, y2, radius):
    return x1 < x2 < x1 + radius and y1 < y2 < y1 + radius

def LDCount():
    return

def similarity(A, B):
    numerator = (A.get("P")*B.get("P")) + (A.get("H")*B.get("H")) + (A.get("R")*B.get("R")) + (A.get("C")*B.get("C")) + (A.get("S")*B.get("S"))
    denominator1 = (A.get("P")**2 + A.get("H")**2 + A.get("R")**2 + A.get("C")**2 + A.get("S")**2)**(1/2)
    denominator2 = (B.get("P")**2 + B.get("H")**2 + B.get("R")**2 + B.get("C")**2 + B.get("S")**2)**(1/2)
    result = round(numerator / (denominator1 * denominator2), 4)
    return result

def simScore():
    return

def DCommon():
    return

def distance(x1, y1, x2, y2):
    return round(((((x2 - x1)**2) + (y2 - y1)**2)) ** (1/2), 4)

def LDClose():
    return


def main(inputFile, locId, radius):
    readFile(inputFile)
    
    return

main("Locations.csv", ["L26", "L52"], 3.5)

# LDCount, simScore, DCommon, LDClose = main("Locations.csv", ["L26", "L52"], 3.5)
# print(LDCount)
# print(simScore)
# print(DCommon)
# print(LDClose)