#!/usr/bin/python

def convert_UTCTime_to_Seconds(s): # Converts Zulu time to seconds; returns a double
	# Creates a array of numbers of Hour, Minute, Second
	HMSarray = s.split(":")

	# Removes the 'Z' zulu indicator in the time
	HMSarray[2] = "".join(HMSarray[2].split("Z"))

	HMS_in_Seconds = float(HMSarray[0]) * 60 * 60 + float(HMSarray[1]) * 60 + float(HMSarray[2])
	return HMS_in_Seconds

# Pre-defined Constants
DEFAULT_UNAVAILABLE = 0

DEFAULT_OFF = 0
DEFAULT_ON = 1

DEFAULT_EXTENDED = 1
DEFAULT_RETRACTED = 0

DEFAULT_UP = 1
DEFAULT_DOWN = -1
DEFAULT_LEFT = -1
DEFAULT_RIGHT = 1

DEFAULT_NAV_FREQUENCY = 11010 # 110.10, no decimal point

STD_PRESSURE = 29.96 #[inches Hg]

REQUIRED_XPLANE_PARAMETERS = ['TIME', 'TEMP', 'LONGITUDE', 'LATITUDE', 'ALTITUDE', 'RADIO ALTIMETER', 'AILERON RATIO', 'ELEVATOR RATIO', 'RUDDER RATIO', 'PITCH', 'ROLL', 'HEADING,TRACK', 'SPEED,GROUND SPEED', 'VVI,VERTICAL SPEED', 'SLIP', 'TURN', 'MACH', 'AOA', 'STALL', 'FLAP HANDLE POSITION', 'FLAP ACTUAL', 'SLAT RATIO', 'SBRK,SPEEDBRAKE', 'GEAR HANDLE POSITION', 'NGEAR,NOSE GEAR', 'LGEAR,LEFT GEAR', 'RGEAR,RIGHT GEAR', 'ELEV,TRIM', 'NAV-1 FREQUENCY', 'NAV-2 FREQUENCY', 'NAV-1 TYPE', 'NAV-2 TYPE', 'OBS-1', 'OBS-2', 'DME-1', 'DME-2', 'NAV-1 LOCALIZER HORIZONTAL DEFLECTION', 'NAV-2 LOCALIZER HORIZONTAL DEFLECTION', 'NAV-1 N/T/F', 'NAV-2 N/T/F', 'NAV-1 GLIDESLOPE DEFLECTION', 'NAV-2 GLIDESLOPE DEFLECTION', 'OM', 'MM', 'IM', 'F-DIR ON-OFF,FLIGHT DIRECTOR ON-OFF', 'F-DIR PITCH,FLIGHT DIRECTOR PITCH', 'F-DIR ROLL,FLIGHT DIRECTOR ROLL', 'KTMACH', 'THROT,AUTO-THROTTLE', 'HDG MODE', 'ALT MODE', 'HNAV MODE', 'GLSLP MODE', 'BACK MODE', 'SPEED SELEC', 'HDG SELEC', 'VVI SELEC,VS SELEC', 'ALT SELEC', 'BARO', 'DH,DECISION HEIGHT', 'MCAUT,MASTER CAUTION', 'MWARN,MASTER WARNING', 'GPWS', 'MMODE,MAP MODE', 'MRANG,MAP RANGE', 'THROT RATIO', 'PROP CNTRL', 'PROP RPM', 'PROP DEG', 'N1', 'N2', 'MPR', 'EPR', 'TORQ', 'FF,FUEL FLOW', 'ITT', 'EGT', 'CHT']
#----------------------

AIRCRAFT_CALLSIGN = "LNI610" # input("Enter aircraft callsign > ").upper()
AIRCRAFT_acf_FILENAME = "Aircraft/Laminar Research/Boeing B737-800/b738.acf" # "Aircraft/" + input("Enter X-Plane aircraft's .acf location > /Aircraft/")
fileName = "JT610_Granular_ADSB_Data.csv" #input("Enter ADS-B .csv filename > ")
ADSBFile = open(fileName,"r") 

ADSB_parameters = ADSBFile.readline().split(",")
ADSB_content = ADSBFile.readlines()
ADSB_startTime = None

lineCount = 1

