import os

from abc import ABCMeta

class Asset(metaclass=ABCMeta):
	name = ""
	header = []
	types = []
	rows = []

	verbose = False

	def __init__(self, path):
		self.path = path
		self.name = os.path.splitext(os.path.basename(self.path))[0]
