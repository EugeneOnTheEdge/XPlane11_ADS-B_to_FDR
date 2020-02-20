#!/usr/bin/python
import math

# Converts Zulu time to seconds
# Returns: float value
def convert_UTCTime_to_Seconds(s):
	# Creates a array of numbers of Hour, Minute, Second
	HMSarray = s.split(":")

	# Removes the 'Z' zulu indicator in the time
	HMSarray[2] = "".join(HMSarray[2].split("Z"))

	HMS_in_Seconds = float(HMSarray[0]) * 60 * 60 + float(HMSarray[1]) * 60 + float(HMSarray[2])
	return HMS_in_Seconds

#---- PRE-DEFINED CONSTANTS ---
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

STD_PRESSURE = 29.92 #[inches Hg]

# ROLL_SPEED_AT_[airspeed in knots]
# Determines how much the heading changes for every second, when an aircraft is roll is [+ROLL_MULTIPLIER] or [-ROLL_MULTIPLIER] degrees
ROLL_MULTIPLIER = 10 # 10-degree roll
HEADING_RATE_AT_200 = 0.66667 # 0.66667 degrees of change-in-heading per second @ 10-degree roll
HEADING_RATE_AT_300 = 0.5		# 0.5 degrees of change-in-heading per second @ 10-degree roll
HEADING_RATE_100KNOTS_DIFFERENCE = math.fabs(HEADING_RATE_AT_300 - HEADING_RATE_AT_200)

REQUIRED_XPLANE_PARAMETERS = ['TIME', 'TEMP', 'LONGITUDE', 'LATITUDE', 'ALTITUDE', 'RADIO ALTIMETER', 'AILERON RATIO', 'ELEVATOR RATIO', 'RUDDER RATIO', 'PITCH', 'ROLL', 'HEADING,TRACK', 'SPEED,GROUND SPEED', 'VVI,VERTICAL SPEED', 'SLIP', 'TURN', 'MACH', 'AOA', 'STALL', 'FLAP HANDLE POSITION', 'FLAP ACTUAL', 'SLAT RATIO', 'SBRK,SPEEDBRAKE', 'GEAR HANDLE POSITION', 'NGEAR,NOSE GEAR', 'LGEAR,LEFT GEAR', 'RGEAR,RIGHT GEAR', 'ELEV,TRIM', 'NAV-1 FREQUENCY', 'NAV-2 FREQUENCY', 'NAV-1 TYPE', 'NAV-2 TYPE', 'OBS-1', 'OBS-2', 'DME-1', 'DME-2', 'NAV-1 LOCALIZER HORIZONTAL DEFLECTION', 'NAV-2 LOCALIZER HORIZONTAL DEFLECTION', 'NAV-1 N/T/F', 'NAV-2 N/T/F', 'NAV-1 GLIDESLOPE DEFLECTION', 'NAV-2 GLIDESLOPE DEFLECTION', 'OM', 'MM', 'IM', 'F-DIR ON-OFF,FLIGHT DIRECTOR ON-OFF', 'F-DIR PITCH,FLIGHT DIRECTOR PITCH', 'F-DIR ROLL,FLIGHT DIRECTOR ROLL', 'KTMACH', 'THROT,AUTO-THROTTLE', 'HDG MODE', 'ALT MODE', 'HNAV MODE', 'GLSLP MODE', 'BACK MODE', 'SPEED SELEC', 'HDG SELEC', 'VVI SELEC,VS SELEC', 'ALT SELEC', 'BARO', 'DH,DECISION HEIGHT', 'MCAUT,MASTER CAUTION', 'MWARN,MASTER WARNING', 'GPWS', 'MMODE,MAP MODE', 'MRANG,MAP RANGE', 'THROT RATIO', 'PROP CNTRL', 'PROP RPM', 'PROP DEG', 'N1', 'N2', 'MPR', 'EPR', 'TORQ', 'FF,FUEL FLOW', 'ITT', 'EGT', 'CHT']
#-------------------------------

