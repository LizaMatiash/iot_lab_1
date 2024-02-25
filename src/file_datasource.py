from csv import reader
from datetime import datetime
from typing import List
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.parking import Parking
from domain.aggregated_data import AggregatedData
import config


class FileDatasource:
    def __init__(self, accelerometer_filename: str, gps_filename: str, parking_filename: str) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.parking_filename = parking_filename

    def read(self) -> List[AggregatedData]:
        "Метод повертає дані отримані з датчиків"
        aggregated_data_list = []
        try:
            for _ in range(10):
                accelerometer_data = next(self.accelerometer_reader)
                gps_data = next(self.gps_reader)
                parking_data = next(self.parking_reader)

                accelerometer = Accelerometer(*map(int, accelerometer_data))
                gps = Gps(*map(float, gps_data))
                parking = Parking(*map(float, parking_data), gps=gps)

                aggregated_data_list.append(AggregatedData(accelerometer, gps, parking, datetime.now()))

        except StopIteration:
            self.accelerometer_file.seek(1)
            self.gps_file.seek(1)
            self.parking_file.seek(1)
            return self.read()

        except Exception as e:
            print(f"An error occurred while reading data: {e}")

        return aggregated_data_list

    def startReading(self, *args, **kwargs):
        "Метод повинен викликатись перед початком читання даних"
        self.accelerometer_file = open(self.accelerometer_filename, 'r')
        self.gps_file = open(self.gps_filename, 'r')
        self.parking_file = open(self.parking_filename, 'r')

        self.accelerometer_reader = reader(self.accelerometer_file)
        self.gps_reader = reader(self.gps_file)
        self.parking_reader = reader(self.parking_file)

        next(self.accelerometer_reader)
        next(self.gps_reader)
        next(self.parking_reader)

    def stopReading(self, *args, **kwargs):
        "Метод повинен викликатись для закінчення читання даних"
        self.accelerometer_file.close()
        self.gps_file.close()
        self.parking_file.close()


