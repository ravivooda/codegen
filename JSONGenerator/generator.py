import json
import templates
import os

def createFileWithName(name):
	if not os.path.exists("output"):
		os.makedirs("output")
	file = open("output/" + name + ".py", "w+")
	return file

def deflateArray(jsonArray):
	if not jsonArray:
		return []
	if not isinstance(jsonArray[0], list):
		return jsonArray
	return jsonArray

def generateFileForJSONArray(jsonArray, nameOfFile):
	if not jsonArray:
		return
	# Creating combiend JSONObject
	jsonObject = {}
	jsonArray = deflateArray(jsonArray)
	for element in jsonArray:
		for dictObject, value in element.iteritems():
			jsonObject[dictObject] = value;
	return generateFileForJSONObject(jsonObject, nameOfFile)

def nextLevelName(currentName, key):
	return currentName + str(key).capitalize()

def getUniqueStringsInArray(stringsArray):
	check = {}
	returnArray = []
	for string in stringsArray:
		if string in check:
			continue
		returnArray.append(string)
		check[string] = True
	return returnArray

def getTextForClass(importStrings, className, propertiesArray, parsingStringsArray, jsonObject):
	classPropertiesPrinting = ""
	for property in propertiesArray:
		classPropertiesPrinting += templates.ClassPropertyPrintingTemplate % (property, property)
	classPrintingString = templates.ClassPrintingTemplate %(className, classPropertiesPrinting)

	importStringsPrinting = ""
	importStrings = getUniqueStringsInArray(importStrings)
	for string in importStrings:
		importStringsPrinting += templates.ImportTemplate % (string, string)

	return templates.classTemplate % (importStringsPrinting, className, stringsFromClassProperties(propertiesArray), stringsFromParsingStrings(parsingStringsArray), classPrintingString, jsonObject, className)

def generateFileForJSONObject(jsonObject, nameOfFile):
	classProperties = []
	parsingStrings = []
	importStrings = []
	for key,value in jsonObject.iteritems():
		newName = nextLevelName(nameOfFile, key)
		if isinstance(value, list):
			if not value:
				continue
			elif isinstance(value[0], dict):
				importStrings.append(generateFileForJSONArray(value, newName))
				classProperties.append(key)
				parsingStrings.append(templates.ArrayParsingTemplate % (key, key, newName, key))
			else:
				classProperties.append(key)
				parsingStrings.append(templates.SimpleArrayParsingTemplate % (key, key, key))
		elif isinstance(value, dict):
			importStrings.append(generateFileForJSONObject(value, newName))
			classProperties.append(key)
			parsingStrings.append(templates.DictionaryParsingTemplate % (key, newName, key, key))
		else:
			classProperties.append(key)
			parsingStrings.append(templates.SimpleParsingTemplate %(key, key))

	classText = getTextForClass(importStrings, nameOfFile, classProperties, parsingStrings, jsonObject)
	classFile = createFileWithName(nameOfFile)
	classFile.write(classText)
	classFile.close()
	return nameOfFile

def stringsFromClassProperties(classProperties):
	return "\n\t\tpass"

def stringsFromParsingStrings(parsingStrings):
	if not parsingStrings:
		return "\n\t\tpass"
	retString = ""
	for string in parsingStrings:
		retString += string
	return retString

def generateFilesForJSONString(string, name):
	jsonObject = json.loads(string)
	generateFileForJSONObject(jsonObject, name);

