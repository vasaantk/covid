#! /usr/bin/env python3

import datetime
import numpy as np
import matplotlib.pyplot as plt
import sys
plt.rcParams.update({'font.size': 22})




#======================================================================
#    Time series from
# https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series
confirmed = 'time_series_covid19_confirmed_global.csv'
recovered = 'time_series_covid19_recovered_global.csv'
deaths = 'time_series_covid19_deaths_global.csv'
usrQuery = sys.argv[1:]

if len(usrQuery) == 0:
    sys.exit()

pltDiff = False
if '--diff' in usrQuery:
    pltDiff = True
    usrQuery.remove('--diff')




#======================================================================
#    Custom functions
def covidreader(fileName, usrNations, dataType):
    # To store the number of covid cases
    covidArray = []
    sortedArray = []
    natArray = []
    oldIndex = 0
    with open(fileName, 'r') as file:
        dateLine = file.readline()
        dates = dateLine.split(',')[4:]
        dates = np.asarray([datetime.datetime.strptime(i.strip(),
                                                       '%m/%d/%y') for i in dates[0:]])
        for line in file:
            csvAsList = line.split(',')
            # csvAsList[0] is the country's states, if given
            if csvAsList[0] != '':
                statNation = ', '.join(csvAsList[0:2])
            else:
                statNation = csvAsList[1]
            for nat in usrNations:
                if statNation.upper() == nat.upper():
                    covidCases = np.asarray(list(map(int, csvAsList[4:])))
                    covidArray.append(covidCases)
                    natArray.append(nat)
    # Ensure that the arrays are correctly sorted
    for i in usrNations:
        newIndex = natArray.index(i)
        numpyCovidArr = np.asarray(covidArray)
        sortedArray.append(numpyCovidArr[newIndex, :])
        oldIndex += 1
    return np.asarray(sortedArray), np.asarray(dates)

def covidplotter(dates, data, usrNations, dataType, delta, dotType,
                 linecol= None, alfa= 1, lw= 1):
    # To remember the line colour used for each country
    if not linecol:
        lineColArr = []
        useCol = linecol
    else:
        lineColArr = linecol
    numNats = np.shape(data)[0]
    for nats in np.arange(numNats):
        if type(linecol) is list:
            useCol = linecol[nats]
        natLeg = usrNations[nats] + ' (' + dataType + ')'
        if delta:
            covid, = plt.plot(dates[1:], np.diff(data[nats, :]),
                              color= useCol, alpha= alfa, linestyle= dotType, label=
                              natLeg, linewidth= lw)
        else:
            covid, = plt.plot(dates, data[nats, :], color= useCol,
                              alpha= alfa, linestyle= dotType, label= natLeg, linewidth=
                              lw)
        if not linecol:
            lineColArr.append(plt.getp(covid, 'color'))
    return lineColArr




#======================================================================
#    Code begins here
linew= 3
uniqQuery = list(set(usrQuery))

# Get and plot number of confirmed cases
conf, dates = covidreader(confirmed, uniqQuery, 'confirmed')
confcols = covidplotter(dates, conf, uniqQuery, 'confirmed', pltDiff,
                        'solid', lw= linew)

# Get and plot number of recoveries, using the same line colour as
# confirmed cases
reco, dates = covidreader(recovered, uniqQuery, 'recovered')
covidplotter(dates, reco, uniqQuery, 'recovered', pltDiff, 'dashdot',
             linecol= confcols, alfa= 0.6, lw= linew)

# Get an plot the number of deaths
if not pltDiff:
    dead, dates = covidreader(deaths, uniqQuery, 'deaths')
    natLen = np.shape(dead)[0]
    for i in np.arange(natLen):
        recoDead = reco[i, :] + dead[i, :]
        plt.fill_between(dates, recoDead, reco[i, :], alpha= 0.5,
                         label= 'recovered + deaths')

plt.xticks(rotation= 25)
plt.xlabel('Date')
plt.ylabel('Count')
plt.legend()
plt.show()