print ("\n## Recognized ADS-B Parameters ##")
for p in range(len(ADSB_parameters)):
	# Removes the indicated units from parameter name
	ADSB_parameters[p] = (" ".join(ADSB_parameters[p].upper().split("(")[0].rsplit(" ")))
	if (ADSB_parameters[p])[-1] == ' ':
		ADSB_parameters[p] = (ADSB_parameters[p])[:len(ADSB_parameters[p]) - 1:]

	print("\""+ADSB_parameters[p]+"\"")
print ("#### \n\n")

for data in ADSB_content:
	ADSB_data = data.split(",")
	FDR_data = ["DATA"]
	validADSBdata = True # An ADS-B tuple data is considered valid if one of latitude and longitude is NOT zero

	if lineCount == 1 or ADSB_startTime == None:
		if ((str(ADSB_data[ADSB_parameters.index('LATITUDE')]) == "0") or (str(ADSB_data[ADSB_parameters.index('LONGITUDE')]) == "0")):
			validADSBdata = False

		if validADSBdata:
			ADSB_date_array = ADSB_data[0].split(" ")[0].split("-")
			ADSB_date = ADSB_date_array[1] + "/" + ADSB_date_array[2] + "/" + ADSB_date_array[0] # converts ADS-B date format to X-Plane's MM/DD/YYYY format

			ADSB_startTime = ADSB_data[0].split(" ")[1]
			ADSB_startTime = convert_UTCTime_to_Seconds(ADSB_startTime)
			print("ADS-B START TIME: " + str(ADSB_startTime) + "\n")

			# Write the header of FDR file
			outputFDRfile = open(AIRCRAFT_CALLSIGN + ".fdr", "w")
			outputFDRfile.write("A\n") # The needed beginning of the file: 'A' or 'I' for 'Apple' or 'IBM' carriage-returns
			outputFDRfile.write("1\n\n\n") # FDR Version Number
			outputFDRfile.write("TAIL," + AIRCRAFT_CALLSIGN + ",\n")
			outputFDRfile.write("DATE," + ADSB_date + ",\n")
			outputFDRfile.write("PRES," + str(STD_PRESSURE) + ",\n")
			outputFDRfile.write("WIND," + "0,0" + ",\n") # From [angle] Heading, speed [knots]
			outputFDRfile.write("TIME," + ADSB_data[0].split(" ")[1].split("Z")[0] + ",\n")
			outputFDRfile.write("ACFT," + AIRCRAFT_acf_FILENAME + "\n\n")
	
	for xplane_parameter in REQUIRED_XPLANE_PARAMETERS:
		if str(ADSB_data[ADSB_parameters.index('LATITUDE')]) == "0" or str(ADSB_data[ADSB_parameters.index('LONGITUDE')]) == "0":
			validADSBdata = False

		if validADSBdata:
			# Checks if the ADS-B has the parameter corresponding to X-Plane's required parameter
			ADSB_data_exists = xplane_parameter in ADSB_parameters
			for paramIndex in range(len(xplane_parameter.split(","))):
				ADSB_data_exists = ADSB_data_exists or (xplane_parameter.split(",")[paramIndex] in ADSB_parameters)

			if ADSB_data_exists:
				if xplane_parameter == 'TIME':
					parameter_value = str(convert_UTCTime_to_Seconds(ADSB_data[0].split(" ")[1]) - ADSB_startTime)[:5] # Take up to 5 characters in the time string

				else:
					# Get the ADS-B value corresponding to the index (location) of its' parameter name that is required for X-Plane's FDR
					for column in xplane_parameter.split(","):
						if column in ADSB_parameters:
							parameter_value = str(ADSB_data[ADSB_parameters.index(column)])

			else: # ADS-B data does NOT exist for the corresponding X-Plane parameter
				if xplane_parameter == 'GEAR':
					parameter_value = str(DEFAULT_DOWN)

				if xplane_parameter == 'BARO':
					parameter_value = str(STD_PRESSURE)

				elif ((xplane_parameter == 'NAV-1 FREQUENCY') or (xplane_parameter == 'NAV-2 FREQUENCY')):
					parameter_value = str(DEFAULT_NAV_FREQUENCY)

				else:
					parameter_value = str(DEFAULT_UNAVAILABLE)

			FDR_data.append(parameter_value.split("\n")[0])

	if validADSBdata:
		FDR_data = ",".join(FDR_data)
		outputFDRfile.write(FDR_data + ",\n")
	lineCount += 1

ADSBFile.close()
outputFDRfile.close()