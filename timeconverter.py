#This script takes a user input UNIX formatted time (epoch format) and outputs a human-readable time
#!/usr/bin/python

import argparse
import datetime
import pytz
import sys

__author__ = 'Gavin Lau'
__date__ = '20180206'
__version__ = '1.0'

#Passing inputs to different methods depending on the input
def timeConverter(hrFormat, timezone, timestamp):
	#Convert timestamp to UTC readable time
	UTCTime = (defaultConverter(timestamp))

	#Check if user entered the correct hr format
	if hrFormat != 12 and hrFormat != 24:
		print 'Hour format entered is incorrect!'
		sys.exit(0)

	# '-t 24' only
	if hrFormat == 24 and timezone == 'UTC':
		return(twoFourHrConverter(timezone, UTCTime))

	# '-z timezone' only
	elif hrFormat == 12 and timezone != 'UTC':
		return oneTwoHrConverter(timezone, timezoneConverter(UTCTime, timezoneCheck(timezone, 100)))

	# '-t 24 -z zone'
	elif hrFormat == 24 and timezone != 'UTC':
		return twoFourHrConverter(timezone, timezoneConverter(UTCTime, timezoneCheck(timezone, 100)))

	#Else convert to default
	else:
		return UTCTime.strftime('%d-%m-%Y %I:%M:%S:%p'+' '+timezone)
	
#Use %H for 24 hour format, or %I with %p for 12 hour format with AM/PM
def defaultConverter(timestamp):
	date_ts = datetime.datetime.utcfromtimestamp(timestamp)
	return date_ts

#Get timezone offset depending on user's timezone input
def timezoneCheck(timezone, offset):
	#timezone list
	tz = [[['GMT', 'UTC', 'WET'], [0]], [['CET', 'MET', 'WAT', 'WEST'], [+1]],
		  [['CAT', 'EET', 'IST', 'SAST', 'USZ1'], [+2]], [['EAT', 'FET', 'IOT', 'MSK', 'SYOT', 'TRT'], [+3]],
		  [['AZT', 'GET', 'MUT', 'RET', 'SAMT', 'SCT', 'VOLT'], [+4]],
		  [['HMT', 'MAWT', 'MVT', 'ORAT', 'PKT', 'TFT', 'TJT', 'TMT', 'UZT', 'YEKT'], [+5]],
		  [['BIOT', 'BST', 'BTT', 'KGT', 'OMST', 'VOST'], [+6]],
		  [['CXT', 'DAVT', 'HOVT', 'ICT', 'KRAT', 'THA', 'WIT'], [+7]],
		  [['AWST', 'BDT', 'CHOT', 'CIT', 'CT', 'HKT', 'IRKT', 'MYT', 'PHT', 'SGT', 'SST', 'ULAT', 'WST'], [+8]],
		  [['EIT', 'JST', 'TLT', 'YAKT'], [+9]], [['AEST', 'CHST', 'CHUT', 'DDUT', 'PGT', 'VLAT'], [+10]],
		  [['KOST', 'MIST', 'NCT', 'NFT', 'PONT', 'SAKT', 'SBT', 'SRET', 'VUT'], [+11]],
		  [['FJT', 'GILT', 'MAGT', 'MHT', 'NZST', 'PETT', 'TVT', 'WAKT'], [+12]],
		  [['PHOT', 'TKT', 'TOT'], [+13]], [['LINT'], [+14]], [['AZOT', 'CVT', 'EGT'], [-1]],
		  [['FNT', 'GST'], [-2]], [['ART', 'BRT', 'GFT', 'PMST', 'ROTT', 'UYT'], [-3]],
		  [['AMT', 'AST', 'BOT', 'CLT', 'FKT', 'GYT', 'PYT', 'VET'], [-4]],
		  [['ACT', 'COT', 'ECT', 'EST', 'PET'], [-5]], [['CST', 'EAST', 'GALT'], [-6]],
		  [['MST'], [-7]], [['CIST', 'PST'], [-8]], [['AKST', 'GAMT', 'GIT'], [-9]], [['CKT', 'HST', 'TAHT'], [-10]],
		  [['NUT'], [-11]], [['BIT'], [-12]]]
	#Check if user's timezone input is within the list
	for x in tz:
		#find the index of timzeone & get offset
		if x[0].count(timezone) == 1:
			offset=x[1].pop()

	#if timezone entered is not found, error message and exit
	if offset == 100:
		print 'Timezone entered cannot be found!'
		sys.exit(0)
	else:
		return offset

