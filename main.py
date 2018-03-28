
# main py file for aesc410 for calculations n' stuff
import csv
import math
import string

routeLegend = []
partLegend = []
containerLegend = []
routes = []
parts = []
containers = []

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
containerNameInPart = 8
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

# Containers Legend:::
containerName = 0
containerRE = 1
containerPrice = 2

# Dollar weight per
HandlingCost = 1.15
InboundTrans = 1.25

mpg = 6.2
plantWorkingDays = 6

ManufacTime = 2









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

    with open('container_names_with_pricing.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        i = 0
        for row in reader:
            j = 0
            if i == 0:
                for thing in row:
                    containerLegend.append(row[j])
                    j = j + 1
            if i != 0:
                containers.append(row)
            i = i + 1









###############METRICS WE NEED TO LOOKUP BY ROW###########
#ONE WAY PLANT DISTANCE - Miles
def getMiles(part):
    global routes
    global routeID
    global miles
    i=0;
    for route in routes:
        if route[routeID] == part[routeID]:
            break;
        i+=1
    return float(routes[i][miles])

#AVG WEEKLY PARTS REQUIRED done
def averageQtyWk(part):
    total = 0;
    for i in range(0,20):
        if part[qtyWk(i)].isalpha() == False:
            total += float(part[qtyWk(i)])
    return total/20

#MANUFACTURING TIME

#PEAK WEEKLY PARTS REQUIRED
def maxQtyWk(part):
    max = 0;
    for i in range(0,20):
        if qtyWk(i) > max:
            max = qtyWk(i)
    return max

#NUMBER OF PARTS
def numOfParts(route):
    num = 0;
    for part in parts:
        if part[routeID] == route[routeID]:
            num+=1
    return num

#COST PER PART
# part[piecePrice]

#FUEL RATE
fuelRate = 2.559

# GAS PRICE PER ROUTE
def gasCost(miles):
    global mpg
    global fuelRate
    return (miles/mpg) * fuelRate

def containerPrice(part):
    global containers
    global containerNameInPart
    global containerName
    for container in containers:
        if part[containerNameInPart] == container[containerName]:
            return container[containerPrice]

##########################################################


def finalCost(part, frequency): #final cost to be used w/ frequency
    cost = freight(part, frequency) + floorSpace(part, frequency) + invHolding(part, frequency) + contCapital(part, frequency)
    return cost









######################################## 4 MAIN COST CALCULATIONS ##########################
def freight(part, frequency):
     global mpg
     global fuelRate
     return (getMiles(part)/mpg) * fuelRate

def floorSpace(part, frequency):
    global stdPack
    global plantWorkingDays
    space = float(part[qtyWk(1)]) / float(part[stdPack]) / float(frequency)

    if frequency % plantWorkingDays != 0:
        space = math.ceil(space*1.1)

    return space

def invHolding(part, frequency):
    # I = 0.15 * numberParts * costPerPart
    # I = 0.15 * floorSpace(part, frequency) * costPerPart
    # return I
    return 5

def contCapital(part, frequency):
    containerNum = contPlant(part,frequency) + contSupplier(part,frequency) + contTransit(part, frequency)
    contCapital = containerNum * containerPrice(part)
    return contCapital










##################### PLANT CALC ##########################################################
def contPlant(part, frequency):
    S = ShipSize(part, frequency) + PlantSafetyStock(part, frequency)
    return S

def PlantSafetyStock(part, frequency):
    S = min(2, PlantVolumeCalc(part, frequency))
    return S

def PlantVolumeCalc(part, frequency):
    C = PlantMin(part) + PartVolatility(part) + IntHandling(part) + 1
    return C

def PlantMin(part):
    global ManufacTime
    expedTrans = (getMiles(part)/50)/ManufacTime
    M = min(  TransTime(part) , expedTrans  ) * ContainersPerDay(part)
    return M

def PartVolatility(part):
    PeakPartDemandPerDay = maxQtyWk(part)/6
    V = (PeakPartDemandPerDay - AvgPartDemand(part))/(float(part[stdPack]))
    return V

def IntHandling(part):
    global ManufacTime
    IntHandlingTime = 4/ManufacTime
    H = IntHandlingTime * ContainersPerDay(part)
    return H










################SUPPLIER CALC ###########################################################
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
    global stdPack
    C = AvgPartDemand(part)/(float(part[stdPack]))
    return C

def AvgPartDemand(part):  #EQ GOOD
    APD = (averageQtyWk(part)/6)
    return APD

def TransTime(part):
    T = TruckTime(part) + MxBorder(part) + ODC(part)
    return T

def TruckTime(part): #EQ GOOD
    global routes
    T = (2 + ((2*getMiles(part))/50))/10
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




    if routeDict[part[routeID]][mode] == "TL":
        print(finalCost(part, 3))
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
