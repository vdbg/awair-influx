from datetime import datetime
import aiohttp
import asyncio
import logging
from python_awair import Awair

"""fix yelling at me error"""
# Copy/pasted from https://pythonalgos.com/runtimeerror-event-loop-is-closed-asyncio-fix
from functools import wraps

from asyncio.proactor_events import _ProactorBasePipeTransport


def silence_event_loop_closed(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != "Event loop is closed":
                raise

    return wrapper


_ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)
"""fix yelling at me error end"""


class AwairConnector:
    def __init__(self, token: str, min_records: int):
        self.token = token
        self.min_records = min_records

    def fetch_data(self, from_time: datetime, to_time: datetime, measurement: str) -> list:
        five_minutes_count = (to_time - from_time).total_seconds() / 60 / 5
        if five_minutes_count < self.min_records:  # helps with not getting throttled
            logging.debug(f"Skipping awair download: not enough records to download.")
            return []
        return asyncio.run(self.__fetch_data_async(int(five_minutes_count), from_time, to_time, measurement))

    async def __fetch_data_async(self, limit: int, from_time: datetime, to_time: datetime, measurement: str) -> list:
        # datetime handling in Python is problematic
        # influx returns offset-aware datetimes
        # awair compares them with datetime.now() that is offset-naive
        # hilarity ensues. Therefore must convert all input dates to offset-naive
        utc_to_local = datetime.utcnow() - datetime.now()
        from_time = from_time.replace(tzinfo=None) - utc_to_local
        to_time = to_time.replace(tzinfo=None) - utc_to_local

        delta = to_time - from_time

        logging.info(f"Querying awair from {from_time} to {to_time} = {delta}.")

        async with aiohttp.ClientSession() as session:

            client = Awair(access_token=self.token, session=session)

            user = await client.user()
            devices = await user.devices()

            records = []

            for device in devices:

                data = await device.air_data_five_minute(fahrenheit=False, from_date=from_time, to_date=to_time, limit=limit)

                for datum in data:
                    sensorsDict = {sensor: value for sensor, value in datum.sensors.items()}
                    if datum.score == 0:
                        continue  # gaps in reported metrics result in score 0 instead of missing record
                    sensorsDict["score"] = datum.score
                    records.append({"measurement": measurement, "tags": {"host": device.uuid}, "fields": sensorsDict, "time": datum.timestamp})

            return records
