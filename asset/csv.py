import os, sys

class CSV(object):

	name = ""
	header = []
	types = []
	rows = []

	def open(self, path):
		"""
		Parse CSV file to list

		:param str path: Path to CSV file
		:return: Parsed CSV data
		:rtype: list
		"""

		try:
			self.csv = open(path, "r", encoding="utf-16")
		except (OSError, IOError):
			print("could not open \"{0}\"".format(path), file=sys.stderr)

		self.name = os.path.splitext(os.path.basename(path))[0]
		self.header = self.csv.readline().rstrip("\n\r").split("\t")
		self.types = self.csv.readline().rstrip("\n\r").split("\t")
		self.rows = [line.rstrip("\n\r").split("\t") for line in self.csv]

		self.csv.close()
		return [self.header] + [self.types] + self.rows

	def write(self, path, data):
		"""
		TODO: Write list to CSV

		:param str path: Path to CSV file
		:param list data: Decoded list to write on CSV file
		"""

		pass
