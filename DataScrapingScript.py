# Transportation Minor Senior Project

# Charlie Marshall
# Start Date: 15 April 2021
# End Date:

# Script to scrape CTA Train Tracker API data for Transportation Minor Senior Project

# Import Packages
from bs4 import BeautifulSoup
import requests
import os
import logging
import schedule
import time

# Logging Data
dir_path = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(dir_path, 'Purple51421PM.txt')
# print(filename)

# Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(filename)
file_handler.setLevel(logging.INFO)
#file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
file_handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(file_handler)

# Important Stations and IDs (9 API requests)
# Central - 41250
# South Boulevard - 40840
# Wilson - 40540
# Fullerton - 41220
# Merchandise Mart - 40460
# Clark/Lake - 40380
# Washington/Wells - 40730
# Merchandise Mart - 40460 (Only need to call once)
# Belmont - 41320
# Wilson - 40540 (Only need to call once)
# South Boulevard - 40840 (Only need to call once)
# Linden - 41050

# Web Scraping
# Central
# Central = 'http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key=8fec6506ea1e456f818195bae61fde65&mapid=41250'
#
# req = requests.get(Central)
# soupC = BeautifulSoup(req.text, 'lxml-xml')
# print(soupC.find_all('rn'))
# print(soupC.find_all('prdt'))
# print(soupC.find_all('arrT'))
#
# # South Boulevard
# SB = 'http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key=8fec6506ea1e456f818195bae61fde65&mapid=40840'
#
# req = requests.get(SB)
# soupSB = BeautifulSoup(req.text, 'lxml-xml')
# print(soupSB.find_all('rn'))
# print(soupSB.find_all('prdt'))
# print(soupSB.find_all('arrT'))

# Web Scraping using One Line Color
purple = 'http://lapi.transitchicago.com/api/1.0/ttpositions.aspx?key=8fec6506ea1e456f818195bae61fde65&rt=P'

def purple_data():
    req = requests.get(purple)
    soup = BeautifulSoup(req.text, 'lxml-xml')

    for train in soup.find_all('train'):
        # if train.isApp.string == "1":
        logger.info([train.rn.string,train.nextStaNm.string,train.isApp.string,train.trDr.string,train.arrT.string])

########### Old Scheduling Method ##########
# purple_data()
# schedule.every(1).minutes.do(purple_data)

# while True:
#     schedule.run_pending()
#     time.sleep(1)
#############################################

if __name__ == '__main__':
    purple_data()