#Convert UTC date and time to different timezone
def timezoneConverter(newTime, offset):
	#Declare old Hour, Day, Month, Year
	oldTimeHour=newTime.hour
	oldTimeDay=newTime.day
	oldTimeMonth=newTime.month
	oldTimeYear=newTime.year

	#New Hour in different timezone
	newTimeHour=oldTimeHour+offset

	#Change time within one day
	if newTimeHour > 0 and newTimeHour < 24:
		newTime=newTime.replace(hour=newTimeHour)
		return newTime

	#Goes back one day
	if newTimeHour < 0:
		newTimeHour = newTimeHour+24
		newTime=newTime.replace(hour=newTimeHour)
		#Check the date and change
		#Regular
		if oldTimeDay != 1 and oldTimeMonth != 1:
			newTime=newTime.replace(hour=newTimeHour, day=oldTimeDay-1)
			return newTime
		#1st day of each month, goes back one month
		elif oldTimeDay == 1 and oldTimeMonth != 1:
			if oldTimeMonth == 5 or oldTimeMonth == 7 or oldTimeMonth == 10 or oldTimeMonth == 12:
				newTime=newTime.replace(hour=newTimeHour, day=30, month=oldTimeMonth-1)
				return newTime
			elif oldTimeMonth == 2 or oldTimeMonth == 4 or oldTimeMonth == 6 or oldTimeMonth == 8 or oldTimeMonth == 9 or oldTimeMonth == 11:
				newTime=newTime.replace(hour=newTimeHour, day=31, month=oldTimeMonth-1)
				return newTime
			else:
				newTime=newTime.replace(hour=newTimeHour, day=28, month=oldTimeMonth-1)
				return newTime
		#Jan 1st, goes back one year
		elif oldTimeDay == 1 and oldTimeMonth == 1:
			newTime=newTime.replace(hour=newTimeHour, day=31, month=12, year=oldTimeYear-1)
			return newTime

	#Goes forward one day
	elif newTimeHour > 24:
		newTimeHour = newTimeHour-24
		newTime=newTime.replace(hour=newTimeHour)

		#Check the date and change
		#Regular
		if (oldTimeDay != 31 and oldTimeDay != 28 and oldTimeDay != 30) and oldTimeMonth != 12:
			newTime=newTime.replace(hour=newTimeHour, day=oldTimeDay+1)
			return newTime
		#last day of each month, goes forward one month
		elif (oldTimeDay == 31 or oldTimeDay == 30 or oldTimeDay == 28) and oldTimeMonth != 12:
				newTime=newTime.replace(hour=newTimeHour, day=1, month=oldTimeMonth+1)
				return newTime
		#Dec 31st, goes forward one year
		elif oldTimeDay == 31 and oldTimeMonth == 12:
			newTime=newTime.replace(hour=newTimeHour, day=1, month=1, year=oldTimeYear+1)
			return newTime

#Convert to 24 hour format
def twoFourHrConverter(timezone, UTCTime):
	return UTCTime.strftime('%d-%m-%Y %H:%M:%S'+' '+timezone)

#UConvert to 12 hour format with AM/PM
def oneTwoHrConverter(timezone, UTCTime):
	return UTCTime.strftime('%d-%m-%Y %I:%M:%S %p'+' '+timezone)


	"""The unix_converter function uses the datetime library to convert the timestamp
	:parameter hourformat: An integer input for switching to 24 hour format.
	:parameter timezone: An String input for declaring timezone.
	:parameter timestamp: An integer representation of a UNIX timestamp.
	:return: A human-readable date & time string with timezone."""
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Time Converter')
    parser.add_argument('-t', type=int, default=12, help='Change to 24 hour format')
    parser.add_argument('-z', type=str, default='UTC', help='Timezone')
    parser.add_argument('UNIX_timestamp', type=int, help='Unix timestamp')
    args = parser.parse_args()
    print(timeConverter(args.t, args.z, args.UNIX_timestamp))