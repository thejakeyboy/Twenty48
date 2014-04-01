import random
from time import sleep
# from multiprocessing import Process, Value


indmap = dict()
for action in ['up','down','left','right']:
  for index in range(4):
    if action =='left':
      indmap[(action,index)] = [4*index + y for y in range(4)]
    if action =='right':
      indmap[(action,index)] = [4*index + (3-y) for y in range(4)]
    if action =='down':
      indmap[(action,index)] = [index + 4 * y for y in range(4)]
    if action =='up':
      indmap[(action,index)] = [(3-index) + 4 * y for y in range(4)]

def update(array,inds,k,p1,p2):
  print "p1 = %i p2 = %i ---- %s" % (p1,p2,str(array))
  if p2 >= k: return False
  elif array[inds[p2]] == 0: return update(array,inds,k,p1,p2+1)
  elif array[inds[p1]] == 0: 
    array[inds[p1]] = array[inds[p2]]
    array[inds[p2]] = 0
    update(array,inds,k,p1,p2+1)
    return True
  elif array[inds[p1]] == array[inds[p2]]:
    array[inds[p1]] = 2*array[inds[p1]]
    array[inds[p2]] = 0
    update(array,inds,k,p1+1, p2+1)
    return True
  elif p2 > p1 + 1: return update(array,inds,k,p1+1,p2)
  else: return update(array,inds,k,p1+1,p2+1)

def arrange_arr(arr,inds):
  k = len(inds)
  return update(arr,inds,k,0,1)

class TileGame(object):
  def __init__(self,X = None):
    super(TileGame, self).__init__()
    self.X = [0]*16
    if X is not None:
      self.X = X + []
    else:
      for numiter in range(2):
        if not self.add_random_piece():
          print "this is happenng at the beginning!"
    self.num_moves = 0
  def __repr__(self):
    show = lambda x: str(x) if x > 0 else "."
    return "<TileGame nummoves=%i \n %s \n ---------------------->" % (self.num_moves,str(self))

  def set(self,i,j,val):
    self.X[4*i + j] = val

  def get(self,i,j):
    return self.X[4*i + j]

  def score(self):
    return sum(sum(self.X))

  def add_random_piece(self):
    pair = self.pick_rand_slot()
    if pair is False:
      print "Game is finished! You LOSE!"
      # print self.X
      return False
    else:
      print "the pair is %s" % str(pair)
      i,j = pair
      val = 2 if random.random() < .9 else 4
      self.set(i,j,val)
      return True

  def get_open_slots(self):
    return [(i,j) for i in range(4) for j in range(4) if self.get(i,j) == 0]

  def get_full_slots(self):
    return [(i,j) for i in range(4) for j in range(4) if self.get(i,j) != 0] 

  def pick_rand_slot(self):
    open_slots = self.get_open_slots()
    if len(open_slots) == 0:
      return False
    ind = random.randint(0,len(open_slots)-1)
    return open_slots[ind]

  def __str__(self):
    def read(val):
      return str(val) if val > 0 else "."
    strarr = [[read(self.get(i,j)) for j in range(4)] for i in range(4)]
    return "\n".join(map((lambda row: "\t".join(row)), strarr))

  def is_dead(self):
    if len(self.get_open_slots()) > 0: return False
    for i,j in self.get_full_slots():
      for pair in [(i,j+1), (i+1,j)]:
        (newi,newj) = pair
        if newi > 3 or newj > 3: continue
        if self.get(i,j) == self.get(newi,newj): return False
    return True

  def move(self,action=None):
    if action is None: action = random.choice(['up','down','left','right'])
    moved = False
    for index in range(4):
      inds = indmap[(action,index)]
      result = arrange_arr(self.X,inds)
      moved = moved or result

    if moved:
      if not self.add_random_piece():
        print "what is this"
        print oldX
        print self.X
        print "hello there"
      self.num_moves += 1
      return True
    else: return False

  def run_until_dead(self):
    while not self.is_dead(): self.move()

  def estimate_score(self,numiter=50):
    vals = []
    for i in range(numiter):
      # print "ITER %i" % i
      t = TileGame(self.X)
      t.run_until_dead()
      vals.append(t.score())
    return sum(vals)/float(numiter)

  def estimate_moves(self):
    perfs = dict()
    for action in ['up','down','left','right']:
      # print "checking action %s" % action
      t = TileGame(self.X)
      response = t.move(action=action)
      if response: perfs[action] = self.estimate_score()
      # perfs[action] = estimate_score(self.X)
    return perfs

  def take_best_move(self):
    perfs = self.estimate_moves()
    best_action = max(perfs.keys(), key=lambda x: perfs[x])
    self.move(best_action)
    return best_action

# def op(X,value):
#   t = TileGame(X)
#   t.run_until_dead()
#   value.value += t.score()

# def estimate_score(X,numiter=50):
#   total = Value('i',0)
#   pool = []
#   for i in range(numiter):
#     pool.append(Process(target=op, args=(X, total)))
#   for p in pool: p.start()
#   for p in pool: p.join()
#   return float(total.value) / numiter



# if __name__ == '__main__':
#   t = TileGame()
#   print t
#   # for i in range(4):
#   while not t.is_dead():
#   print "best action is %s" % t.take_best_move()
#   print t
#   # numiter = 0
#   # while not t.is_dead():
#   #   numiter += 1
#   #   # print "*" * 25
#   #   # print "BEFORE--------------------"
#   #   # print t
#   #   t.move()
#   #   # print "AFTER---------------------"
#   #   # print t 
#   #   # sleep(0.3)
#   # print t
#   # print numiter
#   # print t.X.sum()


  


  