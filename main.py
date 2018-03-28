
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




###############METRICS WE NEED TO LOOKUP BY ROW###########
#ONE WAY PLANT DISTANCE
#AVG WEEKLY PARTS REQUIRED
#CONTAINER STANDARD PACK
#MANUFACTURING TIME
#PEAK WEEKLY PARTS REQUIRED
#NUMBER OF PARTS
#COST PER PART
#FUEL RATE
##########################################################



def finalCost(part, frequency): #final cost to be used w/ frequency
    cost = freight(part, frequency) + floorSpace(part, frequency) + invHolding(part, frequency) + contCapital(part, frequency)
    return cost


######################################## 4 MAIN COST CALCULATIONS ##########################
def freight(part, frequency):
     F = (miles/6.2) * FuelRate
     return F

def floorSpace(part, frequency):
    space = float(part[qtyWk(1)]) // float(part[stdPack]) // float(frequency)

    if frequency % plantWorkingDays != 0:
        space = math.ceil(space*1.1)

    return space

def invHolding(part, frequency):
    I = 0.15* numberParts * costPerPart
    return I

def contCapital(part, frequency):
    contCapital = contPlant(part,frequency) + contSupplier(part,frequency) + contTransit(part, frequency)
    return contCapital




#####################PLANT CALC##########################################################
def contPlant(part, frequency):
    S = ShipSize(part, frequency) + PlantSafetyStock()
    return S

def PlantSafetyStock(part, frequency):
    S = min(2, PlantVolumeCalc(part, frequency))
    return S

def PlantVolumeCalc(part, frequency):
    C = PlantMin(part) + PartVolatility(part) + IntHandling(part) + 1
    return C

def PlantMin(part):
    expedTrans = (OneWayPlantDist/50)/ManufacTime
    M = min(  TransTime(part) , expedTrans  ) * ContainersPerDay(part)
    return M

def PartVolatility(part):
    PeakPartDemandPerDay = PeakWeeklyPartsReq/6
    V = (PeakPartDemandPerDay - AvgPartDemand(part))/ContainerStand
    return V

def IntHandling(part):
    IntHandlingTime = 4/ManufacTime
    H = IntHandlingTime * ContainersPerDay(part)
    return H

################SUPPLIER CALC###########################################################
def contSupplier(part, frequency):
    C = ShipSize(part, frequency) + SupplierSafetyStock(part, frequency)
    return C

def SupplierSafetyStock(part,frequency): ###check w/ supply chain, as contperday is part of shipsize calc???
    S= min(2,   (ContainersPerDay(part) + ShipSize(part, frequency) + 1)   )
    return S


#############TRANSIT CALC################################################################
def contTransit(part, frequency): #EQ GOOD
    T = ShipSize(part,frequency) * math.ceil(frequency*TransTime(part))+1
    return T

def ShipSize(part,frequency):   #EQ GOOD
    S = (ContainersPerDay(part))/frequency
    return S

def ContainersPerDay(part): #EQ GOOD
    C = AvgPartDemand(part)/ContainerStand)
    return C

def AvgPartDemand(part):  #EQ GOOD
    APD = (AvgWeekReq/6)
    return APD

def TransTime(part):
    T = TruckTime(part) + MxBorder(part) + ODC(part)
    return T

def TruckTime(part): #EQ GOOD
    T = (2 + ((2*OneWayPlantDist)/50))/10
    return T

def MxBorder(part): #EQ GOOD
    #if departure is in US:
    #    return 3
    #else:
        return 0

def ODC(part):
    #if type is 'CON':
    #   return 1.5
    #else:
        return 0
##########################################################################################




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
