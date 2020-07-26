from influxdb import InfluxDBClient;
from datetime import datetime

class InfluxInserter():

#Constructor
	def __init__(self, influxIP, influxUser, influxPassword, influxPort, influxDB):
		self.client = InfluxDBClient(influxIP, influxPort, influxUser, influxPassword);
		self.client.switch_database(influxDB);

	def InsertData(self, measurement, tags={},fields = {}):
		data = {"measurement": measurement,
			"tags": tags,
			"time": str(datetime.utcnow()),
			"fields": fields
		};
		result = self.client.write_points([data]);
		return result;
