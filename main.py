#!/usr/bin/python3

from awair import AwairConnector
from datetime import datetime, timezone
from influx import InfluxConnector
import logging
from pathlib import Path
import time
import yaml

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

def main(config) -> None:
    influx_conf = config["influx"]
    awair_conf = config["awair"]
    measurement = influx_conf["measurement"]
    influxConnector = InfluxConnector(influx_conf["bucket"], influx_conf["token"], influx_conf["org"], influx_conf["url"])

    try:
        to_time = datetime.now(timezone.utc)
        from_time = influxConnector.get_last_recorded_time(measurement, awair_conf["maxhours"], to_time)
        awairConnector = AwairConnector(awair_conf["token"], awair_conf["records"])
        records = awairConnector.fetch_data(from_time, to_time, measurement)

        try:
            influxConnector.add_samples(records, len(records))
        except Exception as e:
            logging.error(f"Exception importing records")
            logging.exception(e)
    except Exception as e:
        logging.error(f"Exception while querying records")
        logging.exception(e)

CONFIG_FILE = "config.yaml"

try:
    while True:
        with open(Path(__file__).with_name(CONFIG_FILE)) as config_file:

            config = yaml.safe_load(config_file)

            if not config:
                raise ValueError(f"Invalid {CONFIG_FILE}. See template.{CONFIG_FILE}.")

            for name in {"influx", "awair", "main"}:
                if name not in config:
                    raise ValueError(f"Invalid {CONFIG_FILE}: missing section {name}.")

            main_conf = config["main"]
            logging.getLogger().setLevel(logging.getLevelName(main_conf["logverbosity"]))

            main(config)

            time.sleep(main_conf["loop_seconds"])

except FileNotFoundError as e:
    logging.error(f"Missing {e.filename}.")
    exit(2)

except Exception as e:
    logging.exception(e)
    exit(1)
