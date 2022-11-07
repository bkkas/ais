# AIS - An open source AIS data analyzer

AIS (automatic identification system) is a tracking system for maritime vessels.

This project's aim is to provide useful tools to analyze, aggregate and extract information from historical AIS datasets.

AIS equipment provides information such as unique identification, position, course, and speed to other vessels and central authorities
Live AIS data can be viewed online through a variety of web services.  

Historical AIS data can be freely accessed online, e.g. via the
Norwegian Coastal Administration (https://ais-public.kystverket.no/) or the Danish Maritime Authority (http://web.ais.dk/aisdata/).


## Table of content
  * [License](#license)
  * [Installation](#installation)
    * [Requirements](#requirements)
    * [Build and install](#build-and-install)
    * [Uninstall](#uninstall)
  * [Usage](#usage)
  * [Credits](#credits)

## License
For the license of the package, refer to [LICENSE](LICENSE). 
For the dataset that is included in the tests-folder, the norwegian dataset is aquired through (https://ais-public.kystverket.no/), while the danish dataset is aquired throuh (http://web.ais.dk/aisdata/).

The norwegian dataset uses the [NLOD](https://data.norge.no/nlod/en/2.0) license, as defined by the norwegian government.
The danish dataset has its own [terms of use](https://dma.dk/safety-at-sea/navigational-information/download-data/conditions-for-the-use-of-data).


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
pip install ais_analyzer-*.*.*.tar.gz  
# or 
pip install ais_analyzer-*.*.*-py3-none-any.whl
```
will install the packae as a python module.

Be aware that the `pip` install directory must be in path if you wish to run `ais` as a command, and drop the `python -m ais_analyzer` part.
For some Linux distributions, this is not the default.
If you get a warning, adding the folder specified to `$PATH` will fix the issue (usually `$HOME/.local/bin/`).

### Uninstall
Simply run
```sh
pip uninstall ais_analyzer
```
and the package, along with the script, will be removed.

## Usage
The program can be called in two ways, and their usages are equal.
```
ais <args>
```
or
```
python -m ais_analyzer <args>
```

Calling
```sh
ais ais_analyzer -h
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

An example of a complete run could look something like
```
ais --input-file some_data.csv --full --output-file statistics.csv statistcs
```
Where `statistics` is the given `<COMMAND>`.


## Credits
