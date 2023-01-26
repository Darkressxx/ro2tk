import os, sys, struct
from struct import calcsize
from .asset import Asset

class CT(Asset):
	"""
	Gravity proprietary file format for Ragnarok Online 2 assets
	CT file format
		Useless 63 bytes at the start.
		Header (variable length)
		- List of text represting the data names of each column
		Types row (variable length)
		- List of integers representing the data type of each column in the file
		Data rows (variable length)
		- Each row corresponds to a single record
		- Each column corresponds to a field in the record
		- Data is stored according to the data types specified in the types row
		Last two bytes are not generated here but they are a checksum
	:param str path: Path to CT file
	"""

	def _checksum(self):
		self.ct.seek(0)
		checksum = 0
		chunk = self.ct.read(1024)
		while chunk:
			for b in chunk:
				checksum += b
			chunk = self.ct.read(1024)
		return checksum & 0xffff

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

		# Convert all elements in rows to str
		self.rows = [[str(elem) for elem in row] for row in self.rows]

		if self.verbose:
			print("\nCT read of \"{0}\" complete!\n".format(self.path))

		self.ct.close()
		return [self.header] + [self.types] + self.rows

	@staticmethod
	def _mstype(n):
		"""
		Decode MS-DTYP from CT type row
		:param int n: Value from CT type row
		:return: Windows Data Type
		:rtype: str
		"""
		type_map = {
			2: "BYTE",
			3: "SHORT",
			4: "WORD",
			5: "INT",
			6: "DWORD",
			7: "DWORD_HEX",
			8: "STRING",
			9: "FLOAT",
			11: "INT64",
			12: "BOOL"
		}
		return type_map.get(n, "UNKNOWN_TYPE")

	def write(self, data, mode="w+b"):
		"""
		Write data to CT file
		:param list data: Data to write to CT file
		:param str mode: File mode, defaults to "w+b"
		"""
		# Check if data is a list
		if not isinstance(data, list):
			print("Error: data must be a list. Please provide a valid list as the data parameter.")
			return

		# Check if data has at least three elements (header, types, and at least one row)
		if len(data) < 3:
			print("Error: data must contain at least the header and types rows and one data row.")
			return

		try:
			self.ct = open(self.path, mode)
		except:
			print("Error: there was an issue opening the CT file for writing.")
			return

		# Write header data (THIS DOESN'T REALLY MATTER AS LONG THERE ARE 63 BYTES BEFORE THE HEADERS ROW)
		header_data = "52 00 4F 00 32 00 53 00 45 00 43 00 21 00 00 00 32 00 30 00 31 00 39 00 2D 00 30 00 32 00 2D 00 30 00 31 00 20 00 31 00 31 00 3A 00 34 00 32 00 3A 00 35 00 39 00 00 00 00 00 00 00 00 00 00 00"
		self.ct.write(bytes.fromhex(header_data))

		# Write header row
		self._pack(len(data[0]))
		for header in data[0]:
			header_bytes = header.encode("UTF-16LE")
			self._pack(len(header_bytes) // 2)
			self.ct.write(header_bytes)

		# Write types row
		self._pack(len(data[1]))
		for dtyp in data[1]:
			self._pack(self._mscode(dtyp))

		# Write data rows
		self._pack(len(data[2:]))
		for row in data[2:]:
			for i, elem in enumerate(row):
				self._pack(elem, data[1][i])

		self.ct.seek(64)
		self.ct.write(struct.pack("<H", self._checksum()))

		self.ct.close()

	@staticmethod
	def _mscode(dtyp):
		"""
		Encode MS-DTYP to CT type row value
		:param str dtyp: Windows Data Type
		:return: Value for CT type row
		:rtype: int
		"""
		type_map = {
			"BYTE": 2,
			"SHORT": 3,
			"WORD": 4,
			"INT": 5,
			"DWORD": 6,
			"DWORD_HEX": 7,
			"STRING": 8,
			"FLOAT": 9,
			"INT64": 11,
			"BOOL": 12
		}
		return type_map.get(dtyp, 0)  # Return 0 for unknown types

	def _pack(self, data, dtyp="DWORD"):
		"""
		Encode data to Windows data type
		:param str data: Data to encode
		:param str dtyp: MS-DTYP to encode, defaults to DWORD
		"""
		type_map = {
			"BYTE": ("B", int),
			"SHORT": ("h", int),
			"WORD": ("<H", int),
			"INT": ("i", int),
			"DWORD": ("<L", int),
			"DWORD_HEX": ("<L", lambda x: int(x, 16)),
			"STRING": ("s", lambda x: x.encode("UTF-16LE")),
			"FLOAT": ("f", float),
			"INT64": ("<Q", int),
			"BOOL": ("B", lambda x: int(bool(x)))
		}
		try:
			fmt, conv = type_map[dtyp]
			print(f"data: {data}")  # Debug statement
			converted_data = conv(data)
			print(f"converted_data: {converted_data}")  # Debug statement
			if fmt:
				self.ct.write(struct.pack(fmt, converted_data))
			else:
				self.ct.write(converted_data)
		except KeyError:
			raise ValueError(f"Invalid data type: {dtyp}")
		except struct.error:
			raise ValueError(f"Invalid data: {data}")



	def _unpack(self, dtyp="DWORD"):
		"""
		Decode binary data from Windows data type
		:param str dtyp: MS-DTYP to decode, defaults to DWORD
		:return: unpacked byte(s) of requested dtyp as a string
		:rtype: str
		"""

		type_map = {
			"BYTE": ("B", int),
			"SHORT": ("h", int),
			"WORD": ("<H", int),
			"INT": ("i", int),
			"DWORD": ("<L", int),
			"DWORD_HEX": ("<L", lambda x: int(x, 16)),
			"STRING": ("<H", lambda x: (len(x), x.encode("UTF-16LE"))),
			"FLOAT": ("f", float),
			"INT64": ("<Q", int),
			"BOOL": ("B", lambda x: int(bool(x)))
		}
		try:
			fmt, conv = type_map[dtyp]
			if fmt:
				data = struct.unpack(fmt, self.ct.read(calcsize(fmt)))
				if isinstance(data, tuple):
					# This handles the case where the value needs to be unpacked from a tuple,
					# like in the case of "STRING".
					return data[0]
				else:
					return data
			else:
				# This handles the case where the value is already decoded, like in the case of "BOOL".
				return converted_data
		except KeyError:
			raise ValueError(f"Invalid data type: {dtyp}")

