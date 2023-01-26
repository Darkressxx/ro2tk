import os

from .asset import Asset

class TSV(Asset):

	def write(self, data):
	    """
	    Write list to TSV
	    :param list data: Decoded list to write on TSV file
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
	        os.makedirs(os.path.dirname("./{0}".format(self.path)), exist_ok=True)
	        self.tsv = open(self.path, "w", encoding="UTF-16LE", newline="\r\n")
	    except:
	        print("Error: there was an issue opening the TSV file for writing.")
	        return

	    self.header = "\t".join(i for i in data[0]) + "\n"
	    self.types = "\t".join(i for i in data[1]) + "\n"
	    self.rows = "\n".join("\t".join(str(cell) for cell in row) for row in data[2:]) + "\n"


	    self.tsv.write(self.header + self.types + self.rows)

	    if self.verbose:
	        print("\nTSV write to \"{0}\" complete!\n".format(self.path))


	def read(self):
	    """
	    Parse TSV file to a decoded list

	    :return: Decoded TSV data
	    :rtype: list
	    """
	    try:
	        self.tsv = open(self.path, "r", encoding="UTF-16LE")
	    except FileNotFoundError:
	        print("Error: the specified TSV file does not exist.")
	        return
	    except:
	        print("Error: there was an issue opening the TSV file.")
	        return

	    self.header = self.tsv.readline().strip().split("\t")
	    self.types = self.tsv.readline().strip().split("\t")
	    self.rows = [l.strip().split("\t") for l in self.tsv.readlines()]

	    if len(self.header) == 0 or len(self.types) == 0 or len(self.rows) == 0:
	        print("Error: the TSV file is empty or has fewer than three rows.")
	        return

	    self.tsv.close()
	    return [self.header, self.types] + self.rows
