from pandas.io.json import json_normalize
from OTXv2 import OTXv2, IndicatorTypes
from datetime import datetime, timedelta
from termcolor import colored, cprint
#import pandas as pd
import datetime
import json
import csv
import os

def get_iocs(today):
   dic = []
   cprint("\nCollecting iocs for the date : "+str(today)+"..This may take sometime depending on your network speed..",'yellow', attrs=['bold'])
   otx = OTXv2("758fe3198bde37e69611027cc1e90ed40d796aaaf7f6bf71470a5e6586eaf9a8")
   iocs = {}
   pulses = otx.getall()
   
   file = open('./OTX_IoCs.csv'+str(today),'w')
   for each in pulses:
       pulsedate=each['created'].split('T')[0] 
       if (pulsedate==today):
           dic.append(each)
   for each in dic:
      for ioc in each['indicators']:
         iocs['IOC']=str(ioc['indicator'])
         iocs['IOC_Created']=str(ioc['created'])
         iocs['Title']=ioc['title']
         iocs['Is_active_(0/1)_?']=str(ioc['is_active'])
         iocs['Type']=ioc['type']
         iocs['Tags']=','.join(each['tags'])
         iocs['Pulse_Created']=str(each['created'])
         iocs['Malware_Families']=','.join(each['malware_families'])
         iocs['References']=' '.join(each['references'])
         iocs['Targeted_Countries']=','.join(each['targeted_countries'])
         iocs['Industries']=','.join(each['industries'])
         writer = csv.DictWriter(file, iocs.keys())
         if file.tell() == 0:
            writer.writeheader()
         for data in iocs:
            writer.writerow(iocs)
choice = raw_input("\nEnter your choice for fetching iocs : \n\n1.Check iocs for today \n2.Check iocs for a specific date : \n")
if choice == "1" :
   date = datetime.datetime.utcnow().isoformat()
   today = date.split('T')[0]
   print(today)
   get_iocs(today)
if choice == "2":
   today = raw_input("\nEnter date in the following format - 'year-month-day'.. Eg : 2020-11-03\n\n")
   get_iocs(today)
'''
df = pd.read_csv('./iocs.csv')
df.drop_duplicates(inplace=True)
print("Removed duplicates ..")
df.to_csv('./iocs', index=False)
'''
print("\nFinished collecting iocs..Check iocs.csv to see the results..")
