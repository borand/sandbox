def process_default(data):
	#print("process_default({})".format(data))
	return data[1]

##########################################################################################
# Define special processing functions for various sensor data
def process_hydro_power_data(data):    
    power = round(3600.0/((pow(2,16)*float(data[1]) + float(data[2]))/16.0e6*1024.0))    
    print("process_hydro_power_data({} = power = {})".format(data,power))
    if power < 120.0*100.0: # 120V @ 100A 
        return power
    else:
        return -1

def process_hydro_wh_data(data):
    print("process_hydro_wh_data({})".format(data))
    return data[2]

def process_1wire_thermometer(data):
    print("process_default({})".format(data))
    return data[1]	