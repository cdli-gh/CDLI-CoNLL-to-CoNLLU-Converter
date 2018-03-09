#!/usr/bin/env python
import codecs
import click
import os
import mapping as mp

OUTPUT_FOLDER = 'output'

class cdliCoNLLtoCoNNLUConverter:

    def __init__(self, cdliCoNLLInputFileName, verbose):
        self.cdliCoNLLInputFileName = cdliCoNLLInputFileName
        self.outFolder = os.path.join('', OUTPUT_FOLDER)
        self.verbose = verbose
        self.cl = mp.Mapping()
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
                line = line.split('\t')
                inputLines.append(line)

            self.convertCDLICoNLLtoCoNLLU(inputLines)


    def convertCDLICoNLLtoCoNLLU(self, inputLines):


        for line in inputLines:
            inputList = line.strip().split()
            inputData = dict()

            for i in range(self.cl.cdliConllFields):
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

                #default mapping
                if upostag in self.cl.defaultMap:
                    for feature in self.cl.defaultMap[upostag]:
                        feats[feature] = self.cl.defaultMap[upostag][feature]

                #remaining mapping
                for item in featList:
                    if item.find('-') != -1:
                        found = False
                        for feat in self.cl.posToFeatsMap[upostag]:
                            if item in self.cl.featsMap[feat]:
                                feats[feat] = self.cl.featsMap[feat][item]
                                found = True
                        if not found:
                            splitItem = item.split('-')
                            featList += splitItem
                    else:
                        for feat in self.cl.posToFeatsMap[upostag]:
                            if item in self.cl.featsMap[feat]:
                                feats[feat] = self.cl.featsMap[feat][item]

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
        outFileName = os.path.join(self.outFolder, self.outputFileName + ".conllU")

        with codecs.open(outFileName, 'w+', 'utf-8') as outputFile:
            header = '\t'.join(self.cl.conllUFields)
            outputFile.writelines(header)

            for line in self.outputLines:
                l = '\t'.join(line)
                outputFile.writelines(l)


