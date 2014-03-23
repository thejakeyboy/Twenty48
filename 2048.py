import random
import numpy as np
from time import sleep
from multiprocessing import Process, Value


def shift(arr):
  nonzeros = sum(arr>0)
  arr[:nonzeros] = arr[arr > 0]
  arr[nonzeros:] = 0

def arrange(arr):
  shift(arr)
  for ind in range(len(arr) - 1):
    if arr[ind] == arr[ind+1]:
      arr[ind],arr[ind+1] = 2 * arr[ind], 0
  shift(arr)


class TileGame(object):
  def __init__(self,X = None):
    super(TileGame, self).__init__()
    # if X is None:
    self.X = np.array([
          [0,0,0,0],
          [0,0,0,0],
          [0,0,0,0],
          [0,0,0,0]])
    if X is not None:
      self.X = X.copy()
      # for i in range(4):
      #   for j in range(4):
      #     self.X[i,j] = X[i,j]
    else:
      for numiter in range(2):
        if not self.add_random_piece():
          print "this is happenng at the beginning!"
     # self.X = X.copy()
    self.num_moves = 0

  def score(self):
    return self.X.sum()

  def add_random_piece(self):
    pair = self.pick_rand_slot()
    if pair is False:
      print "Game is finished! You LOSE!"
      # print self.X
      return False
    else:
      i,j = pair
      self.X[i,j] = 2 if np.random.rand() < .9 else 4
      return True

  def get_open_slots(self):
    return [(i,j) for i in range(4) for j in range(4) if self.X[i,j] == 0]

  def get_full_slots(self):
    return [(i,j) for i in range(4) for j in range(4) if self.X[i,j] != 0] 

  def pick_rand_slot(self):
    # print "open slots: " + str(self.get_open_slots())
    open_slots = self.get_open_slots()
    if len(open_slots) == 0:
      return False
    ind = np.random.random_integers(0,len(open_slots)-1)
    return open_slots[ind]

  def __str__(self):
    return "\n".join(map( 
          lambda row: "\t".join(map(
            lambda v: str(v) if v > 0 else "", 
            row)), self.X))

  def is_dead(self):
    if len(self.get_open_slots()) > 0: return False
    for i,j in self.get_full_slots():
      for pair in [(i,j+1), (i+1,j)]:
        (newi,newj) = pair
        if newi > 3 or newj > 3: continue
        if self.X[i,j] == self.X[newi,newj]: return False
    return True

  def move(self,action=None):
    if action is None: action = np.random.choice(['up','down','left','right'])
    oldX = self.X.copy()
    for index in range(4):
      if action == 'up': lst = self.X[:,index]
      if action == 'down': lst = self.X[::-1,index]
      if action == 'left': lst = self.X[index,:]
      if action == 'right': lst = self.X[index,::-1]
      arrange(lst)
    notchanged = (oldX == self.X).all()
    if notchanged: return False
    else:
      if not self.add_random_piece():
        print "what is this"
        print oldX
        print self.X
        print "hello there"
      self.num_moves += 1
    return True

  def run_until_dead(self):
    while not self.is_dead(): self.move()

  def estimate_score(self,numiter=50):
    vals = []
    for i in range(numiter):
      # print "ITER %i" % i
      t = TileGame(self.X)
      t.run_until_dead()
      vals.append(t.score())
    return np.mean(vals)

  def estimate_moves(self):
    perfs = dict()
    for action in ['up','down','left','right']:
      # print "checking action %s" % action
      t = TileGame(self.X)
      response = t.move(action=action)
      if response:
        perfs[action] = self.estimate_score()
        # perfs[action] = estimate_score(self.X)
    return perfs

  def take_best_move(self):
    perfs = self.estimate_moves()
    best_action = max(perfs.keys(), key=lambda x: perfs[x])
    self.move(best_action)
    return best_action

def op(X,value):
  t = TileGame(X)
  t.run_until_dead()
  value.value += t.score()

def estimate_score(X,numiter=50):
  total = Value('i',0)
  pool = []
  for i in range(numiter):
    pool.append(Process(target=op, args=(X, total)))
  for p in pool: p.start()
  for p in pool: p.join()
  return float(total.value) / numiter



if __name__ == '__main__':
  t = TileGame()
  print t
  for i in range(4):
  # while not t.is_dead():
    print "best action is %s" % t.take_best_move()
    print t
  # numiter = 0
  # while not t.is_dead():
  #   numiter += 1
  #   # print "*" * 25
  #   # print "BEFORE--------------------"
  #   # print t
  #   t.move()
  #   # print "AFTER---------------------"
  #   # print t 
  #   # sleep(0.3)
  # print t
  # print numiter
  # print t.X.sum()


  


    