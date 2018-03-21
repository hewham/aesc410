
# main py file for aesc410 for calculations n' stuff

import csv
import math

routeLegend = []
partLegend = []
routes = []
parts = []

# Dictionary for looking up route type by route number, ex: "MR" for MilkRun
routeDict = {}

# routeDict  Legend:::
routeID = 0
plannedLaneRate = 2
laneFreq = 3
isRoundTrip = 4
mode = 5
equipCode = 6
miles = 7
piecePrice = 8
pieceWeight = 9

# Parts Legend:::
drawArea = 2
originID = 3
city = 4
state = 5
postalCode = 6
partID = 7
container = 8
stdPack = 9
contL = 10
contW = 11
contH = 12
contT = 13
re = 14
qtyWk1 = 15 #JUST USE WEEK 1 VALUES FOR NOW
qtyWk2 = 16
qtyWk3 = 17
qtyWk4 = 18
qtyWk5 = 19
qtyWk6 = 20
qtyWk7 = 21
qtyWk8 = 22
qtyWk9 = 23
qtyWk10 = 24
qtyWk11 = 25
qtyWk12 = 26
qtyWk13 = 27
qtyWk14 = 28
qtyWk15 = 29
qtyWk16 = 30
qtyWk17 = 31
qtyWk18 = 32
qtyWk19 = 33
qtyWk20 = 34
wtUtilWk1 = 35 #JUST USE WEEK 1 VALUES FOR NOW
lnCubeWk1 = 36
wtUtilWk2 = 37
lnCubeWk2 = 38
wtUtilWk3 = 39
lnCubeWk3 = 40
wtUtilWk4 = 41
lnCubeWk4 = 42
wtUtilWk5 = 43
lnCubeWk5 = 44
wtUtilWk6 = 45
lnCubeWk6 = 46
wtUtilWk7 = 47
lnCubeWk7 = 48
wtUtilWk8 = 49
lnCubeWk8 = 50
wtUtilWk9 = 51
lnCubeWk9 = 52
wtUtilWk10 = 53
lnCubeWk10 = 54
wtUtilWk11 = 55
lnCubeWk11 = 56
wtUtilWk12 = 57
lnCubeWk12 = 58
wtUtilWk13 = 59
lnCubeWk13 = 60
wtUtilWk14 = 61
lnCubeWk14 = 62
wtUtilWk15 = 63
lnCubeWk15 = 64
wtUtilWk16 = 65
lnCubeWk16 = 66
wtUtilWk17 = 67
lnCubeWk17 = 68
wtUtilWk18 = 69
lnCubeWk18 = 70
wtUtilWk19 = 71
lnCubeWk19 = 72
wtUtilWk20 = 73
lnCubeWk20 = 74


# Dollar weight per
HandlingCost = 1.15
InboundTrans = 1.25

mpg = 6.2
plantWorkingDays = 6


def finalCost(part, frequency): #final cost to be used w/ frequency
    cost = freight(frequency) + floorSpace(frequency) + invHolding(frequency) + contCapital(frequency)

    return cost



def freight(part, frequency):
     #freight = (miles/mpg) * fuelRate
     freight = 0
     return freight



def floorSpace(part, frequency):
    space = float(part[qtyWk1]) // float(part[stdPack]) // float(frequency)

    if frequency % plantWorkingDays != 0:
        space = math.ceil(space*1.1)

    return space









def invHolding(part, frequency):
    #invHolding = 0.15* numberParts * costPerPart

    return 0



def contCapital(part, frequency):
    contCapital = contPlant(frequency) + contSupplier(frequency) + contTransit(frequency)

    return contCapital


def contPlant(part, frequency):
    return 0


def contSupplier(part, frequecny):
    return 0

def contTransit(part, frequency):
    return 0








with open('silao_data_set_routes.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)

    i = 0
    for row in reader:
        j = 0
        if i == 0:
            for thing in row:
                routeLegend.append(row[j])
                j = j + 1
        if i != 0:
            routes.append(row)
            routeDict[routes[i-1][0]] = routes[i-1]
        i = i + 1


with open('silao_data_set_parts.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)

    i = 0
    for row in reader:
        j = 0
        if i == 0:
            for thing in row:
                partLegend.append(row[j])
                j = j + 1
        if i != 0:
            parts.append(row)
        i = i + 1





for part in parts:

    print(floorSpace(part, 3))




    if routeDict[part[routeID]][mode] == "TL":

        # print("GOT TL")
        pass
    elif routeDict[part[routeID]][mode] == "MR":
        # print("GOT MR")
        pass
    elif routeDict[part[routeID]][mode] == "CON":
        pass
        # print("GOT CON")
    elif routeDict[part[routeID]][mode] == "ITL":
        pass
        # print("GOT ITL")





