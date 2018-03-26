#!/usr/bin/env python
import codecs
import click
import os
from cdliconll2conllu.mapping import mapping
import re

OUTPUT_FOLDER = 'output'

class cdliCoNLLtoCoNNLUConverter:

    def __init__(self, cdliCoNLLInputFileName, verbose):
        self.cdliCoNLLInputFileName = cdliCoNLLInputFileName

        path = os.path.abspath(cdliCoNLLInputFileName)
        newPath = path[:len(path) - len(cdliCoNLLInputFileName)]
        self.outFolder = newPath + OUTPUT_FOLDER

        # self.outFolder = os.path.join('', OUTPUT_FOLDER)
        self.verbose = verbose
        self.cl = mapping()
        self.__reset__()

    def __reset__(self):
        self.outputFileName = ''
        self.outputLines = list()

    def convert(self):
        if self.verbose:
            click.echo('Info: Reading file {0}.'.format(self.cdliCoNLLInputFileName))

        with codecs.open(self.cdliCoNLLInputFileName) as openedCDLICoNLLFile:
            inputLines = list()

            for line in openedCDLICoNLLFile:
                line = line.strip()
                if line[0] != '#':
                    line = line.split()
                    inputLines.append(line)

            self.convertCDLICoNLLtoCoNLLU(inputLines)


    def convertCDLICoNLLtoCoNLLU(self, inputLines):

        # print(inputLines)
        for line in inputLines:
            inputList = line
            inputData = dict()
            print(line)
            for i in range(len(self.cl.cdliConllFields)):
                inputData[self.cl.cdliConllFields[i]] = inputList[i]

            result = dict()

            result['ID'] = inputData['ID']
            result['FORM'] = inputData['FORM']

            if inputData['SEGM'] == '_':
                result['LEMMA'] = '_'
            else:
                segm = inputData['SEGM']
                position = segm.find(']')
                start = segm.rfind('-', 0, position + 1)
                result['LEMMA'] = segm[start + 1: (position + 1)]

            if inputData['XPOSTAG'] == '_':
                result['UPOSTAG'] = '_'
                result['XPOSTAG'] = '_'
                result['FEATS'] = '_'
            else:
                xpostag = inputData['XPOSTAG'].split('.')
                typeCDLICoNLL = list(set(xpostag).intersection(set(self.cl.xPosTag.keys())))[0]
                result['UPOSTAG'] = self.cl.xPosTag[typeCDLICoNLL]
                result['XPOSTAG'] = typeCDLICoNLL
                xpostag.pop(xpostag.index(typeCDLICoNLL))

                upostag = self.cl.xPosTag[typeCDLICoNLL]
                feats = dict()
                featList = xpostag.copy()

                #animacy Hum Mapping to PN, DN, RN
                HumPos = ['PN', 'DN', 'RN']
                if typeCDLICoNLL in HumPos:
                    feats['Animacy'] = 'Hum'

                # print(featList)
                #default mapping
                defaults = list()
                if upostag in self.cl.defaultMap:
                    for feature in self.cl.defaultMap[upostag]:
                        feats[feature] = self.cl.defaultMap[upostag][feature]
                        defaults.append(feature)
                #print(defaults)
                #remaining mapping
                for item in featList:
                    # print(item)
                    if item.find('-') != -1:
                        # print(item)
                        found = False
                        for feat in self.cl.posToFeatsMap[upostag]:
                            if item in self.cl.featsMap[feat]:
                                if feat in feats:
                                    if feat in defaults:
                                        feats[feat] = self.cl.featsMap[feat][item]
                                        defaults.pop(defaults.index(feat))
                                    #check if multiple entries allowed
                                    if feat in self.cl.multiList:
                                        combinedEntry = str(feats[feat]) + "," + str(self.cl.featsMap[feat][item])
                                        feats[feat] = combinedEntry
                                        found = True
                                else:
                                    feats[feat] = self.cl.featsMap[feat][item]
                                    found = True
                        if found == False:
                            splitItem = item.split('-')
                            featList += splitItem
                            # print(featList)
                    else:
                        for feat in self.cl.posToFeatsMap[upostag]:
                            if item in self.cl.featsMap[feat]:
                                if feat not in feats:
                                    feats[feat] = self.cl.featsMap[feat][item]
                                else:
                                    if feat in defaults:
                                        feats[feat] = self.cl.featsMap[feat][item]
                                        defaults.pop(defaults.index(feat))
                                    if feat in self.cl.multiList:
                                        combinedEntry = str(feats[feat]) + "," + str(self.cl.featsMap[feat][item])
                                        feats[feat] = combinedEntry
                                        found = True
                    # print(feats)
                feature = ''
                for key, value in feats.items():
                    feature = feature + key + '=' + value + '|'

                feature = feature[:-1]
                result['FEATS'] = feature

            result['HEAD'] = inputData['HEAD']
            result['DEPREL'] = inputData['DEPREL']
            result['MISC'] = inputData['MISC']

            output = list()

            for field in self.cl.conllUFields:
                output.append(result[field])

            self.outputLines.append(output)


    def writeToFile(self):
        filename = re.split('[/ .]', self.cdliCoNLLInputFileName)
        self.outputFileName = filename[-2]
        outFileName = os.path.join(self.outFolder, self.outputFileName + ".conll")

        with codecs.open(outFileName, 'w+', 'utf-8') as outputFile:
            header = '\t'.join(self.cl.conllUFields)
            header = header + '\n'
            outputFile.writelines(header)

            for line in self.outputLines:
                l = '\t'.join(line)
                l = l + '\n'
                outputFile.writelines(l)
