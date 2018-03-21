import os
import click
from stat import ST_MODE, S_ISREG

from cdliconll2conllu.converter import cdliCoNLLtoCoNNLUConverter


def file_process(cdliconllInFile, verbose=False):
    outfolder = os.path.join('output')

    if not os.path.exists(outfolder):
        os.makedirs(outfolder)

    convertor = cdliCoNLLtoCoNNLUConverter(cdliconllInFile, verbose)
    convertor.convert()
    convertor.writeToFile()


def check_and_process(pathname, verbose=False):
    mode = os.stat(pathname)[ST_MODE]

    if S_ISREG(mode) and pathname.lower().endswith('.txt'):
        # It's a file, call the callback function
        if verbose:
            click.echo('Info: Processing {0}.'.format(pathname))

        cdliConllFile = pathname

        t = pathname.split('.')
        #conllFilePath = str(t[0]) + '.conll'

        # if not os.path.exists(conllFilePath):
        #     click.echo("Error: CoNLL file doesn't exist")

        file_process(cdliConllFile, verbose)


@click.command()
@click.option('--input_path', '-i', type=click.Path(exists=True, writable=True), prompt=True, required=True,
              help='Input the file/folder name.')
@click.option('-v', '--verbose', default=False, required=False, is_flag=True, help='Enables verbose mode')
@click.version_option()
def main(input_path, verbose):
    if os.path.isdir(input_path):
        with click.progressbar(os.listdir(input_path), label='Info: Converting the files') as bar:
            for f in bar:
                pathname = os.path.join(input_path, f)

                check_and_process(pathname, verbose)
    else:
        check_and_process(input_path, verbose)