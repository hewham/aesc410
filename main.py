
# main py file for aesc410 for calculations n' stuff

import csv

routeLegend = []
partLegend = []
routes = []
parts = []

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

routeNumber = 'list'
while routeNumber == 'list':
    routeNumber = str(raw_input('Input a route number  (enter "list" for route numbers): '))
    if routeNumber == 'list':
        for route in routes:
            print(route[0])
    else:
        break


for route in routes:
    if route[0] == routeNumber:
        print(route)

print('')
print('')


verifyRouteHasParts = 0;
for part in parts:
    if part[0] == routeNumber:
        verifyRouteHasParts = verifyRouteHasParts +1
        print(part)

if verifyRouteHasParts == 0:
    print("No Parts Found :(")
