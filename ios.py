#!/usr/bin/python3

import os, json

class Game():

	def __init__(self):

		base_path = os.path.abspath(os.path.dirname(__file__))
		locations_path = os.path.join(base_path, "locations.json")
		items_path = os.path.join(base_path, "items.json")
		with open(locations_path, 'r') as fp:
			self.locations = json.load(fp)
		with open(items_path, 'r') as fp:
			self.items = json.load(fp)
		self.prepositions = ["BY", "FACING", "AT", "IN", "OUTSIDE", "BENEATH", "ON"]
		self.verbs = ["N", "S", "E", "W", "GO", "GET", "TAK", "GIV", "DRO", "LEA", "EAT", "DRI", "RID", "OPE", "PIC", "CHO", "CHI", "TAP", "BRE", "FIG", "STR", "ATT", "HIT", "KIL", "SWI", "SHE", "HEL", "SCR", "CAT", "RUB", "POL", "REA", "EXA", "FIL", "SAY", "WAI", "RES", "WAV", "INF", "XLO", "XSA", "QUI"]
		self.status = "LET YOUR QUEST BEGIN"
		self.over = False

		self.location = 23
		self.time_remaining = 1000
		self.strength = 100
		self.wisdom = 35

		self.CONST_C1 = 16
		self.CONST_C2 = 21
		self.CONST_C3 = 24

	def input(self, text):

		return

if __name__ == "__main__":

	game = Game()
	while not game.over:
		print(game.status)
		game.input(input().upper())
