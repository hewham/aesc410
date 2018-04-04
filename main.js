
// main py file for aesc410 for calculations n' stuff
// import csv
// import math
// import string

const Papa = require('papaparse');
const partsCSV = '../silao_data_set_parts.csv';
const routesCSV = '../silao_data_set_routes.csv';
const containersCSV = '../container_names_with_pricing.csv';

var routeLegend = [];
var partLegend = [];
var containerLegend = [];
var routes = [];
var parts = [];
var containers = [];

// Dictionary for looking up route type by route number, ex: "MR" for MilkRun
var routeDict = {};

// routeDict  Legend:::
var routeID = 0;
var plannedLaneRate = 2;
var laneFreq = 3;
var isRoundTrip = 4;
var mode = 5;
var equipCode = 6;
var miles = 7;
var piecePrice = 8;
var pieceWeight = 9;

// Parts Legend:::
var drawArea = 2;
var originID = 3;
var city = 4;
var state = 5;
var postalCode = 6;
var partID = 7;
var containerNameInPart = 8;
var stdPack = 9;
var contL = 10;
var contW = 11;
var contH = 12;
var contT = 13;
var re = 14;
// Following functions give legend index for qtyWk, wtUtil, and lnCube
function qtyWk(week){
  return week + 14;
}
function wtUtil(week){
  return (week*2)-1 + 34;
}
function lnCube(week){
  return (week*2)-1 + 35;
}

// Containers Legend:::
var containerName = 0;
var containerRE = 1;
var containerPrice = 2;

// Dollar weight per
var HandlingCost = 1.15;
var InboundTrans = 1.25;

var mpg = 6.2;
var plantWorkingDays = 6;

var ManufacTime = 2;



function populate(){
  console.log(originID);


  Papa.parse(partsCSV, {
    complete: function(results) {
      console.log(results);
    }
  });


  } // populate()



// function populate(){
//   console.log(originID);
//
//   with open('silao_data_set_routes.csv') as csvfile{
//     reader = csv.reader(csvfile)
//     let i = 0;
//     for (let row of reader){
//       let j = 0;
//       if (i == 0){
//         for (let thing of row){
//           routeLegend.push(row[j])
//           j = j + 1
//         }
//       }
//       if (i != 0){
//         routes.push(row)
//         routeDict[routes[i-1][0]] = routes[i-1]
//       }
//       i = i + 1
//     }
//   }
//
//   with open('silao_data_set_parts.csv') as csvfile{
//     reader = csv.reader(csvfile)
//     let i = 0
//     for (let row of reader){
//       let j = 0
//       if (i == 0){
//         for (let thing in row){
//           partLegend.push(row[j])
//           j = j + 1
//         }
//       }
//       if (i != 0){
//         console.log(row[originID]);
//         if (row[originID] == "#N/A"){
//           parts.push(row)
//         }
//       }
//       i = i + 1
//     }
//   }
//
//   with open('container_names_with_pricing.csv') as csvfile:
//     reader = csv.reader(csvfile)
//     let i = 0;
//     for (let row of reader){
//       let j = 0;
//       if (i == 0){
//         for (let thing of row){
//           containerLegend.push(row[j])
//           j = j + 1
//         }
//       }
//       if (i != 0){
//         containers.push(row)
//       }
//       i = i + 1
//     }
//   } // populate()








//////////////////////////////METRICS WE NEED TO LOOKUP BY ROW//////////////////////
//ONE WAY PLANT DISTANCE - Miles
function getMiles(part){
    let i = 0;
    for (let route of routes)
      if (route[routeID] == part[routeID]){
        break;
      }
      i++;
    return float(routes[i][miles])
  }
//AVG WEEKLY PARTS REQUIRED done
function averageQtyWk(part){
    let total = 0;
    for (i=0; i<20; i++){
      if (part[qtyWk(i)].isalpha() == False){
        total += float(part[qtyWk(i)]);
      }
    }
    return total/20;
  }
//MANUFACTURING TIME

//PEAK WEEKLY PARTS REQUIRED
function maxQtyWk(part){
    let max = 0;
    for (i=0; i<20; i++){
      if (qtyWk(i) > max){
        max = qtyWk(i);
      }
    }
    return max
  }
//NUMBER OF PARTS
function numOfParts(route){
    let num = 0;
    for (let part of parts){
      if (part[routeID] == route[routeID]){
        num++;
      }
    }
    return num;
  }
//COST PER PART
// part[piecePrice]

//FUEL RATE
var fuelRate = 2.559;

