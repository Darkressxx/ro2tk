import os

from .asset import Asset

class CSV(Asset):
	"""
	Comma-separated values file format for Ragnarok Online 2 assets

	:param str path: Path to CSV file
	"""

	def read(self):
		"""
		Parse CSV file to list

		:return: Parsed CSV data
		:rtype: list
		"""

		self.csv = open(self.path, "r", encoding="UTF-16", newline="\r\n")

		self.header = self.csv.readline().rstrip("\r\n").split("\t")
		self.types = self.csv.readline().rstrip("\r\n").split("\t")
		self.rows = [line.rstrip("\r\n").split("\t") for line in self.csv]

		self.csv.close()
		return [self.header] + [self.types] + self.rows

	def write(self, data):
		"""
		Write list to CSV

		:param list data: Decoded list to write on CSV file
		"""

		os.makedirs(os.path.dirname("./{0}".format(self.path)), exist_ok=True)
		self.csv = open(self.path, "w", encoding="UTF-16", newline="\r\n")

		self.header = "\t".join(i for i in data[0]) + "\n"
		self.types = "\t".join(i for i in data[1]) + "\n"
		self.rows = "\n".join("\t".join(l) for l in data[2:]) + "\n"

		self.csv.write(self.header + self.types + self.rows)
		print("CSV write to \"{0}\" complete!".format(self.path))
