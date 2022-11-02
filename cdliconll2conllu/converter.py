#!/usr/bin/env python
import codecs
from itertools import count
import click
import os
from cdliconll2conllu.mapping import Mapping
import sys
import random

OUTPUT_FOLDER = 'output_2'


class CdliCoNLLtoCoNLLUConverter:

    def __init__(self, cdliCoNLLInputFileName, output_folder, verbose):
        self.cdliCoNLLInputFileName = cdliCoNLLInputFileName

        # path = os.path.abspath(cdliCoNLLInputFileName)
        # newPath = path[:len(path) - len(cdliCoNLLInputFileName)]
        # self.outFolder = newPath + OUTPUT_FOLDER

        if(output_folder==None or os.path.samefile(output_folder,os.path.dirname(self.cdliCoNLLInputFileName))):
            output_folder = os.path.join(os.path.dirname(self.cdliCoNLLInputFileName), OUTPUT_FOLDER)
        self.outFolder = os.path.join('', output_folder)
        self.verbose = verbose
        self.cl = Mapping()
        self.headerLines = list()
        self.outputFileName = ''
        self.__reset__()

    def __reset__(self):
        self.outputFileName = ''
        self.outputLines = list()

    def convert(self):
        if self.verbose:
            click.echo('\nInfo: Reading file {0}.'.format(self.cdliCoNLLInputFileName))

        with codecs.open(self.cdliCoNLLInputFileName, 'r', 'utf-8') as openedCDLICoNLLFile:
            inputLines = list()

            for line in openedCDLICoNLLFile:
                line = line.strip()
                if(len(line)==0):
                    continue
                if line[0] != '#':
                    line = line.split("\t")
                    inputLines.append(line)
                else:
                    self.headerLines.append(line)
            try:
                self.convertCDLICoNLLtoCoNLLU(inputLines)
            except:
                pass


    def get_head_dict(self,inputLines):
        N = len(inputLines)
        head_dict = dict()
        counter = 1
        for line in inputLines:
            try:
                head_dict[line[0]] = str(counter)
                counter+=1
            except:
                pass
        
        return head_dict


    def convertCDLICoNLLtoCoNLLU(self, inputLines):
        counter = 1
        head_dict = self.get_head_dict(inputLines)
        #print(head_dict)
        # total_lines = len(inputLines)

        for line in inputLines:
            inputList = line
            inputData = dict()

            if len(inputList) > len(self.cl.cdliConllFields):
                click.echo("\nIncorrect File Format in file {0} for line {1}.".format(self.cdliCoNLLInputFileName, line))
                pass
            else:
                while len(inputList) != len(self.cl.cdliConllFields):
                    inputList.append("_")

            for i in range(len(self.cl.cdliConllFields)):
                inputData[self.cl.cdliConllFields[i]] = inputList[i]

            result = dict()


            #result['ID'] = inputData['ID'] # The old ID, e.g. 'r.4.1'
            #result['ID'] = inputData['ID'].split('.')[-1]
            result['ID'] = str(counter)
            counter+=1
            
            result['FORM'] = inputData['FORM']

            if inputData['SEGM'] == '_':
                result['LEMMA'] = '_'
            else:
                segm = inputData['SEGM']
                position = segm.find(']')
                start = segm.rfind('-', 0, position + 1)
                result['LEMMA'] = segm[start + 1: (position + 1)]
                if result['LEMMA'] == '':
                    errorLine = '\t'.join(line)
                    click.echo(
                        "\nIncorrect Segment at Line '{0}' in file {1}.".format(errorLine, self.cdliCoNLLInputFileName))
                    pass

            if inputData['XPOSTAG'] == '_':
                result['UPOSTAG'] = '_'
                result['XPOSTAG'] = '_'
                result['FEATS'] = '_'
            else:
                xpostag = inputData['XPOSTAG'].split('.')
                intersected_xpostag = list(set(xpostag).intersection(set(self.cl.xPosTag.keys())))
                if len(intersected_xpostag)==0:
                    result['UPOSTAG'] = '_'
                    result['XPOSTAG'] = '_'
                    result['FEATS'] = '_'
                    errorLine = '\t'.join(line)
                    click.echo("\nIncorrect Segment at Line at line: '{0}' in file {1}.".format(errorLine,
                                                                                                             self.cdliCoNLLInputFileName))
                else:
                    typeCDLICoNLL = intersected_xpostag[0]
                    result['UPOSTAG'] = self.cl.xPosTag[typeCDLICoNLL]
                    result['XPOSTAG'] = typeCDLICoNLL
                    xpostag.pop(xpostag.index(typeCDLICoNLL))

                    upostag = self.cl.xPosTag[typeCDLICoNLL]
                    feats = dict()
                    featList = list(xpostag)

                    # animacy Hum Mapping to PN, DN, RN
                    HumPos = ['PN', 'DN', 'RN']
                    if typeCDLICoNLL in HumPos:
                        feats['Animacy'] = 'Hum'

                    # print(featList)
                    # default mapping
                    defaults = list()
                    if upostag in self.cl.defaultMap:
                        for feature in self.cl.defaultMap[upostag]:
                            feats[feature] = self.cl.defaultMap[upostag][feature]
                            defaults.append(feature)
                    # print(defaults)
                    # remaining mapping
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
                                        # check if multiple entries allowed
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
                    if feature == '':
                        result['FEATS'] = '_'
                    else:
                        result['FEATS'] = feature

            # result['HEAD'] = inputData['HEAD']
            # result['HEAD'] = str(counter)
            # if total_lines+1 == counter:
            #     result['HEAD'] = "0"

            try:
                result['HEAD'] = head_dict[inputData['HEAD']]
            except:
                result['HEAD'] = "_"

            result['DEPREL'] = inputData['DEPREL']
            result['DEPS'] = '_'
            result['MISC'] = inputData['MISC']

            output = list()

            for field in self.cl.conllUFields:
                output.append(result[field])

            self.outputLines.append(output)

    def writeToFile(self):
        self.outputFileName = os.path.join(self.outFolder, os.path.basename(self.cdliCoNLLInputFileName))
        if self.verbose:
            click.echo('\nInfo: Creating output at {0}.'.format(self.outputFileName))
        if not os.path.exists(self.outFolder):
            click.echo('\nInfo: Creating folder at {0} as it does not exist.'.format(self.outFolder))
            os.makedirs(self.outFolder)
        with codecs.open(self.outputFileName, 'w+', 'utf-8') as outputFile:
            textNumber = self.headerLines[0]
            textNumber = textNumber + '\n'
            outputFile.writelines(textNumber)
            header = '\t'.join(self.cl.conllUFields)
            header = '#' + header + '\n'
            outputFile.writelines(header)

            for line in self.outputLines:
                l = '\t'.join(line)
                l = l + '\n'
                outputFile.writelines(l)
            endLine = '\n'
            outputFile.writelines(endLine)
