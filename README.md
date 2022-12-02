# Awair to InfluxDB

Allows for importing [Awair](https://www.getawair.com/index.html) data to [InfluxDB](https://www.influxdata.com/).

**WARNING**: these scripts can no longer be tested/supported as Awair
[intentionally bricked](https://www.reddit.com/r/Awair/comments/y7i5ku/awair_discontinues_support_for_v1_devices/)
my only Awair device.

## Requirements

- A device, capable of running either Docker containers or Python e.g., [Raspbian](https://www.raspbian.org/) or Windows
- [InfluxDB](https://en.wikipedia.org/wiki/InfluxDB) v2 installed and accessible from the device running the import
- Bucket created on the influxDB and token available
- An Awair device that is not prevented from uploading data to the cloud.
  Recommend contacting [Awair's support](https://support.getawair.com/hc/en-us) to inquire about their forced obsolescence
  policy before purchasing a new device.

## Setup

Choose one of these 3 methods.

### Using pre-built Docker image

1. `touch config.yaml`
2. This will fail due to malformed config.yaml. That's intentional :)
   ``sudo docker run --name my-awair-influx -v "`pwd`/config.yaml:/app/config.yaml" vdbg/awair-influx``
3. `sudo docker cp my-awair-influx:/app/template.config.yaml config.yaml`
4. Edit `config.yaml` by following the instructions in the file
5. `sudo docker start my-awair-influx -i`
  This will display logging on the command window allowing for rapid troubleshooting. `Ctrl-C` to stop the container. Note: config.yaml is automatically reloaded.
7. When done testing the config:
  * `sudo docker container rm my-awair-influx`
  * ``sudo docker run -d --name my-awair-influx -v "`pwd`/config.yaml:/app/config.yaml" --restart=always --memory=100m vdbg/awair-influx``
  * To see logs: `sudo docker container logs -f my-awair-influx`

### Using Docker image built from source

1. `git clone https://github.com/vdbg/awair-influx.git`
2. `sudo docker build -t awair-influx-image awair-influx`
3. `cd awair-influx`
4. `cp template.config.yaml config.yaml`
5. Edit `config.yaml` by following the instructions in the file
6. Test run: ``sudo docker run --name my-awair-influx -v "`pwd`/config.yaml:/app/config.yaml" awair-influx-image``
   This will display logging on the command window allowing for rapid troubleshooting. `Ctrl-C` to stop the container. Note: config.yaml is automatically reloaded.
7. If container needs to be restarted for testing: `sudo docker start my-awair-influx -i`
8. When done testing the config:
  * `sudo docker container rm my-awair-influx`
  * ``sudo docker run -d --name my-awair-influx -v "`pwd`/config.yaml:/app/config.yaml" --restart=always --memory=100m awair-influx-image``
  * To see logs: `sudo docker container logs -f my-awair-influx`

### Running directly on the device

[Python](https://www.python.org/) 3.7 or later with pip3 required. `sudo apt-get install python3-pip` will install pip3 on ubuntu/raspbian systems if missing.

To install:

1. `git clone https://github.com/vdbg/awair-influx.git`
2. `cd awair-influx`
3. `cp template.config.yaml config.yaml`
4. Edit `config.yaml` by following the instructions in the file
5. `pip3 install -r requirements.txt`
6. Run the program:
  * Interactive mode: `python3 main.py`
  * Shorter: `.\main.py` (Windows) or `./main.py` (any other OS).
  * As a background process (on non-Windows OS): `python3 main.py > log.txt 2>&1 &`
7. To exit: `Ctrl-C` if running in interactive mode, `kill` the process otherwise.


