# Awair to InfluxDB

## Requirements

- Tested on raspbian on raspberry pi 2, but should work on most other distros
- Python 3.7 or later
- pip3: `sudo apt-get install python3-pip` if missing
- [InfluxDB](https://en.wikipedia.org/wiki/InfluxDB) v2 installed and accessible from the device running the script
- Bucket created on the influxDB and token available

## Setup

1. Git clone and cd into directory
2. `cp template.config.yaml config.yaml`
3. Edit file `config.yaml` by following instructions in file
4. `pip3 install -r requirements.txt`

## Run

`python3 main.py` or `./main.py`

