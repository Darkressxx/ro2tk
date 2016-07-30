import os, sys, struct

from .asset import Asset

class CT(Asset):
	"""
	Gravity proprietary file format for Ragnarok Online 2 assets

	TODO: Document file format

	:param str path: Path to CT file
	"""

	def read(self):
		"""
		Parse CT file to a decoded list

		:return: Decoded CT data
		:rtype: list
		"""

		self.ct = open(self.path, "rb")
		self.ct.seek(64)

		self.header = [self.ct.read(2 * int(self._unpack())).decode("UTF-16LE") for i in range(int(self._unpack()))]
		self.types = [self._mstype(int(self._unpack())) for i in range(int(self._unpack()))]
		self.rows = [[self._unpack(t) for t in self.types] for i in range(int(self._unpack()))]

		if self.verbose:
			print("\nCT read of \"{0}\" complete!\n".format(self.path))

		self.ct.close()
		return [self.header] + [self.types] + self.rows

	def write(self, data):
		"""
		TODO: Write list to CT file

		:param list data: Decoded list to write on CT file
		"""

		print("\nCT.write() not implementend yet\n", file=sys.stderr)

		return

	@staticmethod
	def _mstype(n):
		"""
		Decode MS-DTYP from CT type row

		:param int n: Value from CT type row
		:return: Windows Data Type
		:rtype: str
		"""

		if n == 2: return "BYTE"
		elif n == 3: return "SHORT"
		elif n == 4: return "WORD"
		elif n == 5: return "INT"
		elif n == 6: return "DWORD"
		elif n == 7: return "DWORD_HEX"
		elif n == 8: return "STRING"
		elif n == 9: return "FLOAT"
		elif n == 11: return "INT64"
		elif n == 12: return "BOOL"
		else: print("\nNo types for byte \"{0}\"\n".format(n), file=sys.stderr)

	def _unpack(self, dtyp="DWORD"):
		"""
		Decode binary data from Windows data type

		:param str dtyp: MS-DTYP to decode, defaults to DWORD
		:return: unpacked byte(s) of requested dtyp as a string
		:rtype: str
		"""

		if dtyp in ("BYTE", "BOOL"):
			return str(struct.unpack("B", self.ct.read(1))[0])
		elif dtyp == "SHORT":
			return str(struct.unpack("h", self.ct.read(2))[0])
		elif dtyp == "WORD":
			return str(struct.unpack("<H", self.ct.read(2))[0])
		elif dtyp == "INT":
			return str(struct.unpack("i", self.ct.read(4))[0])
		elif dtyp == "DWORD":
			return str(struct.unpack("<L", self.ct.read(4))[0])
		elif dtyp == "DWORD_HEX":
			return "0x{:08X}".format(int(self._unpack()))
		elif dtyp == "STRING":
			length = int(self._unpack())
			return self.ct.read(2 * length).decode("UTF-16LE") if length else "null"
		elif dtyp == "FLOAT":
			return str(struct.unpack("f", self.ct.read(4))[0])
		elif dtyp == "INT64":
			return str(struct.unpack("<Q", self.ct.read(8))[0])
		else:
			print("\nCould not read type \"{0}\"\n".format(dtyp), file=sys.stderr)