if __name__ == "__main__":
	jsonString = '''{"optionChain":{"result":[{"underlyingSymbol":"APRN","expirationDates":[1525996800,1526601600,1527206400,1527811200,1528416000,1529020800,1529625600,1530230400,1532044800,1539907200,1547769600,1579219200],"strikes":[1.5,2.0,2.5,3.0,3.5,4.5],"hasMiniOptions":false,"quote":{"language":"en-US","quoteType":"EQUITY","quoteSourceName":"Nasdaq Real Time Price","currency":"USD","longName":"Blue Apron Holdings, Inc.","financialCurrency":"USD","averageDailyVolume3Month":4063967,"averageDailyVolume10Day":6921600,"fiftyTwoWeekLowChange":0.73,"fiftyTwoWeekLowChangePercent":0.4244186,"fiftyTwoWeekRange":"1.72 - 11.0","fiftyTwoWeekHighChange":-8.55,"fiftyTwoWeekHighChangePercent":-0.77727276,"esgPopulated":false,"tradeable":true,"priceHint":2,"market":"us_market","regularMarketPrice":2.45,"regularMarketTime":1526046799,"regularMarketChange":-0.00999999,"regularMarketOpen":2.4,"regularMarketDayHigh":2.41,"regularMarketDayLow":2.4,"regularMarketVolume":408813,"shortName":"Blue Apron Holdings, Inc. Class","exchange":"NYQ","forwardPE":-5.8333335,"exchangeDataDelayedBy":0,"sharesOutstanding":57748400,"fiftyTwoWeekLow":1.72,"fiftyTwoWeekHigh":11.0,"earningsTimestamp":1525350600,"priceToBook":2.0940173,"sourceInterval":15,"exchangeTimezoneName":"America/New_York","exchangeTimezoneShortName":"EDT","gmtOffSetMilliseconds":-14400000,"bookValue":1.17,"fiftyDayAverage":2.0622857,"fiftyDayAverageChange":0.3877144,"regularMarketChangePercent":-0.40650368,"regularMarketDayRange":"2.4 - 2.41","regularMarketPreviousClose":2.46,"bid":2.44,"ask":2.45,"bidSize":2,"askSize":15,"messageBoardId":"finmb_428879292","fullExchangeName":"NYSE","marketState":"REGULAR","fiftyDayAverageChangePercent":0.18800227,"twoHundredDayAverage":3.0613043,"twoHundredDayAverageChange":-0.6113043,"twoHundredDayAverageChangePercent":-0.19968753,"marketCap":469836512,"epsTrailingTwelveMonths":-1.641,"epsForward":-0.42,"symbol":"APRN"},"options":[{"expirationDate":1525996800,"hasMiniOptions":false,"calls":[{"contractSymbol":"APRN180511C00001500","strike":1.5,"currency":"USD","lastPrice":1.1,"change":0.0,"percentChange":0.0,"volume":1,"openInterest":1,"bid":0.75,"ask":1.05,"contractSize":"REGULAR","expiration":1525996800,"lastTradeDate":1525703344,"impliedVolatility":10.312503554687503,"inTheMoney":true},{"contractSymbol":"APRN180511C00002000","strike":2.0,"currency":"USD","lastPrice":0.4,"change":0.0,"percentChange":0.0,"volume":878,"openInterest":940,"bid":0.3,"ask":0.55,"contractSize":"REGULAR","expiration":1525996800,"lastTradeDate":1525978904,"impliedVolatility":5.7812527734375,"inTheMoney":true},{"contractSymbol":"APRN180511C00002500","strike":2.5,"currency":"USD","lastPrice":0.05,"change":0.0,"percentChange":0.0,"volume":145,"openInterest":558,"bid":0.0,"ask":0.05,"contractSize":"REGULAR","expiration":1525996800,"lastTradeDate":1525981462,"impliedVolatility":0.87500125,"inTheMoney":false},{"contractSymbol":"APRN180511C00003000","strike":3.0,"currency":"USD","lastPrice":0.05,"change":0.0,"percentChange":0.0,"volume":10,"openInterest":390,"bid":0.0,"ask":0.05,"contractSize":"REGULAR","expiration":1525996800,"lastTradeDate":1525959398,"impliedVolatility":3.1875020312499998,"inTheMoney":false},{"contractSymbol":"APRN180511C00003500","strike":3.5,"currency":"USD","lastPrice":0.03,"change":0.0,"percentChange":0.0,"volume":1,"openInterest":23,"bid":0.0,"ask":0.05,"contractSize":"REGULAR","expiration":1525996800,"lastTradeDate":1525959141,"impliedVolatility":4.7500040624999995,"inTheMoney":false},{"contractSymbol":"APRN180511C00004500","strike":4.5,"currency":"USD","lastPrice":0.05,"change":0.0,"percentChange":0.0,"volume":1,"openInterest":1,"bid":0.0,"ask":0.05,"contractSize":"REGULAR","expiration":1525996800,"lastTradeDate":1525491954,"impliedVolatility":7.00000125,"inTheMoney":false}],"puts":[{"contractSymbol":"APRN180511P00001500","strike":1.5,"currency":"USD","lastPrice":0.05,"change":0.020000001,"percentChange":66.66667,"volume":3,"openInterest":104,"bid":0.0,"ask":0.05,"contractSize":"REGULAR","expiration":1525996800,"lastTradeDate":1525441337,"impliedVolatility":6.7500015625000005,"inTheMoney":false},{"contractSymbol":"APRN180511P00002000","strike":2.0,"currency":"USD","lastPrice":0.05,"change":0.0,"percentChange":0.0,"volume":22,"openInterest":352,"bid":0.0,"ask":0.05,"contractSize":"REGULAR","expiration":1525996800,"lastTradeDate":1525447813,"impliedVolatility":3.3750015624999996,"inTheMoney":false},{"contractSymbol":"APRN180511P00002500","strike":2.5,"currency":"USD","lastPrice":0.1,"change":0.0,"percentChange":0.0,"volume":117,"openInterest":64,"bid":0.0,"ask":0.15,"contractSize":"REGULAR","expiration":1525996800,"lastTradeDate":1525982253,"impliedVolatility":0.87500125,"inTheMoney":true},{"contractSymbol":"APRN180511P00003000","strike":3.0,"currency":"USD","lastPrice":0.55,"change":0.0,"percentChange":0.0,"volume":42,"openInterest":89,"bid":0.45,"ask":0.75,"contractSize":"REGULAR","expiration":1525996800,"lastTradeDate":1525978322,"impliedVolatility":3.968750078125,"inTheMoney":true},{"contractSymbol":"APRN180511P00003500","strike":3.5,"currency":"USD","lastPrice":0.7,"change":0.0,"percentChange":0.0,"volume":3,"openInterest":0,"bid":0.95,"ask":1.25,"contractSize":"REGULAR","expiration":1525996800,"lastTradeDate":1526044837,"impliedVolatility":5.7500028125,"inTheMoney":true}]}]}],"error":null}}'''
	generateFilesForJSONString(jsonString, "Calls")