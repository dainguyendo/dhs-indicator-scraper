#-------------------------------------------------------------------------------
# Name:         getDHS
# Purpose:      Using DHS api to retrieve indicator data and save as csv
#
# Author:      dain8691
#
# Created:     31/05/2016
# Copyright:   (c) dain8691 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import urllib, urllib2, json, csv

source = 'http://api.dhsprogram.com/rest/dhs/data'

def getIndicators(url = 'http://api.dhsprogram.com/rest/dhs/indicators?returnFields=IndicatorId,Label,Definition&f=json'):
    request = urllib2.urlopen(url)
    response = request.read()
    responseJson = json.loads(response)
    return responseJson['Data']

def indicatorData(indicatorID):
    indicatorURL = '{0}/{1}?f=json&perpage=1000'.format(source, indicatorID)
    request = urllib2.urlopen(indicatorURL)
    response = request.read()
    responseJson = json.loads(response)
    data = responseJson['Data']
    if responseJson['TotalPages'] > 1:
        totalPages = responseJson['TotalPages']
        thisPage = 2
        while thisPage <= totalPages:
            indicatorURL = '{0}/{1}?f=json&page={2}&perpage=1000'.format(source, indicatorID, str(thisPage))
            request = urllib2.urlopen(indicatorURL)
            response = request.read()
            responseJson = json.loads(response)
            data.extend(responseJson['Data'])
            thisPage = thisPage + 1
    return data

def writeOut(inputData, outputFile):
    fieldNames = inputData[0].keys()
    with open(outputFile, 'w') as outFile:
        writer = csv.DictWriter(outFile, fieldnames=fieldNames)
        writer.writeheader()
        writer.writerows(inputData)

def main(outDir = 'D:\\sdg\\dhs\\dhsData'):
    indicators = getIndicators()
    ctr = 0
    for indicator in indicators:
        indID = indicator['IndicatorId']
        print(indID)
        perIndicator = indicatorData(indID)
        if perIndicator:
            writeOut(perIndicator, '{0}\\{1}.csv'.format(outDir, indID))

if __name__ == '__main__':
    main()
