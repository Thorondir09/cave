import time

w = 960
h = 540

highscore = 0



def setup():
  global grav, topseed, botseed, offseed, speed, rad, startstamp, roof, floor, player
  grav = 1
  topseed = int(random(1000))
  botseed = int(random(1000))
  offseed = int(random(1000))
  speed = 5
  rad = 10
  startstamp = time.time()

  size(w,h)
  ellipseMode(RADIUS)

  roof = terrain('roof')
  floor = terrain('floor')

  player = plane((roof.mid + floor.mid)/2)


def lose():
  global highscore
  if currentT > highscore:
    highscore = int(currentT)
  setup()

class plane:
  def __init__(self, spawnpos):
    self.y = spawnpos
    self.force = 0
    self.c = color(0,200,0)

  def display(self):

    fill(self.c)

    if self.force < 5: self.force += grav
    self.y += self.force

    pushMatrix()
    translate(w/2, self.y)
    ellipse(0,0,rad,rad)
    popMatrix()

class terrain:
  def __init__(self, mode):
    self.mode = mode
    self.x = 0
    self.vertices = []
    self.mid = 0

    self.gen()

  def gen(self):

    pushMatrix()
    fill(color(240, 180, 70))
    if self.mode == 'floor': translate(0, h - 250)
    else: translate(0, 150)

    noisemult = 125
    noisescale = 0.01

    beginShape()

    self.vertices = []
    offmult = 150
    noiseSeed(offseed)

    for i in range(w):
      pos = self.x + i
      y = noise(pos*noisescale)*offmult
      self.vertices.append([i,y])

    if self.mode == 'floor': noiseSeed(botseed)
    else: noiseSeed(topseed)
    ymax = 0

    for i in range(w):
      pos = self.x + i
      y = noise(pos*noisescale)*noisemult      
      self.vertices[i][1] += y
      if self.vertices[i][1] < ymax:
        ymax = self.vertices[i][1]
      vertex(i, self.vertices[i][1])
    if self.mode == 'floor':
      vertex(w , ymax+250)
      vertex(0 , ymax+250)
    elif self.mode == 'roof':
      vertex(w , -150)
      vertex(0 , -150)

    self.mid = self.getGlobalPos(self.vertices[w/2][1])

    endShape(CLOSE)
    popMatrix()
    self.x += speed


  def getGlobalPos(self,y):
    if self.mode == 'floor': return h + y - 250
    else: return y + 150 

  def display(self):

    self.gen()

    for i in self.vertices[w/2-rad:w/2+rad+1]:
      if (dist(w/2, player.y, i[0], h + i[1] - 250) < rad and self.mode == 'floor') or (dist(w/2, player.y, i[0], i[1] + 150) < rad and self.mode == 'roof'):
        lose()

def keyPressed():
  global player
  if keyCode == UP or key == ' ': player.force = -10


def draw():
  global currentT
  currentT = time.time()-startstamp
  background(255)



  player.display()

  roof.display()
  floor.display()

  textAlign(LEFT, TOP)
  fill(0)
  textSize(50)
  text("SCORE: %d" %(int(currentT)), 25, 25)
  text("HIGHSCORE: %d" %(highscore), 25, 80)
