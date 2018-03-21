import json

class mapping:
    def __init__(self):

        #open json file containing mapping information and load it in a python object
        self.jsonFile = "mapping.json"
        self.jsonData = json.load(open(self.jsonFile))

        #create mappings and lists which will be used for conversion
        self.cdliConllFields = self.createCDLICoNLLFields()
        self.conllUFields = self.createCoNLLUFields()
        self.xPosTag = self.createXPosTagMapping()
        self.posToFeatsMap = self.createPosToFeatsMap()
        self.featsMap = self.createFeatsMap()
        self.defaultMap = self.createDefaults()
        self.multiList = self. createMultiList()

    def createCDLICoNLLFields(self):
        return self.jsonData['CDLI-CoNLL-Fields']

    def createCoNLLUFields(self):
        return self.jsonData['CoNLL-U-Fields']

    def createXPosTagMapping(self):
        return self.jsonData['xPOSTagMapping']

    def createPosToFeatsMap(self):
        return self.jsonData['posToFeatMapping']

    def createFeatsMap(self):
        return self.jsonData['featureMapping']

    def createDefaults(self):
        return self.jsonData['defaultFeature']

    def createMultiList(self):
        return self.jsonData['multipleFeatureEntries']
