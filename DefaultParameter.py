class DefaultParameter:
    def __init__(self, variants=1, actual_freq=1):
        self.Manufacturing_Time = 16
        self.Load_Unload_time = 2
        self.Mx_Border_Crossing_Time = 3
        self.ODC_Processing_Delay = 1.5
        self.Service_Hrs_Day = 10
        self.Avg_Speed = 50
        self.Min_Containers_Supplier = 2
        self.Min_Safety_Stock_Day_Supplier = 1
        self.Min_Containers_Plant = 2
        self.Internal_Handling_Time = 4
        self.Upper_Confidence_Limit_Volatility = 0.95
        self.Min_Freq = 4
        self.Net_cuft_Truck = 2891
        self.variants = variants
        self.variants_breakpoint = 0
        self.current_proliferation = 0
        self.proposed_additional_container = 0
        self.actual_freq = actual_freq
        self.additional_system_days = 0

        if (self.variants >= 1 and self.variants <= 4):
            self.variants_breakpoint = 1
            self.current_proliferation = 0
            self.proposed_additional_container = 1

        elif (self.variants >= 5 and self.variants <= 10):
            self.variants_breakpoint = 5
            self.current_proliferation = 0.25
            self.proposed_additional_container = 6

        elif (self.variants >= 11 and self.variants <= 30):
            self.variants_breakpoint = 11
            self.current_proliferation = 0.25
            self.proposed_additional_container = 15

        elif (self.variants >= 31 and self.variants <= 40):
            self.variants_breakpoint = 31
            self.current_proliferation = 0.3
            self.proposed_additional_container = 38

        elif (self.variants >= 41 and self.variants <= 50):
            self.variants_breakpoint = 41
            self.current_proliferation = 0.3
            self.proposed_additional_container = 21

        elif (self.variants >= 51 and self.variants <= 70):
            self.variants_breakpoint = 51
            self.current_proliferation = 0.4
            self.proposed_additional_container = 58

        elif (self.variants >= 71 ):
            self.variants_breakpoint = 71
            self.current_proliferation = 0.4
            self.proposed_additional_container = 83

        if(self.actual_freq == 1):
            self.additional_system_days = 8

        elif(self.actual_freq == 2):
            self.additional_system_days = 3

        elif (self.actual_freq == 3):
            self.additional_system_days = 2

        elif (self.actual_freq == 4):
            self.additional_system_days = 2

        elif (self.actual_freq == 5):
            self.additional_system_days = 0

