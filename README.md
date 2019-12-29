# RegisterPrinter

## How to run
### install dependencies
`pip install -r requirements.txt`
### Usage
```
usage: python -m register_printer [-h] -f CONFIG_FILE_NAME -p EXCEL_FILES_PATH
                                  [-o OUTPUT_PATH] [-d] [-c] [-u] [-r] [-a]

optional arguments:
  -h, --help           show this help message and exit
  -f CONFIG_FILE_NAME  Configuration input filename.
  -p EXCEL_FILES_PATH  Directory path of Excel source files.
  -o OUTPUT_PATH       Output path of generated files. Default "."
  -d                   Generate register documents.
  -c                   Generate register C header files.
  -u                   Generate register UVM models.
  -r                   Generate register RTL module.
  -a                   Generate all files, same as -d -c -u -r
```
