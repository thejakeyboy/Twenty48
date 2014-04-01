import random

indmap = dict()
for action in ['up','down','left','right']:
  for index in range(4):
    if action =='left':
      indmap[(action,index)] = [4*index + y for y in range(4)]
    if action =='right':
      indmap[(action,index)] = [4*index + (3-y) for y in range(4)]
    if action =='down':
      indmap[(action,index)] = [index + 4 * (3-y) for y in range(4)]
    if action =='up':
      indmap[(action,index)] = [index + 4 * y for y in range(4)]

def update(array,inds,k,p1,p2):
  # print "p1 = %i p2 = %i ---- %s" % (p1,p2,str(array))
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
    if X is not None: self.X = X + []
    else:
      self.add_random_piece()
      self.add_random_piece()
    self.num_moves = 0

  def __str__(self):
    read = lambda val: str(val) if val > 0 else "."
    strarr = [[read(self.get(i,j)) for j in range(4)] for i in range(4)]
    return "\n".join(map((lambda row: "  ".join(row)), strarr))

  def __repr__(self):
    show = lambda x: str(x) if x > 0 else "."
    return "<TileGame nummoves=%i \n%s \n ------------------------->" % (self.num_moves,str(self))

  def set(self,i,j,val): self.X[4*i + j] = val

  def get(self,i,j): return self.X[4*i + j]

  def score(self): return sum(self.X)

  def add_random_piece(self):
    pair = self.pick_rand_slot()
    if pair is False: return False
    else:
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
    if len(open_slots) == 0:  return False
    ind = random.randint(0,len(open_slots)-1)
    return open_slots[ind]

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
      self.add_random_piece()
      self.num_moves += 1
      return True
    else: return False

  def run_until_dead(self):
    while not self.is_dead(): 
      self.move()



  


  