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

		self.header = [self.ct.read(2 * self._unpack()).decode("UTF-16LE") for i in range(self._unpack())]
		self.types = [self._mstype(self._unpack()) for i in range(self._unpack())]
		self.rows = [[self._unpack(t) for t in self.types] for i in range(self._unpack())]

		self.ct.close()
		return [self.header] + [self.types] + self.rows

	def write(self, data):
		"""
		TODO: Write list to CT file

		:param list data: Decoded list to write on CT file
		"""

		pass

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
		else: print("No types for byte \"{0}\"".format(n), file=sys.stderr)

	def _unpack(self, dtyp=None):
		"""
		Decode binary data from Windows data type

		:param dtyp: MS-DTYP to decode, UINT32 if None (default)
		:type dtyp: str or None
		:return: byte(s) of requested dtyp
		:rtype: str, int if dtyp is None
		"""

		if dtyp in ("BYTE", "BOOL"):
			return "{:d}".format(struct.unpack("B", self.ct.read(1))[0])
		elif dtyp == "SHORT":
			return "{:d}".format(struct.unpack("h", self.ct.read(2))[0])
		elif dtyp == "WORD":
			return "{:d}".format(struct.unpack("<H", self.ct.read(2))[0])
		elif dtyp == "INT":
			return "{:d}".format(struct.unpack("i", self.ct.read(4))[0])
		elif dtyp == "DWORD":
			return "{:d}".format(self._unpack())
		elif dtyp == "DWORD_HEX":
			return "0x{:08X}".format(self._unpack())
		elif dtyp == "STRING":
			length = self._unpack()
			return self.ct.read(2 * length).decode("UTF-16LE") if length else "null"
		elif dtyp == "FLOAT":
			return "{:.6f}".format(struct.unpack("f", self.ct.read(4))[0])
		elif dtyp == "INT64":
			return "{:d}".format(struct.unpack("<Q", self.ct.read(8))[0])
		else:
			return struct.unpack("<L", self.ct.read(4))[0]
