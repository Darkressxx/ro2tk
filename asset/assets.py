import io, os, sys

class Asset(object):

	name = ""
	header = []
	types = []
	rows = []

	def __init__(self, asset):
		"""Initialize object."""
		try:
			f = open(asset, "r", encoding="utf-16")
			self.csv = io.StringIO(f.read())
			f.close()
		except (OSError, IOError):
			print("could not open {0}".format(asset), file=sys.stderr)

		self.name = os.path.splitext(os.path.basename(asset))[0]

	def close(self):
		"""Close CSV object to clean memory."""
		self.csv.close()

	def debug(self, full=False):
		"""Print object attributes."""
		print("Name:\n{0}\n".format(self.name))
		print("Header:\n{0}\n".format(self.header))
		print("Types:\n{0}\n".format(self.types))
		if full:
			print("Rows:\n{0}\n".format(self.rows))
		else:
			print("Row #1:\n{0}\n".format(self.rows[:1]))

	def parse(self):
		"""Parse CSV object."""
		self.csv.seek(0)

		self.header = self.csv.readline().strip("\n\r").split("\t")
		self.types = self.csv.readline().strip("\n\r").split("\t")

		for line in self.csv:
			line = line.rstrip("\n\r").replace("\\", "/").split("\t")

			for col in range(len(line)):
				if line[col] == "null":
					line[col] = None
				elif self.types[col] in ("BYTE", "WORD", "DWORD", "INT", "INT32", "INT64"):
					line[col] = int(line[col])
				elif self.types[col] in ("STRING", "DWORD_HEX"):
					pass
				else:
					print("Unknown type: {0}".format(self.types[col]), file=sys.stderr)

			self.rows.append(line)

	def update(self, db, user=None, password=None):
		pass

	def write(self, path):
		"""Write decoded CT to disk as a UTF-8 CSV file."""
		self.csv.seek(0)
		filename = "{0}/{1}.csv".format(path, self.name)
		os.makedirs(os.path.dirname(filename), exist_ok=True)
		with open(filename, "w", newline="\r\n") as copy:
			copy.write(self.csv.read())
