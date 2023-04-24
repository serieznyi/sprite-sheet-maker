# spritesheets-maker

Python script to pack images to spritesheet

## Install

```commandline
pip install https://github.com/serieznyi/spritesheet-maker/archive/refs/heads/main.zip
```

## Usage

```shell
$ spritesheet-maker --help

usage: spritesheet-maker [-h] [--rows ROWS] [--columns COLUMNS] [--chunkSize CHUNKSIZE] [--logLevel {info,debug,warn}] sourceDir outputDir

                Generate spritesheet image
            

positional arguments:
  sourceDir             Directory with source images for spritesheet generating
  outputDir             Directory for result

options:
  -h, --help            show this help message and exit
  --rows ROWS           Columns count
  --columns COLUMNS     Rows count
  --chunkSize CHUNKSIZE
                        Split images from source dir on chunks
  --logLevel {info,debug,warn}
                        Logging level. Default: info

```

## References
 - [Making a simple sprite sheet generator in Python](https://minzkraut.com/2016/11/23/making-a-simple-spritesheet-generator-in-python/)
