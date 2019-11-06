from bs4 import BeautifulSoup as Soup
from urllib.request import urlopen
from collections import Counter
import re
import csv

pdataDate = []
pdataBalls = []
pdataOut = {}
NUMBERS = []
TIMES = []
CHANCE = []
uniqueNums = 0

for yr in range(2019,2015,-1):
    COUNTER = 0  # We will need this later
    url = urlopen('https://www.lottery.co.uk/lotto/results/archive-{}'.format(str(yr)))
    RAW = url.read()  # Reads data into variable
    url.close()  # Closes connection
    PARSED = Soup(RAW, 'html.parser')  # (DATA, Type of Parser)

    for line in PARSED.findAll('tr'):  # Finds all the 'tr' tags with align:center
        pRAW = re.findall('>(.*?)<', str(line))  # Gathers the dates and balls from that text
        if pRAW[0] == '': # Skip lines that do not contain dates and balls
            pdataDate.append(pRAW[1])  # Stores date in list for mutation later
            pline = ""
            for i in range(3, 10): # Select the balls from the line
                pline += pRAW[i] + " " 
            pdataBalls.append(pline) # Stores balls in list for mutation later
            if pRAW[1] == 'Saturday 10th October 2015': break
            # print(pRAW[1],',',pline)

    for date in pdataDate:
        pdataOut[date] = pdataBalls[COUNTER]  # For every date it will give it value of the numbers
        COUNTER += 1

with open('lotto.csv', 'w', newline='') as data:
    file = csv.writer(data)
    file.writerows(pdataOut.items()) # Save results

def frequency(list):
    global uniqueNums
    BUFFED = []  # Local list to manipulate
    for line in list:
        buffer = line.split()
        for bbuffer in buffer:
            BUFFED.append(bbuffer)
    STORED = Counter(BUFFED)  # Counts each unique number
    uniqueNums = len(STORED)  # Used to tell us how unique numbers there are

    with open('occurrence.csv', 'w', newline='') as data:
        file = csv.writer(data)
        file.writerows(STORED.items())


def solution():
    with open('occurrence.csv', 'r') as data:
        fileReader = csv.reader(data)
        for row in fileReader:
            if any(x.strip() for x in row):
                NUMBERS.append(row[0])  # Grabs first row which are numbers
                TIMES.append(row[1])  # Grabs second row which is the occurrence
                a = str((int(row[1]) / len(pdataBalls)))  # Calculates the occurrence divided by total
                CHANCE.append(a[2:4])  # Possible Chance Strips 00.02345 -> 02 which is in percent


REPORT = {  # Dictionary of the list
    'Numbers': NUMBERS,
    'Times': TIMES,
    'Chance': CHANCE,
}

frequency(pdataBalls)
solution()

with open('report.csv', 'w', newline='') as data:
    dataWriter = csv.writer(data)
    n = 0
    while n < uniqueNums:  # Unique numbers there are
        dataWriter.writerow([
            str(REPORT['Numbers'][n]),
            str(REPORT['Times'][n]),
            str(REPORT['Chance'][n]),
        ])
        n += 1

#print(REPORT['Numbers'][10], REPORT['Times'][10], REPORT['Chance'][10])