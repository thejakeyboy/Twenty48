from twenty48 import Twenty48

class Twenty48Strategy(Twenty48):
  """docstring for Twenty48Strategy"""
  def __init__(self,X=None):
    super(Twenty48Strategy, self).__init__(X)
    
  def estimate_score(self,numiter=50):
    # raise NotImplementedError("You haven't implemented this yet")
    vals = []
    for i in range(numiter):
      t = Twenty48(self.X)
      t.run_until_dead()
      vals.append(t.score())
    return sum(vals)/float(numiter)

  def estimate_moves(self,numiter=50):
    perfs = dict()
    for action in ['up','down','left','right']:
      t = Twenty48Strategy(self.X)
      response = t.move(action=action)
      if response: perfs[action] = t.estimate_score(numiter=numiter)
    return perfs

  def take_best_move(self,numiter=50):
    perfs = self.estimate_moves(numiter=numiter)
    print perfs
    best_action = max(perfs.keys(), key=lambda x: perfs[x])
    self.move(best_action)
    return best_action


if __name__ == '__main__':
  t = Twenty48Strategy()
  print t
  while not t.is_dead():
    print "best action is %s" % t.take_best_move(numiter=50)
    print t
