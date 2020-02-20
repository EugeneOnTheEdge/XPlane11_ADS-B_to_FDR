# ADS-B to FDR Converter for X-Plane 11
This software converts a given ADS-B flight radar data (usually given by *FlightRadar24* soon after an airline accident) to a replayable FDR file (Flight Data Recorder) for X-Plane 11 PC Flight Simulator.

Now you can see what the pilot "sees" just before their aircraft goes down.

___

***NOTE: ADS-B does NOT record all parameters like the FDR does (for example: N1/N2/N3/N4, flaps, autopilot settings, trim, rudder, etc). It only records basic infos such as time, position (lat + long), ground speed, callsign, altitude, heading and V/S***

On _that_ note (no pun intended), I have created a stupid-simple algorithm that **extrapolates** the **aircraft's pitch and roll**. The pitch works smoothly; the roll doesn't. I'm currently working to make the roll much smoother. With all of those said, yes, the pitch and roll are indeed **_completely artificial_** but they should decently represent what the original accident looks like.
(Without artificial pitch and roll, the aircraft will just be pitching and rolling at 0 degrees while moving around the global map... yeah, imagine how awful it looks..) 

Have a look at JT610_Granular_ADSB_Data.csv for a real-world example of an ADS-B data. The file provides basic parameters recorded in the Lion Air JT610 that plunged into an Indonesian sea back in 2018. Credit to the Granular ADS-B file goes to *FlightRadar24.com*: https://www.flightradar24.com/blog/flightradar24-data-regarding-lion-air-flight-jt610/

You can also try finding Granular ADS-B CSV files from *FlightRadar24* and try converting them using the software. If you do this, however, note that you MUST change the attribute names in the CSV file so that it matches with JT610_Granular_ADSB_Data.csv 's. If you don't, it MAY work but some things may not occur as intended.
**Change the lines 44-46 in the ADS-B_to_FDR.py code so it matches to your aircraft callsign, X-Plane's aircraft .acf file, and the CSV file you want to convert.**

## Enjoy seating yourself in a plane crash!
