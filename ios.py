#!/usr/bin/python3

import os, json, time, random

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
		self.status = "LET YOUR QUEST BEGIN."
		self.state = ""
		self.over = False

		self.location = 23
		self.time_remaining = 1000
		self.strength = 100
		self.wisdom = 35
		self.food = 2
		self.drink = 2

		self.CONST_C1 = 16
		self.CONST_C2 = 21
		self.CONST_C3 = 24
		self.CONST_C4 = 43

	def items_seen(self):

		items = []
		for i in range(0, self.CONST_C4):
			if ((self.items[i][2] == self.location) & (self.items[i][3] < 1)):
				items.append(self.items[i])
		return items

	def prose(self):

		items = self.items_seen()
		location = self.locations[self.location - 1]

		prose = ["ISLAND OF SECRETS", "-----------------"]
		prose.append("Time remaining: " + str(self.time_remaining))
		prose.append("Strength: " + str(self.strength))
		prose.append("Wisdom: " + str(self.wisdom))
		prose.append("")
		prose.append("You are " + (self.prepositions[location[0] - 1].lower()) + ": " + location[1])
		if len(items) > 0:
			prose.append("You see: " + (', '.join([x[1] for x in items])))
		prose.append("")
		prose.append(self.status)
		return prose

	def __slow_print(self, text):

		for i in range(0, len(text)):
			print(text[i], end='', flush=True)
			time.sleep(0.1)
		print('')

	def __lookup_word(self, word):

		vc = len(self.verbs)
		nc = len(self.items)
		for i in range(0, nc):
			if word.startswith(self.items[i][0]):
				return [False, i + 1]
		for i in range(0, vc):
			if word.startswith(self.verbs[vc - (i + 1)]):
				return [True, vc - i]
		return []

	def __parse(self, text):

		nouns = []
		verbs = []
		for word in text.strip().split(' '):
			item = self.__lookup_word(word.upper())
			if len(item) != 2:
				continue
			if item[0]:
				verbs.append(item[1])
			else:
				nouns.append(item[1])
		return [self.verbs[x - 1] for x in verbs], [self.items[x - 1] for x in nouns]

	def __word_id(self, word):
		for i in range(0, len(self.items)):
			if self.items[i][0] == word:
				return i + 1
		return 0

	def input(self, text):

		v, n = self.__parse(text)
		if len(n) == 0:
			self.state = ""
		else:
			word_id = self.__word_id(n[0][0])
			self.state = str(word_id) + str(n[0][2]) + str(n[0][3]) + str(self.location)

		print('\033[96m' + self.state + '\033[0m')

		self.time_remaining = self.time_remaining - 1
		self.status = ''

		if (((len(v) == 0) | ('GO' in v)) & (len(n) > 0)):
			self.__cmd_move(n, self.state)
		if ((('GET' in v) | ('TAK' in v) | ('PIC' in v) | ('CAT' in v)) & (len(n) > 0)):
			self.__cmd_get(v, n, self.state)

		if self.strength <= 0:
			self.over = True
		if self.time_remaining <= 0:
			self.over = True
		if 'QUI' in v:
			self.over = True

		return

	def __swimming(self):

		self.wisdom = self.wisdom - 1
		r = random.randint(1, 5)
		self.__slow_print("SWIMMING IN THE POISONOUS WATERS")
		self.strength = self.strength - r
		if self.strength < 1:
			self.status = "YOU GOT LOST AND DROWNED"
			self.over = True
			return
		if self.strength < 15:
			print("YOU ARE VERY WEAK")
		self.status = "YOU SURFACE"
		self.location = 30 + random.randint(1, 3)
		return

	def __cmd_move(self, nouns, state):

		v = 42
		w = 51
		o = self.__word_id(nouns[0][0])

		d = 0 # direction of movement
		c = 0 # did we actually move anywhere?

		if ((o > self.CONST_C4) & (o < w)):
			d = o - self.CONST_C4

		if ((state == '500012') | (state == '500053') | (state == '500045')):
			d = 4

		if ((state == '500070') | (state == '500037') | (state == '510011') | (state == '510041')):
			d = 1

		if ((state == '510043') | (state == '490066') | (state == '490051')):
			d = 1

		if ((state == '510060') | (state == '480056')):
			d = 2

		if ((state == '510044') | (state == '510052')):
			d = 3

		if ((state == '490051') & (self.items[28][3] == 0)):
			self.__swimming()
			return

		if ((self.location == self.items[38]) & ((self.location == 10) | ((self.strength + self.wisdom) < 180))):
			self.status = "YOU CAN'T LEAVE!"
			return

		if ((self.location == self.items[31][2]) & (self.items[31][3] < 1) & (d == 3)):
			self.status = "HE WILL NOT LET YOU PAST."
			return

		if ((self.location == 47) & (self.items[43][3] == 0)):
			self.status = "THE ROCKS MOVE TO PREVENT YOU"
			return

		if ((self.location == 28) & (self.items[6][3] != 1)):
			self.status = "THE ARMS HOLD YOU FAST"
			return

		if ((self.location == 45) & (self.items[39][3] == 0) & (d == 4)):
			self.status = "HISSSS!"
			return

		if ((self.location == 25) & ((self.items[15][2] + self.items[15][3]) != -1) & (d == 3)):
			self.status = "TOO STEEP TO CLIMB."
			return

		if ((self.location == 51) & (d == 3)):
			self.status = "THE DOOR IS BARRED!"
			return

		if ((d > 0) & (d != 5)):
			loc = self.locations[self.location - 1]
			if d == 1:
				if loc[2] == 0:
					self.location = self.location - 10
					c = 1
			if d == 2:
				if loc[3] == 0:
					self.location = self.location + 10
					c = 1
			if d == 3:
				if loc[4] == 0:
					self.location = self.location + 1
					c = 1
			if d == 4:
				if loc[5] == 0:
					self.location = self.location - 1
					c = 1

		self.status = "OK."

		if ((d < 1) | (c == 0)):
			self.status = "YOU CAN'T GO THAT WAY."

		if ((self.location == 33) & (self.items[15][2] == 0)):
			self.items[15][2] = random.randint(1, 4)
			self.items[15][3] = 0
			self.status = "THE BEAST RUNS AWAY!"
			return

		if ((self.location != self.items[24][2]) | (o != 25)):
			return

		self.status = ''
		text = "#YOU BOARD THE CRAFT "
		if self.wisdom < 60:
			text = text + "FALLING UNDER THE SPELL OF THE BOATMAN "
		text = text + "AND ARE TAKEN TO THE ISLAND OF SECRETS"
		self.__slow_print(text)

		if x < 60:
			text = "#TO SERVE OMEGAN FOREVER!"
			self.over = True
		else:
			text = "#THE BOAT SKIMS THE DARK SILENT WATERS"
			self.location = 57
		self.__slow_print(text)

	def __cmd_get(self, verbs, nouns, state):

		v = 42
		w = 51
		o = self.__word_id(nouns[0][0])

