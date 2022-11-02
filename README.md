# AIS - An open source AIS data analyzer

AIS (automatic identification system) is a tracking system for maritime vessels.

This project's aim is to provide useful tools to analyze, aggregate and extract information from historical AIS datasets.

AIS equipment provides information such as unique identification, position, course, and speed to other vessels and central authorities
Live AIS data can be viewed online through a variety of web services.  

Historical AIS data can be freely accessed online, e.g. via the
Norwegian Coastal Administration (https://ais-public.kystverket.no/) or the Danish Maritime Authority (http://web.ais.dk/aisdata/).


## Table of content
  * [Installation](#installation)
    * [Requirements](#requirements)
    * [Build and install](#build-and-install)
    * [Uninstall](#uninstall)
  * [Usage](#usage)
  * [Credits](#credits)

## Installation
Currently, the package can only be installed by building the project locally. 
### Requirements
The package requires `pip` and `build` to build and install the package.
The `wheel` package is also required to install the project.
The requirements for running the project are listed in [requirements.txt](requirements.txt), and can be installed with
```sh
pip install -r requirements.txt
```

### Build and install
To build the project, download the source code either with `git`:
```sh
git clone https://github.com/bkkas/ais
```
or by downloading the source code as a zip from the browser.

To build the project, move into the now cloned repository and run 
```py
python -m build
```
This will create a new folder called `dist` in which the built package will be stored.
Running either
```sh
pip install ais_analyzer-0.0.1.tar.gz  
# or 
pip install ais_analyzer-0.0.1-py3-none-any.whl
```
will install the packae as a python module.

### Uninstall
Simply run
```sh
pip uninstall ais_analyzer
```
and the package will be removed.

## Usage
Currently it only supports running as a python module.
This means it has to be called by issuing
```sh
python -m ais_analyzer <args>
```

Calling
```sh
python -m ais_analyzer -h
```
will give the following output
```
usage: ais [-h] [--input-file INPUT_FILE] [--full] [--lat LAT] [--lon LON] [--radius RADIUS] [--output-file OUTPUT_FILE] <COMMAND>

AIS analyzer application

positional arguments:
  <COMMAND>             a command to call on the input data

options:
  -h, --help            show this help message and exit
  --input-file INPUT_FILE
                        the path to the input ais csv file(s)
  --full                enables the full statistic output
  --lat LAT             latitude in degrees, use decimal degrees not minutes & seconds
  --lon LON             longitude in degrees, use decimal degrees not minutes & seconds
  --radius RADIUS       radius from latlong point in meters
  --output-file OUTPUT_FILE
                        output path and name of output csv
```
where `<COMMMAND>` is the last argument provided.



## Credits
