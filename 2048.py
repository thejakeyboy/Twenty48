import random

class Tile(int):
	# def __init__(self, val=2):
	# 	super(Tile, self).__init__()
	# 	self.val = val

	# def inc(self):
	# 	self.val = self.val * 2

	# def combine(self,tile):
	# 	if self.val != tile.val:
	# 		raise Exception()
	# 	tile.inc()

	def __str__(self):
		if self == 0:
			return 
		return "%i"%self.val

def shift(arr):
	nonzeros = sum(arr>0)
	arr[:nonzeros] = arr[arr > 0]
	arr[nonzeros:] = 0

def arrange(arr):
	shift(arr)
	indold, indnew = 0,0
	while True:
		if indnew >= len(arr): break
		if indold < len(arr) - 1:
			if arr[indold] == arr[indold+1]:
				arr[indnew] = arr[indold]*2
				indold = indold + 2
			else:
				arr[indnew] = arr[indold]
				indold += 1
		else: arr[indnew] = 0
		indnew += 1

rrr = np.array([0, 2, 4,4 ,2, 0, 2, 2, 4, 32, 32, 32, 0, 0, 4, 4, 4])

arrange(rrr)
print rrr


class TileGame(object):
	def __init__(self):
		super(TileGame, self).__init__()
		self.X = np.array([
					[0,0,0,0],
					[0,0,0,0],
					[0,0,0,0],
					[0,0,0,0]])
		for numiter in range(2): self.add_random_piece()

	def add_random_piece(self):
		pair = self.pick_rand_slot()
		if pair is False:
			print "Game is finished! You LOSE!"
			return False
		else:
			i,j = pair
			X[i,j] = 2 if np.random.rand() < .9 else 4

	def get_open_slots(self):
		return [(i,j) for i in range(4) for j in range(4) if self.X[i,j] > 0] 

	def pick_rand_slot(self):
		open_slots = self.get_open_slots()
		if len(open_slots) == 0:
			return False
		return random.choice(open_slots)

	def __str__(self):
		return "\n".join(map( 
					lambda row: "\t".join(map(
						lambda v: str(v) if v > 0 else "", 
						row)),
					X))
		# return "\n".join(["".join(["\t" + str(item) + "\t" for item in row]) for row in self.X])

	def move(self,action=np.random.choice('up','down','left','right')):
		for index in range(4):
			if action == 'up': lst = X[:,index]
			if action == 'down': lst = X[::-1,index]
			if action == 'left': lst = X[index,:]
			if action == 'right': lst = X[index,::-1]
			arrange(lst)



	# def arrange_row(self,rowind,rev=False):
	# 	indices = [(rowind,i) for in range(4)]
	# 	if rev: indices.reverse()
	# 	tiles = [self.X[i][j] for (i,j) in indices if self.X[i][j] is not None]
	# 	new_tiles = arrange(tiles)
	# 	for pair_ind, (i,j) in enumerate(indices)


t = TileGame()

print t


		