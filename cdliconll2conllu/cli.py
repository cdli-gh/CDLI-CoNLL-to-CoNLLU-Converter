import os
import click
from stat import ST_MODE, S_ISREG

from cdliconll2conllu.converter import CdliCoNLLtoCoNLLUConverter
from cdliconll2conllu.conllu_to_cdli_conll import CoNLLU_to_Cdli_CoNLL


def file_process(cdliconllInFile, output_folder, verbose=False):
    convertor = CdliCoNLLtoCoNLLUConverter(cdliconllInFile, output_folder, verbose)
    convertor.convert()
    convertor.writeToFile()

def to_cdli_conllu(file_process_output_file , cdliconllInFile):
    convertor_2 = CoNLLU_to_Cdli_CoNLL(file_process_output_file, cdliconllInFile)
    convertor_2.write_new_file()


def check_and_process(pathname, output_folder, input_path_with_sytnax, verbose=False):
    mode = os.stat(pathname)[ST_MODE]

    if S_ISREG(mode) and pathname.lower().endswith('.conll'):
        # It's a file, call the callback function
        if verbose:
            click.echo('\nInfo: Processing {0}.'.format(pathname))

        cdliConllFile = pathname

        t = pathname.split('.')
        # conllFilePath = str(t[0]) + '.conll'

        # if not os.path.exists(conllFilePath):
        #     click.echo("Error: CoNLL file doesn't exist")

        file_process(cdliConllFile, output_folder, verbose)
        #file_process(cdliConllFile, output_folder, verbose)

        to_cdli_conllu(cdliConllFile, input_path_with_sytnax )




@click.command()
@click.option('--input_path', '-i', type=click.Path(exists=True, writable=True), prompt=True, required=True, multiple = True, 
              help='Input the file/folder name.')
@click.option('--input_path_with_sytnax', '-s', type=click.Path(exists=True, writable=True), prompt=True, required=True,
              help='Input the conllu file/folder name.')

@click.option('--verbose', '-v', default=False, required=False, is_flag=True, help='Enables verbose mode')
@click.option('--output_folder', '-o', default=None, type=click.Path(), required=False, help='Used to specify the output folder.')
@click.version_option()

def main(input_path, output_folder, verbose, input_path_with_sytnax):
    if os.path.isdir(input_path):
        with click.progressbar(os.listdir(input_path), label='Info: Converting the files') as bar:
            for f in bar:
                pathname = os.path.join(input_path, f)

                check_and_process(pathname, output_folder, input_path_with_sytnax, verbose)
    else:
        check_and_process(input_path, output_folder, verbose)

if __name__=='__main__':
    main()