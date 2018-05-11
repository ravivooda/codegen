classTemplate = '''%s
class %s:
	# initializer
	def __init__(self):%s

	# parsing
	def parse(self, jsonObject):%s

	# printing class
	def __str__(self):%s


if __name__ == '__main__':
	jsonObject = %s
	test = %s()
	test.parse(jsonObject)
	print test
'''

ClassPrintingTemplate = '''
		return '%s: {' +\\%s
		'\\n}'
'''

ImportTemplate = '''from %s import %s
'''

ClassPropertyPrintingTemplate ='''
		'\\n\\t%s: ' + str(self.%s) +\\'''

ArrayParsingTemplate = '''
		self.%s = []
		for object in jsonObject['%s']:
			classObject = %s()
			classObject.parse(object)
			self.%s.append(classObject)'''

SimpleArrayParsingTemplate = '''
		self.%s = []
		for object in jsonObject['%s']:
			self.%s.append(object)
'''

DictionaryParsingTemplate = '''
		self.%s = %s()
		self.%s.parse(jsonObject['%s'])
'''

SimpleParsingTemplate = '''
		self.%s = jsonObject['%s']'''