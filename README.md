# CDLI-CoNLL-to-CoNLLU-Converter

## Description
This tool converts a CDLI-CoNLL file to a CoNLL-U file.

More information on the CDLI-CoNLL file format can be found [here] (https://cdli-gh.github.io/guide_overview.html).

More information on the CONLL-U file format can be found [here] (http://universaldependencies.org/format.html).

## Using the Tool 

### Installation
If you don't have pip installed on your system, please find the instructions [here] (https://pip.pypa.io/en/stable/installing/).

To install this converter, you can run the following commands:

```
pip install git+https://github.com/cdli-gh/CDLI-CoNLL-to-CoNLLU-Converter.git
```

### Upgrading
To upgrade this tool, you can run the following commands:

```
pip install git+https://github.com/cdli-gh/CDLI-CoNLL-to-CoNLLU-Converter.git --upgrade
```

### Execution
To use/execute this tool, run one of the following commands:

```
cdliconll2conllu -i input_file_name.txt
```

To see processing messages on the console, use the verbose option:
```
cdliconll2conllu -i input_file_name.txt -v
```
OR
```
cdliconll2conllu -i input_file_name.txt --verbose
```

To view all possible options, use the --help option:
```
cdliconll2conllu --help
```
If you don't use any arguments, it will prompt for the input file path as follows:
```
cdliconll2conllu
Input path: input.txt
```
