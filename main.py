#!/usr/bin/python3

from awair import AwairConnector
from datetime import datetime, timezone
from influx import InfluxConnector
import logging
from pathlib import Path
import time
import yaml

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


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


try:
    while True:
        with open(Path(__file__).with_name("config.yaml")) as config_file:

            config = yaml.safe_load(config_file)

            if not config:
                raise ValueError("Invalid config.yaml. See template.config.yaml.")

            for name in {"influx", "awair", "main"}:
                if name not in config:
                    raise ValueError(f"Invalid config.yaml: missing section {name}.")

            main_conf = config["main"]
            logging.getLogger().setLevel(logging.getLevelName(main_conf["logverbosity"]))

            main(config)

            time.sleep(main_conf["loop_seconds"])

except FileNotFoundError as e:
    logging.error("Missing config.yaml file.")
    exit(2)

except Exception as e:
    logging.exception(e)
    exit(1)