AIRCRAFT_CALLSIGN = "LNI610" # input("Enter aircraft callsign > ").upper()
AIRCRAFT_acf_FILENAME = "Aircraft/Laminar Research/B738 FDR Custom Livery/b738.acf" # "Aircraft/" + input("Enter X-Plane aircraft's .acf location > /Aircraft/")
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
			firstLine = True
			ADSB_date_array = ADSB_data[0].split(" ")[0].split("-")
			ADSB_date = ADSB_date_array[1] + "/" + ADSB_date_array[2] + "/" + ADSB_date_array[0] # converts ADS-B date format to X-Plane's MM/DD/YYYY format

			ADSB_startTime = ADSB_data[0].split(" ")[1]
			ADSB_startTime = convert_UTCTime_to_Seconds(ADSB_startTime)
			
			ADSB_data_previousTime = ADSB_startTime

			# Retrieves the aircraft's heading/track from the ADS-B data. Used to approximate the aircraft's ROLL in the FDR.
			ADSB_data_previousHeading = float(ADSB_data[ADSB_parameters.index('TRACK')])

			# Write the header of FDR file
			outputFDRfile = open(AIRCRAFT_CALLSIGN + ".fdr", "w")
			outputFDRfile.write("A\n") # The needed beginning of the file: 'A' or 'I' for 'Apple' or 'IBM' carriage-returns
			outputFDRfile.write("1\n\n") # FDR Version Number
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
					ADSB_data_currentTime = convert_UTCTime_to_Seconds(ADSB_data[0].split(" ")[1])

					time_difference_from_start_data = ADSB_data_currentTime - ADSB_startTime
					time_difference_from_previous_data = ADSB_data_currentTime - ADSB_data_previousTime
					ADSB_data_previousTime = ADSB_data_currentTime

					parameter_value = str(time_difference_from_start_data)[:5] # Take up to 5 characters in the time string

				else:
					# Get the ADS-B value corresponding to the index (location) of its' parameter name that is required for X-Plane's FDR
					for column in xplane_parameter.split(","):
						if column in ADSB_parameters:
							parameter_value = str(ADSB_data[ADSB_parameters.index(column)])

			else: # ADS-B data does NOT exist for the corresponding X-Plane parameter
				if xplane_parameter == 'GEAR':
					parameter_value = DEFAULT_UP

				elif xplane_parameter == 'BARO':
					parameter_value = STD_PRESSURE

				elif xplane_parameter == 'PITCH':
					# The following 'PITCH' section APPROXIMATES the aircraft's pitch angle, if it's unavailable in the ADS-B data (which it most likely is)
					ADSB_data_verticalSpeed = float(ADSB_data[ADSB_parameters.index('VERTICAL SPEED')]) # in feet/minute (fpm)

					ADSB_data_groundSpeed = float(ADSB_data[ADSB_parameters.index('GROUND SPEED')]) # in knots
					ADSB_data_groundSpeed_fpm = ADSB_data_groundSpeed * 1.852 # 1.852 km/h per knots; 
					ADSB_data_groundSpeed_fpm *= (1000 / 60) # to meters/minute
					ADSB_data_groundSpeed_fpm *= 3.28084 # to feet/minute (fpm)

					pitch = math.atan(ADSB_data_verticalSpeed / ADSB_data_groundSpeed_fpm) * (180/math.pi)
					pitch = "%.2f" % pitch

					parameter_value = pitch

				elif xplane_parameter == 'ROLL':
					# The following 'ROLL' approximates the aircraft's roll angle, if it's unavailable in the ADS-B data (which it most likely is)

					# Gets the change in heading---
					ADSB_data_currentHeading = float(ADSB_data[ADSB_parameters.index('TRACK')])

					heading_difference_from_previous_data = ADSB_data_currentHeading - ADSB_data_previousHeading
					ADSB_data_previousHeading = ADSB_data_currentHeading
					#---

					if time_difference_from_previous_data != 0: # if it's not the first tuple-data in the ADS-B
						change_in_heading_per_second = heading_difference_from_previous_data / time_difference_from_previous_data

						if ADSB_data_groundSpeed < 300:
							speedDifference_ratio = math.fabs(ADSB_data_groundSpeed - 200) / 200
							roll_rate = HEADING_RATE_AT_200 + (speedDifference_ratio * HEADING_RATE_AT_200)
						else:
							speedDifference_ratio = math.fabs(ADSB_data_groundSpeed - 300) / 300
							roll_rate = HEADING_RATE_AT_300 + (speedDifference_ratio * HEADING_RATE_AT_300)

						aircraft_roll = roll_rate * change_in_heading_per_second
						aircraft_roll *= ROLL_MULTIPLIER
						parameter_value = aircraft_roll

					else:
						parameter_value = 0

				elif (xplane_parameter == 'NAV-1 FREQUENCY') or (xplane_parameter == 'NAV-2 FREQUENCY'):
					parameter_value = DEFAULT_NAV_FREQUENCY

				else:
					parameter_value = DEFAULT_UNAVAILABLE

			FDR_data.append(str(parameter_value).split("\n")[0])

	if validADSBdata:
		FDR_data = ",".join(FDR_data)
		outputFDRfile.write(FDR_data + ",\n")
	lineCount += 1

ADSBFile.close()
outputFDRfile.close()