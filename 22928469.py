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
            print(locationList)
    except EOFError:
        return

def isInRadius(x1, y1, x2, y2):

    return

def LDCount():
    return

def similarity(A, B):
    return

def simScore():
    return

def DCommon():
    return

def distance(x1, y1, x2, y2):
    return

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