import json
import templates
import os

def createFileWithName(name):
	if not os.path.exists("output"):
		os.makedirs("output")
	file = open("output/" + name + ".py", "w+")
	return file

def generateFileForJSONArray(jsonArray, nameOfFile):
    pass

def nextLevelName(currentName, key):
    return currentName + str(key).capitalize()

def getTextForClass(className, propertiesArray, parsingStringsArray, jsonObject):
	classPropertiesPrinting = ""
	for property in propertiesArray:
		classPropertiesPrinting += templates.ClassPropertyPrintingTemplate % (property, property)
	classPrintingString = templates.ClassPrintingTemplate %(className, classPropertiesPrinting)
	return templates.classTemplate % (className, stringsFromClassProperties(propertiesArray), stringsFromParsingStrings(parsingStringsArray), classPrintingString, jsonObject, className)

def generateFileForJSONObject(jsonObject, nameOfFile):
    classProperties = []
    parsingStrings = []
    #print jsonObject
    for key,value in jsonObject.iteritems():
    	newName = nextLevelName(nameOfFile, key)
        if isinstance(value, list):
            generateFileForJSONArray(value, newName)
            classProperties.append(key)
            parsingStrings.append(templates.ArrayParsingTemplate % (key, key, newName, key))
        elif isinstance(value, dict):
            generateFileForJSONObject(value, nextLevelName(nameOfFile, key))
            classProperties.append(key)
            parsingStrings.append('''
            		self.%s = %s()
            		self.%s.parse(jsonObject['%s'])''' % (key, newName, key, key))
        else:
        	classProperties.append(key)
        	parsingStrings.append(templates.SimpleParsingTemplate %(key, key))

    classText = getTextForClass(nameOfFile, classProperties, parsingStrings, jsonObject)
    classFile = createFileWithName(nameOfFile)
    classFile.write(classText)
    classFile.close()

def stringsFromClassProperties(classProperties):
	return "pass"

def stringsFromParsingStrings(parsingStrings):
	if not parsingStrings:
		return "pass"
	retString = ""
	for string in parsingStrings:
		retString += string
	return retString

if __name__ == "__main__":
	jsonObject = {
	"ask": 1.05,
	"bid": 0.75,
	"change": 0,
	"contractSize": "REGULAR",
	"contractSymbol": "APRN180511C00001500",
	"currency": "USD",
	"expiration": 1525996800,
	"impliedVolatility": 10.312503554687503,
	"inTheMoney": True,
	"lastPrice": 1.1,
	"lastTradeDate": 1525703344,
	"openInterest": 1,
	"percentChange": 0,
	"strike": 1.5,
	"volume": 1
	}
	generateFileForJSONObject(jsonObject, 'Calls');