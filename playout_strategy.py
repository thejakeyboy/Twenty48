from 2048 import TileGame

class PlayoutStrategy(TileGame):
  """docstring for PlayoutStrategy"""
  def __init__(self):
    super(PlayoutStrategy, self).__init__()
    
  def estimate_score(self,numiter=50):
    vals = []
    for i in range(numiter):
      t = TileGame(self.X)
      t.run_until_dead()
      vals.append(t.score())
    return sum(vals)/float(numiter)

  def estimate_moves(self,numiter=50):
    perfs = dict()
    for action in ['up','down','left','right']:
      t = TileGame(self.X)
      response = t.move(action=action)
      if response: perfs[action] = self.estimate_score(numiter=numiter)
    return perfs

  def take_best_move(self,numiter=50):
    perfs = self.estimate_moves(numiter=numiter)
    print perfs
    best_action = max(perfs.keys(), key=lambda x: perfs[x])
    self.move(best_action)
    return best_action


if __name__ == '__main__':
  t = PlayoutStrategy()
  print t
  # for i in range(4):
  while not t.is_dead():
    print "best action is %s" % t.take_best_move(numiter=50)
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