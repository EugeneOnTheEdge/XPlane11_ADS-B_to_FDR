#!/usr/bin/python

def convert_UTCTime_to_Seconds(s): # Converts Zulu time to seconds; returns a double
	# Creates a array of numbers of Hour, Minute, Second
	HMSarray = s.split(":")

	# Removes the 'Z' zulu indicator in the time
	HMSarray[2] = "".join(HMSarray[2].split("Z"))

	HMS_in_Seconds = float(HMSarray[0]) * 60 * 60 + float(HMSarray[1]) * 60 + float(HMSarray[2])
	return HMS_in_Seconds

# Pre-defined Constants
UNAVAILABLE = 0
OFF = 0
ON = 1
STD_PRESSURE = 29.96 #[inches Hg]
ACCEPTED_XPLANE_PARAMETERS = ['TIME', 'TEMP', 'LONGITUDE', 'LATITUDE', 'ALTITUDE', 'RADIO ALTIMETER', 'AILERON RATIO', 'ELEVATOR RATIO', 'RUDDER RATIO', 'PITCH', 'ROLL', 'HEADING,TRACK', 'SPEED,GROUND SPEED', 'VVI,VERTICAL SPEED', 'SLIP', 'TURN', 'MACH', 'AOA', 'STALL', 'FLAP HANDLE POSITION', 'FLAP ACTUAL', 'SLAT RATIO', 'SBRK,SPEEDBRAKE', 'GEAR HANDLE POSITION', 'NGEAR,NOSE GEAR', 'LGEAR,LEFT GEAR', 'RGEAR,RIGHT GEAR', 'ELEV,TRIM', 'NAV-1 FREQUENCY', 'NAV-2 FREQUENCY', 'NAV-1 TYPE', 'NAV-2 TYPE', 'OBS-1', 'OBS-2', 'DME-1', 'DME-2', 'NAV-1 LOCALIZER HORIZONTAL DEFLECTION', 'NAV-2 LOCALIZER HORIZONTAL DEFLECTION', 'NAV-1 N/T/F', 'NAV-2 N/T/F', 'NAV-1 GLIDESLOPE DEFLECTION', 'NAV-2 GLIDESLOPE DEFLECTION', 'OM', 'MM', 'IM', 'F-DIR ON-OFF,FLIGHT DIRECTOR ON-OFF', 'F-DIR PITCH,FLIGHT DIRECTOR PITCH', 'F-DIR ROLL,FLIGHT DIRECTOR ROLL', 'KTMACH', 'THROT,AUTO-THROTTLE', 'HDG MODE', 'ALT MODE', 'HNAV MODE', 'GLSLP MODE', 'BACK MODE', 'SPEED SELEC', 'HDG SELEC', 'VVI SELEC,VS SELEC', 'ALT SELEC', 'BARO', 'DH,DECISION HEIGHT', 'MCAUT,MASTER CAUTION', 'MWARN,MASTER WARNING', 'GPWS', 'MMODE,MAP MODE', 'MRANG,MAP RANGE', 'THROT RATIO', 'PROP CNTRL', 'PROP RPM', 'PROP DEG', 'N1', 'N2', 'MPR', 'EPR', 'TORQ', 'FF,FUEL FLOW', 'ITT', 'EGT', 'CHT']
#----------------------

AIRCRAFT_CALLSIGN = "LNI610" # input("Enter aircraft callsign > ").upper()
fileName = "JT610_Granular_ADSB_Data.csv" #input("Enter ADS-B .csv filename > ")
ADSBFile = open(fileName,"r") 

ADSB_parameters = ADSBFile.readline().split(",")
ADSB_content = ADSBFile.readlines()

lineCount = 1

print ("\n## Recognized Parameters ##")
for p in ADSB_parameters:
	# Removes the indicated units from parameter name
	p = (" ".join(p.upper().split("(")[0].rsplit(" ")))
	if p[-1] == ' ':
		p = p[:len(p) - 1:]

	print("\""+p+"\"")
print ("#### \n\n")

for data in ADSB_content:
	ADSB_data = data.split(",")
	FDR_data = []

	if lineCount == 1:
		ADSB_startTime = ADSB_data[0].split(" ")[1]
		ADSB_startTime = convert_UTCTime_to_Seconds(ADSB_startTime)
		print("ADS-B START TIME: " + str(ADSB_startTime))
	
	else:
		FDR_time = convert_UTCTime_to_Seconds(ADSB_data[0].split(" ")[1]) - ADSB_startTime


	lineCount += 1