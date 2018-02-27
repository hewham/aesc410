import DefaultParameter
from scipy.stats import binom

a=DefaultParameter.DefaultParameter()

Container_L = 48
Container_W = 45
Container_H = 34
St_Pack = 5
Plant_days_Wk = 5
Program_Planning_Volume = 1000
Number_of_Variants = 6
Penetration = 0.5
Part_Veh = 1
Supplier_Plant_Distance = 100
Cross_MX_Border = False
ODC_Processing = False
Calculated_Commodity_Shipment_Week = St_Pack/a.Net_cuft_Truck
Override_Freq = 0
Min_Freq = a.Min_Freq
if (Override_Freq>0):
    Actual_Freq = Override_Freq
else:
    Actual_Freq = max(St_Pack/a.Net_cuft_Truck, a.Min_Freq)
a=DefaultParameter.DefaultParameter(Number_of_Variants, Actual_Freq)


#======================Frequency=========================================

print("======================Frequency=========================================")
apd = Penetration*Program_Planning_Volume*Part_Veh
print("Avg Part Demand/Day: ", apd)
pdw = Plant_days_Wk
print("Plant days/Wk: ", pdw)
pw = apd*pdw
print("Part/Wk: ", pw)
print("Container L: ",Container_L)
print("Container W: ",Container_W)
print("Container H: ",Container_H)
print("St Pack: ", St_Pack)
cp = Container_L * Container_W * Container_H/12/12/12/St_Pack
print("Cuft/Part", cp)
cw = pw*cp
print("Cuft/Week", cw)
print("Calculated Commodity Shipment Week: ", Calculated_Commodity_Shipment_Week)
print("Min Freq: ", a.Min_Freq)
print("Calculated Freq: ", max(St_Pack/a.Net_cuft_Truck,a.Min_Freq))
print("Override Freq: ", Override_Freq)
print("Actual Freq", Actual_Freq)
#======================Plant Bank=========================================

print("======================Plant Bank=========================================")
print("Internal Handling Time: ", a.current_proliferation)
print("Penetration: ", Penetration)
print("Program Planning Volume: ", Program_Planning_Volume)
print("Part/Veh: ", Part_Veh)
print("St Pack: ",St_Pack)
print("Avg Part Demand/Day: ", apd)
cpd = apd/St_Pack
print("Container Per Day", cpd)
ppd = binom.ppf(a.Upper_Confidence_Limit_Volatility, Program_Planning_Volume, Penetration)*Part_Veh
print("Peak Part Demand/Day", ppd)
print("Container Per Day: ", cpd)
Truck_time = (a.Load_Unload_time+(2*Supplier_Plant_Distance/a.Avg_Speed))/10
print(Truck_time)
if Cross_MX_Border:
    MX_Border_Time = a.Mx_Border_Crossing_Time
else:
    MX_Border_Time = 0
if ODC_Processing:
    ODC_Processing_Time = a.ODC_Processing_Delay
else:
    ODC_Processing_Time = 0
ttps = Truck_time+MX_Border_Time+ODC_Processing_Time

print("Material needed to cover a missed/bad shipment:")
print("Time Till Next Delivery: ",ttps," days    Expedite Travel Time: ",Supplier_Plant_Distance/a.Manufacturing_Time/a.Avg_Speed," days")
print("Time Till Next Delivery: ",ttps*cpd," containers    Expedite Travel Time: ",cpd*Supplier_Plant_Distance/a.Manufacturing_Time/a.Avg_Speed," containers")
print("Plant Minimum: ", round(0.1+cpd*min(ttps,Supplier_Plant_Distance/a.Manufacturing_Time/a.Avg_Speed)))
print("Extra Container For Volatility: ", round(0.1+(ppd-apd)/St_Pack))
print("Cover internal handling: ", round(0.1+a.current_proliferation*cpd))
print("Proliferation: ", a.proposed_additional_container)
vol =round(0.1+cpd*min(ttps,Supplier_Plant_Distance/a.Manufacturing_Time/a.Avg_Speed))+round(0.1+(ppd-apd)/St_Pack)+round(0.1+a.current_proliferation*cpd)+a.proposed_additional_container
print("Plant SS Driven By Min Cont: ", a.Min_Containers_Plant, "Vol: ", vol, "Container")
print("Plant SS", max(a.Min_Containers_Plant, vol), "Container")
print("Shipment Size: ", cpd/(Actual_Freq/Plant_days_Wk), "Container")
print("New Plant Bank: ", cpd/(Actual_Freq/Plant_days_Wk)+max(a.Min_Containers_Plant, vol), "Container", cpd/(Actual_Freq/Plant_days_Wk)+max(a.Min_Containers_Plant, vol)/cpd, "ContainerDays")
print("Old Plant Bank w/o Proliferation: ", 2*cpd, "Container", 2, "ContainerDays")
print("Old Proliferation: ", a.current_proliferation)
print("Old Plant Bank: ", 2*cpd*(1+a.current_proliferation), "Container", 2*cpd*(1+a.current_proliferation)/a.Min_Containers_Plant)
#======================In-Transit========================================

print("======================In-Transit========================================")
print("Actual Frequency:: ", Actual_Freq)
print("Plant days/Wk:: ", Plant_days_Wk)
print("Supplier-Plant Distance: ", Supplier_Plant_Distance)
print("Cross MX Border ?: ", Cross_MX_Border)
print("ODC Processing ?: ", ODC_Processing)
print("Load/Unload time: ", a.Load_Unload_time/a.Manufacturing_Time)
print("Shipments Per Day (Lambda): ", Actual_Freq/Plant_days_Wk, "shipments per day")
print("Truck time: ", Truck_time)
print("MX Border Time: ", MX_Border_Time)
print("ODC Processing Time: ", ODC_Processing_Time)
print("Transit Time Per Shipment (Wp): ", ttps)
print("Container Per Day: ", cpd, "Container")
print("Shipment Size: ", cpd/(Actual_Freq/Plant_days_Wk), "Container")
print("Old System Days Freq Ajust: ", a.additional_system_days)
old_citp = round(0.5+Supplier_Plant_Distance/a.Avg_Speed/a.Service_Hrs_Day)*2+MX_Border_Time+ODC_Processing_Time+a.additional_system_days
print("Old Container In Transit w/o Proliferation: ", cpd*old_citp, "Container", old_citp, "ContainerDays")
print("Old Proliferation: ", a.current_proliferation)
print("Old Container In Transit: ", (a.current_proliferation+1)*cpd*old_citp,"Container  ", ((a.current_proliferation+1)*cpd*old_citp)/cpd, "ContainerDays")
print("New Containers In Transit: ", (1+round(0.5+ttps*Actual_Freq/Plant_days_Wk))*(cpd/(Actual_Freq/Plant_days_Wk)), "Container", (1+round(0.5+ttps*Actual_Freq/Plant_days_Wk))*(cpd/(Actual_Freq/Plant_days_Wk))/cpd, "ContainerDays")
#======================Suppplier=========================================

print("======================Suppplier=========================================")
print("Number of Variants: ", Number_of_Variants)
print("Proliferation: ", a.proposed_additional_container)
print("Shipment Size: ", cpd/(Actual_Freq/Plant_days_Wk), "Container")
print("Container Per Day: ", cpd)
print("Old Supplier Bank w/o Proliferation: ", 2*cpd, "Container", 2, "ContainerDays")
print("Old Proliferation: ", a.current_proliferation)
print()