import codecs
from cdliconll2conllu.mapping import Mapping
import os
import click

class CoNLLU_to_Cdli_CoNLL:
    
    def __init__ (self, cdli__conllu_filepath, conllu_filepath):
        self.cdli__conllu_filepath = cdli__conllu_filepath
        self.conllu_filepath = conllu_filepath
        self.cl = Mapping()
        #self.jsonData = json.load(open("mapping.json"))
        self.output_file_path = self.cdli__conllu_filepath.split("/")[-1].split(".")[0] + "_new.conll"
        output_folder = os.path.join(os.path.dirname(self.conllu_filepath) , "output_me")
        self.outFolder = os.path.join('', output_folder)
        self.outputFileName = ''



    def ids_dict(self):
        ids = dict()
        col_1_4 = list()
        ids["0"] = "0"
        with codecs.open(self.cdli__conllu_filepath, 'r', 'utf-8') as openedCDLICoNLLFile:
            count = 1
            for line in openedCDLICoNLLFile:
                line = line.strip()
                if(len(line)==0):
                    continue
                if line[0] != '#':
                    line = line.split("\t")
                    ids[str(count)] = line[0]
                    count += 1
                    col_1_4.append(line[0:4])

        return ids, col_1_4

    def update_head(self):
        
        run_ids_dict = self.ids_dict()
        id_dict = run_ids_dict[0]
        col_1_4 = run_ids_dict[1]
        
        self.headerLines = list()
        self.outputLines = list()
        count = 0
        with codecs.open(self.conllu_filepath, 'r', 'utf-8') as openedCDLICoNLLFile:
            for line in openedCDLICoNLLFile:
                line = line.strip()
                if(len(line)==0):
                    continue
                if line[0] != '#':
                    line = line.split("\t")
                    #print(line)
                    if line[6] not in id_dict.keys():
                        new_var = line[6]
                    else:
                        new_var = id_dict[line[6]]
                    line[6] = new_var
                    new_line = col_1_4[count] + line[6:9]
                    self.outputLines.append(new_line)
                    count += 1
                else:
                    self.headerLines.append(line)
        


    def write_new_file(self):
        
        self.update_head()

        self.outputFileName = os.path.join(self.outFolder, os.path.basename(self.output_file_path))

        if not os.path.exists(self.outFolder):
            click.echo('\nInfo: Creating folder at {0} as it does not exist.'.format(self.outFolder))
            os.makedirs(self.outFolder)
        
        with codecs.open(self.outputFileName, 'w+', 'utf-8') as outputFile:
            textNumber = self.headerLines[0]
            textNumber = textNumber + '\n'
            outputFile.writelines(textNumber)
            header = '\t'.join(self.cl.cdliConllFields)
            header = '#' + header + '\n'
            outputFile.writelines(header)

            for line in self.outputLines:
                l = '\t'.join(line)
                l = l + '\n'
                outputFile.writelines(l)
            endLine = '\n'
            outputFile.writelines(endLine)
