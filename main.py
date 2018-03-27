
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
# Following functions give legend index for qtyWk, wtUtil, and lnCube
def qtyWk(week):
    return week + 14
def wtUtil(week):
    return (week*2)-1 + 34
def lnCube(week):
    return (week*2)-1 + 35



# Dollar weight per
HandlingCost = 1.15
InboundTrans = 1.25

mpg = 6.2
plantWorkingDays = 6


def populate():
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


def finalCost(part, frequency): #final cost to be used w/ frequency
    cost = freight(frequency) + floorSpace(frequency) + invHolding(frequency) + contCapital(frequency)

    return cost



def freight(part, frequency):
     #freight = (miles/mpg) * fuelRate
     freight = 0
     return freight



def floorSpace(part, frequency):
    space = float(part[qtyWk(1)]) // float(part[stdPack]) // float(frequency)

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


def contSupplier(part, frequency):
    #c = ShipSize + ShipSafety
    return 0

def contTransit(part, frequency):
    #Transit = ShipSize(part,frequency) * math.ceil((Shipday(part,frequency)*TransTime(part,frequency))+1) 
    return 0
def TransTime(part,frequency,TruckTime,Mxborder,ODC):
    #T = TruckTime + Mxborder + ODC
    return 0
def getTruckTime(LoadTime,OW_Plantd,AvgSpeed, ServiceTime):
    #T = ((LoadTime + (2*OW_Plantd))/AvgSpeed)/ServiceTime
    return 0 
def Shipday(part,frequency):
    #S = Shipperweek/Plantdays
    return 0
def ShipSize(part,frequency):
    #S = ContainersDay/ShipDay
    return 0
def ContainersDay(part,frequency):
    #C = AvgPartDemand/ContainerStand
    return 0
def AvgPartDemand(part,frequency):
    #A = AvgWeekReq/PlantWorkDays
    return 0
def ShipSafety(part,frequency):
    #S= Min(ContMin,VolumeCalc)
    return 0
def VolumeCalc(part,frequemcy):
    #V= MinSafety*ContainersDay +ShipSize +1
    












populate()

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
