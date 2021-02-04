#License - free to use, copy, and modify for recreation, educational or entertainment purposes only
# - not for commerical, government, or non-governmental organizations
# - use, copy or mofdification by individuals within commerial, or  government organizations including NGOs is permitted for
#        recreation, educational or entertainment purposes.
#No warranty expressly or implied is included, use at risk.
#This licence may only be used when included with the code below, and vice-versa. 

#Expect that the script be in a folder with input file.  An output file is written to this folder.
#The output file name is in the code.  This is overwritten if the script is run again.

#There is a lot of information about different formats of data on-line. 
#This script is to take UK government covid death demographic
#data and look for the ratio of under 70 to over 70 deaths
#input is in JSON format
#this is a typical download link:
#https://api.coronavirus.data.gov.uk/v2/data?areaType=nation&areaCode=E92000001&metric=newDeaths28DaysByDeathDateAgeDemographics&format=csv
#testing is done manually on the csv file, for a couple of days.
#https://coronavirus.data.gov.uk/details/download

#will be very easy to add download from the script

import json
f= "downloadedData.json"

with open (f) as fin:
    j= json.load(fin)

with open ("over70Ratios.csv","w") as fout:
 #reverse the body, since it comes in as newest first
 j["body"].reverse()
 for day in j["body"]:
    under70 = 0
    over70 = 0
    for datas in day["newDeaths28DaysByDeathDateAgeDemographics"]:
            if (datas["age"] == "60+") or (datas["age"] =="00_59"): #these are summary numbers, already counted
                continue
            if (datas["age"] == "90+"): #special case, not an age band with lower and upper age.
                over70 = over70 + int(datas["deaths"])
                continue
            band = int (datas["age"][-2:]) # get the last two letters of the age band
            if (band >= 70):
                over70 = over70 + int(datas["deaths"])
            if (band < 70):
                under70= under70 + int (datas["deaths"])
                
    factor = 999999
    if over70 > 0:
       factor = float(under70)/float(over70)
    else:
       factor = 0 # not sure if this is best?
        
    print (day["date"],factor,under70, over70)
    fout.write(day["date"])
    fout.write(",")
    fout.write(str(factor))
    fout.write("\n")
        
   #expected to take the output CSV file, put into a spreadsheet and draw a graph. 
