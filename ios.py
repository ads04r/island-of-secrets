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
		self.verbs = ["", "", "", "", "GO", "GET", "TAK", "GIV", "DRO", "LEA", "EAT", "DRI", "RID", "OPE", "PIC", "CHO", "CHI", "TAP", "BRE", "FIG", "STR", "ATT", "HIT", "KIL", "SWI", "SHE", "HEL", "SCR", "CAT", "RUB", "POL", "REA", "EXA", "FIL", "SAY", "WAI", "RES", "WAV", "INF", "XLO", "XSA", "QUI"]
		self.status = "LET YOUR QUEST BEGIN."
		self.state = ""
		self.over = False

		self.location = 23
		self.time_remaining = 1000
		self.strength = 100
		self.wisdom = 35
		self.food = 2
		self.drink = 2
		self.items_held = 0

		self.CONST_C1 = 16
		self.CONST_C2 = 21
		self.CONST_C3 = 24
		self.CONST_C4 = 43

	def __s(self):
		return int(self.strength - (self.items_held / self.CONST_C4 + .1))

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

	def __lookup_word(self, word, verb_priority=False):

		if word == 'TO':
			return []

		vc = len(self.verbs)
		nc = len(self.items)
		if not verb_priority:
			for i in range(0, nc):
				if self.items[i][0].startswith(word[0:3]):
					return [False, i + 1]
		for i in range(0, vc):
			if self.verbs[vc - (i + 1)].startswith(word[0:3]):
				return [True, vc - i]
		return []

	def __parse(self, text):

		nouns = []
		verbs = []
		words = text.upper().strip().split(' ')
		if len(words) == 1:
			if words[0] != 'EAT':
				direction = words[0]
				if direction == 'N':
					direction = 'NORTH'
				if direction == 'S':
					direction = 'SOUTH'
				if direction == 'W':
					direction = 'WEST'
				if direction == 'E':
					direction = 'EAST'
				words = ['GO', direction]
		for word in words:
			item = self.__lookup_word(word, verb_priority=((len(verbs) == 0) & (len(word) > 1)))
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

		print('\033[96m' + json.dumps(v) + '\033[0m')
		print('\033[96m' + json.dumps(n) + '\033[0m')
		print('\033[96m' + self.state + '\033[0m')

		self.time_remaining = self.time_remaining - 1
		self.strength = self.__s()
		self.status = ''

		if (((len(v) == 0) | ('GO' in v)) & (len(n) > 0)):
			self.__cmd_move(n, self.state)
		if ((('GET' in v) | ('TAK' in v) | ('PIC' in v) | ('CAT' in v)) & (len(n) > 0)):
			self.__cmd_get(v, n, self.state)
		if 'GIV' in v:
			self.__cmd_give(n, self.state)
		if 'OPE' in v:
			self.__cmd_open(self.state)
		if (('LEA' in v) | ('DRO' in v)):
			self.__cmd_drop(v, n, self.state)
		if 'EAT' in v:
			self.__cmd_eat(n, self.state)
		if 'DRI' in v:
			self.__cmd_drink(n, self.state)
		if 'SAY' in v:
			self.__cmd_say(self.state, text.strip().split(' ', maxsplit=1)[-1])

		if self.strength <= 0:
			self.over = True
		if self.time_remaining <= 0:
			self.over = True
		if 'QUI' in v:
			self.over = True

		return

	def __logmen(self):
		
		self.status = ''
		text = '# THE LOGMEN DECIDE TO HAVE A LITTLE FUN AND '
		self.items[40][2] = 0
		self.strength = self.strength - 4
		self.wisdom = self.wisdom - 4
		if self.location < 34:
			text = text + 'THROW YOU IN THE WATER'
			self.location = 32
		if self.location > 33:
			text = text + 'TIE YOU UP IN A STOREROOM'
			self.location = 51
		self.__slow_print(text)
		for i in range(2, 4):
			if self.items[i][2] == 0:
				self.items[i][2] = 42
		return
		
	def __swampman(self):
		
		text = '* THE SWAMPMAN TELLS HIS TALE'
		self.__slow_print(text)
		self.items[31][3] = -1
		return
		
	def __median(self):
	
		text = "MEDIAN CAN DISABLE THE EQUIPMENT"
		if self.items[7][2] == 0:
			text = text + " AND ASKS YOU FOR THE PEBBLE YOU CARRY"
		return
		
	def __storm_begin(self):
		
		self.items[35][3] = 0 - randint(7, 10)
		self.status = "A STORM BREAKS OVERHEAD!"
		return
		
	def __storm_continue(self):
		
		self.__slow_print("//// LIGHTNING FLASHES!")
		self.items[38][2] = self.location
		self.strength = self.strength - 8
		self.wisdom = self.wisdom - 2
		return

	def __swimming(self):
	
		# I've bodged this a bit because I'm not 100% on how it's supposed to work

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

		if self.wisdom < 60:
			text = "#TO SERVE OMEGAN FOREVER!"
			self.over = True
		else:
			text = "#THE BOAT SKIMS THE DARK SILENT WATERS"
			self.location = 57
		self.__slow_print(text)

		return

	def __cmd_get(self, verbs, nouns, state):

		v = 42
		w = 51
		o = self.__word_id(nouns[0][0])

		if ((((self.items[o - 1][3] > 0) & (self.items[o - 1][3] < 9)) | (self.items[o - 1][2] != self.location)) & (o <= self.CONST_C3)):
			self.status = "WHAT ITEM DO YOU MEAN?"
			return

		if state == '3450050':
			self.strength = self.strength - 8
			self.wisdom = self.wisdom - 5
			self.status = "THEY ARE CURSED."
			return

		if state == '3810010':
			self.__slow_print("////LIGHTNING FLASHES!")
			self.items[38][2] = self.location
			self.strength = self.strength - 8
			self.wisdom = self.wisdom - 2

		if ((('PIC' in verbs) & (o != 20) & (o != 1)) | (('CAT' in verbs) & (o != 16)) | (o > self.CONST_C3)):
			self.status = "YOU CAN'T DO THAT."
			return

		if ((self.items[o - 1][2] == self.location) & ((self.items[o - 1][3] < 1) | (self.items[o - 1][3] == 9)) & (o < self.CONST_C3)):
			verbs = []
			self.items[o - 1][2] = 0

		if ((o == 16) & (self.items[9][2] != 0)):
			self.items[o - 1] = self.location
			self.status = "IT ESCAPED."
			verbs = ['']

		if ((o > self.CONST_C1) & (o < self.CONST_C2)):
			self.food = self.food + 2
			verbs = []

		if ((o >= self.CONST_C2) & (o <= self.CONST_C3)):
			self.drink = self.drink + 2
			verbs = []

		if ((o > self.CONST_C1) & (o < self.CONST_C3)):
			self.items[o - 1][2] = -81

		if len(verbs) == 0:
			self.status = "TAKEN."
			self.wisdom = self.wisdom + 4
			self.items_held = self.items_held + 1
			if self.items[o - 1][3] > 1:
				self.items[o - 1][3] = 0

		if ((self.state != '246046') | (self.items[10][2] == 0)):
			return

		self.status = "YOU ANGER THE BIRD"
		self.items[o - 1][2] = self.location
		if random.randint(1, 3) < 3:
			return

		self.__slow_print("#YOU ANGER THE BIRD, AND IT FLIES YOU TO A REMOTE PLACE")

		self.location = 63 + random.randint(1, 6)
		self.items[15][2] = 1
		self.status = ''

		return

	def __cmd_give(self, nouns, state):

		v = 42
		w = 51
		item = None
		target = None
		for word in nouns:
			o = self.__word_id(word[0])
			if ((item is None) & (o <= self.CONST_C3) & (o != self.CONST_C1)):
				word.append(o)
				item = word
			if ((target is None) & (o > self.CONST_C3) & (o <= self.CONST_C4)):
				word.append(o)
				target = word

		self.status = "IT IS REFUSED."

		if item is None:
			self.status = "UNRECOGNISED ITEM."
			return

		o = item[-1]

		if (((o != 24) & (self.items[o - 1][2] > 0)) | (o == 52)):
			self.status = "YOU DON'T HAVE THAT ITEM."
			return

		if target is None:
			self.status = "GIVE IT TO WHOM?"
			return

		n = target[-1]

		if self.location != self.items[n - 1][2]:
			self.status = target[1] + " IS NOT HERE."
			return

		if ((state == '10045') & (n == 40)):
			self.items[o - 1][2] = 81
			self.items[39][3] = 1
			self.status = "THE SNAKE UNCURLS."
			return

		if ((state == '2413075') & (n == 30) & (self.drink > 1)):
			self.items[10][3] = 0
			self.drink = self.drink - 1
			self.status = "HE OFFERS HIS STAFF."
			return

		if ((state[0:3] == '300') & (n == 42)):
			self.wisdom = self.wisdom + 10
			self.items[o - 1][2] = 81

		if ((state[0:3] == '120') & (n == 42)):
			self.wisdom = self.wisdom + 10
			self.items[o - 1][2] = 81

		if ((state[0:3] == '40-') & (n == 32)):
			self.items[n - 1][3] = 1
			self.items[o - 1][2] = 81

		if ((state[0:2] == '80') & (n == 43)):
			self.items[o - 1][2] = 81
			para = "*HE TAKES IT"
			if self.location != 8:
				para = para + ", RUNS DOWN THE CORRIDOR,"
			para = para + " AND CASTS IT INTO THE CHEMICAL VATS"
			self.__slow_print(para)
			self.__slow.print("PURIFYING THEM WITH A CLEAR BLUE LIGHT REACHING FAR INTO THE LAKES AND RIVERS BEYOND.")
			self.items[7][3] = -1
			return

		if ((self.items[o - 1][2] == 81) | ((o == 24) & (self.items[10][2] > 0) & (self.drink > 0))):
			self.status = "IT IS ACCEPTED"

		if n == 41: # LOGMEN
			self.items[o - 1][2] = 51
			self.status = "IT IS TAKEN"

		return
		
	def __cmd_drop(self, verbs, nouns, state):

		v = 42
		w = 51
		o = self.__word_id(nouns[0][0])
		if 'DRO' in verbs:
			if ((o == 4) & (self.items[o - 1][2] == 0)):
				self.wisdom = self.wisdom - 1
				self.status = "IT BREAKS!"
				return
		if ((self.items[o - 1][2] < self.CONST_C1) & (self.items[o - 1][2] == 0)):
				self.items[o - 1][2] = self.location
				self.status = "NO LONGER CARRYING " + self.items[o - 1][1]
				self.items_held = self.items_held - 1
		return

	def __cmd_break(self, verbs, nouns, state):
		v = 42
		o = self.__word_id(nouns[0][0])
		self.strength = self.strength - 2
		if state == '3577077':
			if self.items[8][2] == 0:
				self.items[22][3] = 0
				self.items[22][2] = self.location
		if ((v > 15) & (v < 19) & ((self.items[8][2] == 0) | (self.items[14][2] == 0))):
			self.status = 'OK'
		if (((state == '1258158') | (state == '2758158')) & (self.items[14][2] == 0)):
			self.items[11][3] = 0
			self.items[26][3] = 0
			self.status = 'CRACK!'
		if ((state[0:4] == '1100') & (self.location == 10)):
			self.__endgame(o)
		if 'TAP' in verbs:
			if ((o == 16) | ((o > 29) & (o < 34)) | ((o > 38) & (o < 44))):
				self.__cmd_kill(o)
		return

	def __cmd_fight(self, state):
		return

	def __cmd_kill(self, o):
		w = 51
		if self.items[8][2] > 0:
			return
		self.strength = self.strength - 12
		self.wisdom = self.wisdom - 10
		self.status = "THAT WOULD BE UNWISE!"
		if self.location != self.items[o - 1][2]:
			return
		self.items[w - 1][3] = 1
		self.status == ''
		self.__slow_print("# A THUNDER SPLITS THE SKY! IT IS THE TRIUMPHANT VOICE OF OMEGAN.")
		self.__slow_print("# WELL DONE ALPHAN! THE MEANS BECOME THE END.. I CLAIM YOU AS MY OWN! HA HA HAH!")
		self.time_remaining = 0
		self.strength = 0
		self.wisdom = 0
		return
		
	def __cmd_say(self, state, text):
		self.status = text
		if ((text == 'STONY WORDS') & (self.location == 47) & (self.items[7][3] == 0)):
			self.items[43][3] = 1
			self.status = "THE STONES ARE FIXED"
		if ((text != "REMEMBER OLD TIMES") | (self.location != self.items[41][2]) | (self.items[2][2] < 81) | (self.items[11][2] < 81)):
			return
		self.status = "HE EATS THE FLOWERS - AND CHANGES"
		self.items[41][3] = 1
		self.items[42][3] = 0
		return

	def __endgame(self, o):
		return

	def __cmd_open(self, state):

		if state == '2644044':
			self.status = "CHEST OPEN."
			self.items[5][3] = 9
			self.items[4][3] = 9
			self.items[14][3] = 9

		if state == '2951151':
			self.status = "THE TRAPDOOR CREAKS."
			self.items[28][3] = 0
			self.wisdom = self.wisdom + 3

		return

	def __cmd_eat(self, nouns, state):

		v = 42
		w = 51
		if len(nouns) == 0:
			o = 0
		else:
			o = self.__word_id(nouns[0][0])
		if (((o > 0) & (o < self.CONST_C1)) | (o > self.CONST_C3)):
			self.status = "YOU CAN'T EAT THAT."
			self.wisdom = self.wisdom - 1
			return
		self.status = "YOU HAVE NO FOOD."
		if self.food > 0:
			self.food = self.food - 1
			self.strength = self.strength + 10
			self.status = "OK"
		if o == 3:
			self.wisdom = self.wisdom - 5
			self.strength = self.strength - 2
			self.status = "THEY MAKE YOU VERY ILL!"
		return

	def __cmd_drink(self, nouns, state):

		v = 42
		w = 51
		if len(nouns) == 0:
			o = 0
		else:
			o = self.__word_id(nouns[0][0])
		if o == 31:
			pass # TODO replace with 'drunk' routine
		if (((o > 0) & (o < self.CONST_C1)) | (o > self.CONST_C3)):
			self.status = "YOU CAN'T DRINK THAT."
			self.wisdom = self.wisdom - 1
			return
		if self.drink > 0:
			self.drink = self.drink - 1
			self.strength = self.strength + 7
			self.status = "OK"
		return

if __name__ == "__main__":

	game = Game()
	while not game.over:
		print('\n'.join(game.prose()))
		game.input(input().upper())
	print(game.status)
