# RegisterPrinter

## How to install
`pip install register_printer`

## How to run
### install dependencies
`pip install -r requirements.txt`
### Usage
```
usage: python -m register_printer [-h] [-v]
                                  [-f CONFIG_FILE_NAME | --input-json INPUT_JSON_FILE]
                                  [-p EXCEL_FILES_PATH] [-o OUTPUT_PATH]
                                  [--print] [--verbose] [-d] [-c] [-u] [-j]
                                  [-r] [-x] [-a]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Display version
  -f CONFIG_FILE_NAME, --file CONFIG_FILE_NAME
                        Configuration input filename.
  --input-json INPUT_JSON_FILE
                        Input JSON documents.
  -p EXCEL_FILES_PATH   Directory path of Excel source files.
  -o OUTPUT_PATH, --output-path OUTPUT_PATH
                        Output path of generated files. Default "."
  --print               Print parsed document.
  --verbose             Logging more information.
  -d, --gen-doc         Generate register documents.
  -c, --gen-c-header    Generate register C header files.
  -u, --gen-uvm         Generate register UVM models.
  -j, --gen-json        Generate JSON documents.
  -r, --gen-rtl         Generate register RTL module.
  -x, --gen-excel       Generate excel files.
  -a, --gen-all         Generate all files, same as -d -c -u -r
```

## How to build
`python -m build`

## How to upload to pypi
`python -m twine upload dist/*`