#1080 IF ((f(o)>0 AND f(o)<9) OR l(o)<>r) AND o<=c3 THEN LET f$="WHAT "+x$+"?": RETURN 

		if ((((self.items[o - 1][3] > 0) & (self.items[o - 1][3] < 9)) | (self.items[o - 1][2] != self.location)) & (o <= self.CONST_C3)):
			self.status = "WHAT ITEM DO YOU MEAN?"
			return

#1090 IF b$="3450050"THEN LET y=y-8: LET x=x-5: LET f$="THEY ARE CURSED": RETURN 

		if state == '3450050':
			self.strength = self.strength - 8
			self.wisdom = self.wisdom - 5
			self.status = "THEY ARE CURSED."
			return

#1100 IF b$="3810010"THEN GO SUB 1370

		if state == '3810010':
			self.__slow_print("////LIGHTNING FLASHES!")
			self.items[38][2] = self.location
			self.strength = self.strength - 8
			self.wisdom = self.wisdom - 2

#1110 IF (a=15 AND o<>20 AND o<>1) OR (a=29 AND o<>16) OR o>c3 THEN LET f$=w$+c$+" "+x$: RETURN 

		if ((('PIC' in verbs) & (o != 20) & (o != 1)) | (('CAT' in verbs) & (o != 16)) | (o > self.CONST_C3)):
			self.status = "YOU CAN'T DO THAT."
			return

#1120 IF l(o)=r AND (f(o)<1 OR f(o)=9) AND o<c3 THEN LET l(o)=0: LET a=-1

		if ((self.items[o - 1][2] == self.location) & ((self.items[o - 1][3] < 1) | (self.items[o - 1][3] == 9)) & (o < self.CONST_C3)):
			verbs = []
			self.items[o - 1][2] = 0

#1130 IF o=16 AND l(10)<>0 THEN LET l(o)=r: LET f$="IT ESCAPED": LET a=0

		if ((o == 16) & (self.items[9][2] != 0)):
			self.items[o - 1] = self.location
			self.status = "IT ESCAPED."
			verbs = ['']

#1140 IF o>c1 AND o<c2 THEN LET f=f+2: LET a=-1

		if ((o > self.CONST_C1) & (o < self.CONST_C2)):
			self.food = self.food + 2
			verbs = []

#1150 IF o>=c2 AND o<=c3 THEN LET g=g+2: LET a=-1

		if ((o >= self.CONST_C2) & (o <= self.CONST_C3)):
			self.drink = self.drink + 2
			verbs = []

#1160 IF o>c1 AND o<c3 THEN LET l(o)=-81

		if ((o > self.CONST_C1) & (o < self.CONST_C3)):
			self.items[o - 1][2] = -81

#1170 IF a=-1 THEN LET f$="TAKEN": LET x=x+4: LET e=e+1: IF f(o)>1 THEN LET f(o)=0

		if len(verbs) == 0:
			self.status = "TAKEN."
			self.wisdom = self.wisdom + 4
			if self.items[o - 1][3] > 1:
				self.items[o - 1][3] = 0

#1180 IF b$<>"246046"OR l(11)=0 THEN RETURN 

		if ((self.state != '246046') | (self.items[10][2] == 0)):
			return

#1190 LET f$=u$: LET l(o)=r: IF FN r(3)<3 THEN RETURN 

		self.status = "YOU ANGER THE BIRD"
		self.items[o - 1][2] = self.location
		if random.randint(1, 3) < 3:
			return

#1200 LET a$="#"+u$+r$

		self.__slow_print("#YOU ANGER THE BIRD, AND IT FLIES YOU TO A REMOTE PLACE")

#1210 LET r=63+FN r(6): LET l(16)=1: LET f$=""

		self.location = 63 + random.randint(1, 6)
		self.items[15][2] = 1
		self.status = ''

#1220 GO SUB 2740: RETURN 

		return


if __name__ == "__main__":

	game = Game()
	while not game.over:
		print('\n'.join(game.prose()))
		game.input(input().upper())