// GAS PRICE PER ROUTE
function gasCost(miles){
  return (miles/mpg) * fuelRate;
}

function containerPrice(part){
  for (let container of containers){
    if (part[containerNameInPart] == container[containerName]){
      return container[containerPrice];
    }else{
      return 0;
    }
  }
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


function finalCost(part, frequency){ //final cost to be used w/ frequency
  let cost = freight(part, frequency) + floorSpace(part, frequency) + invHolding(part, frequency) + contCapital(part, frequency);
  return cost;
}








////////////////////////////////// 4 MAIN COST CALCULATIONS ////////////////////////////////
function freight(part, frequency){
  return (getMiles(part)/mpg) * fuelRate;
}

function floorSpace(part, frequency){
    let space = float(part[qtyWk(1)]) / float(part[stdPack]) / float(frequency);
    if (frequency % plantWorkingDays != 0){
      space = Math.ceil(space*1.1);
    }
    return space;
}
function invHolding(part, frequency){
    // I = 0.15 * numberParts * costPerPart
    // I = 0.15 * floorSpace(part, frequency) * costPerPart
    // return I
    return 5;
}

function contCapital(part, frequency){
  let containerNum = contPlant(part,frequency) + contSupplier(part,frequency) + contTransit(part, frequency);
  let contCapital = containerNum * containerPrice(part);
  return contCapital;
}









////////////////////////////////////////// PLANT CALC ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function contPlant(part, frequency){
  return ShipSize(part, frequency) + PlantSafetyStock(part, frequency);
}

function PlantSafetyStock(part, frequency){
  return min(2, PlantVolumeCalc(part, frequency));
}

function PlantVolumeCalc(part, frequency){
  return PlantMin(part) + PartVolatility(part) + IntHandling(part) + 1;
}

function PlantMin(part){
  let expedTrans = (getMiles(part)/50)/ManufacTime;
  return min(TransTime(part), expedTrans) * ContainersPerDay(part);
}

function PartVolatility(part){
  let PeakPartDemandPerDay = maxQtyWk(part)/6;
  return (PeakPartDemandPerDay - AvgPartDemand(part))/(float(part[stdPack]));
}

function IntHandling(part){
  let IntHandlingTime = 4/ManufacTime;
  return IntHandlingTime * ContainersPerDay(part);
}









////////////////////////////////SUPPLIER CALC //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function contSupplier(part, frequency){
    return ShipSize(part, frequency) + SupplierSafetyStock(part, frequency);
  }

function SupplierSafetyStock(part,frequency){
  //////check w/ supply chain, as contperday is part of shipsize calc???
  return min(2,(ContainersPerDay(part) + ShipSize(part, frequency) + 1));
}









////////////////////////// TRANSIT CALC //////////////
function contTransit(part, frequency){
   //EQ GOOD
  return ShipSize(part,frequency) * math.ceil(frequency*TransTime(part))+1;
}

function ShipSize(part,frequency){
   //EQ GOOD
  return (ContainersPerDay(part))/frequency;
}

function ContainersPerDay(part){
   //EQ GOOD
  return AvgPartDemand(part)/(float(part[stdPack]));
}

function AvgPartDemand(part){
  //EQ GOOD
  return (averageQtyWk(part)/6);
}

function TransTime(part){
  return TruckTime(part) + MxBorder(part) + ODC(part);
}

function TruckTime(part){
   //EQ GOOD
  return (2 + ((2*getMiles(part))/50))/10;
}




function MxBorder(part){
   //EQ GOOD
    //if departure is in US:
    //    return 3
    //else:
        return 0
}

function ODC(part){
    //if type is 'CON':
    //   return 1.5
    //else:
        return 0
}
///////////////////////////////////







populate();

// j = 0
// for part in parts:
//     i = 0
//     for field in part:
//         if i > 16 and part[i].strip() != "-":
//             part[i] = field.strip().replace(',','')
//         elif part[i].strip() == "-":
//             parts.pop(j)
//             break
//         i += 1
//     console.log(part)
//     j += 1


for (let part of parts){
    if (routeDict[part[routeID]][mode] == "TL"){
      // console.log(finalCost(part, 3))
    }
    else if (routeDict[part[routeID]][mode] == "MR"){
      // console.log("GOT MR")
    }
    else if (routeDict[part[routeID]][mode] == "CON"){
       // console.log("GOT CON")
    }
    else if (routeDict[part[routeID]][mode] == "ITL"){
      // console.log("GOT ITL")
    }
}
