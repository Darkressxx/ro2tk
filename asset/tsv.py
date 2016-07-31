import os

from .asset import Asset

class TSV(Asset):
	"""
	Tab-separated values file format for Ragnarok Online 2 assets

	http://www.iana.org/assignments/media-types/text/tab-separated-values

	:param str path: Path to TSV file
	"""

	def read(self):
		"""
		Parse TSV file to list

		:return: Parsed TSV data
		:rtype: list
		"""

		self.tsv = open(self.path, "r", newline="\r\n")

		self.header = self.tsv.readline().rstrip("\r\n").split("\t")
		self.types = self.tsv.readline().rstrip("\r\n").split("\t")
		self.rows = [line.rstrip("\r\n").split("\t") for line in self.tsv]

		if self.verbose:
			print("\nTSV read of \"{0}\" complete!\n".format(self.path))

		self.tsv.close()
		return [self.header] + [self.types] + self.rows

	def write(self, data):
		"""
		Write list to TSV

		:param list data: Decoded list to write on TSV file
		"""

		os.makedirs(os.path.dirname("./{0}".format(self.path)), exist_ok=True)
		self.tsv = open(self.path, "w", newline="\r\n")

		self.header = "\t".join(i for i in data[0]) + "\n"
		self.types = "\t".join(i for i in data[1]) + "\n"
		self.rows = "\n".join("\t".join(l) for l in data[2:]) + "\n"

		self.tsv.write(self.header + self.types + self.rows)

		if self.verbose:
			print("\nTSV write to \"{0}\" complete!\n".format(self.path))
