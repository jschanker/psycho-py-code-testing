from enum import Enum
from psychopy import sound, visual, core, event, constants  # import some libraries from PsychoPy
from time import time
# from functools import partial

def findOneIndex(arr, f):
  for i in range(len(arr)):
    if f(arr[i]):
      return i

  return -1
  
def addImages(win, filePaths, vPadding=10, hPadding=10, scaleToFit=True):
  fitNum = len(filePaths)
  availableX = (win.size[0] - (fitNum + 1) * hPadding)/fitNum
  availableY = 2000*(win.size[1] - 2 * vPadding)
  imgs = [visual.ImageStim(win, filePath, units="pix", anchor="left") for filePath in filePaths]
  imgSizeRatio = min(*[min(availableX/img.size[0], availableY/img.size[1]) for img in imgs])
  
  if (not scaleToFit): imgSizeRatio = min(imgSizeRatio, 1)
  
  for index in range(len(imgs)):
    img = imgs[index]
    # if fp != '': # actual image, not used for placeholder
    img.size = [imgSizeRatio * img.size[0], imgSizeRatio * img.size[1]]
    img.pos[0] = (index + 1) * hPadding + index * img.size[0] - win.size[0]/2
    # img.pos[0] = -1
    print("x", img.pos[0])
    
  def initImgs():
    [img.draw() for img in imgs]
    win.flip()
    return imgs
  
  return initImgs
  
def addSound(win, soundPath):
  snd = sound.Sound(soundPath)
  
  def initSound():
    win.flip()
    # nextFlip = win.getFutureFlipTime(clock='ptb')
    # sound.play(when=nextFlip)
    snd.play()
    return snd

  return initSound

#win.flip()
    

HPosition = Enum('Position', ['LEFT', 'CENTER', 'RIGHT'])
VPosition = Enum('Position', ['TOP', 'MIDDLE', 'BOTTON'])

def addMovie(win, filePath, xPosition=HPosition.CENTER, yPosition=VPosition.MIDDLE, fitNum=2, vPadding=10, hPadding=10):
  mov = visual.MovieStim(
    win,
    filePath,    # path to video file
    #size=(640, 318),
    #units='pix',
    #size=None,
    pos=(0,0),
    flipVert=False,
    flipHoriz=False,
    loop=False,
    noAudio=False,
    volume=0.1,
    autoStart=False)
  availableX = (win.size[0] - (fitNum + 1) * hPadding)/fitNum
  availableY = (win.size[1] - 2 * vPadding)
  videoSizeRatio = min(1, availableX/mov.videoSize[0], availableY/mov.videoSize[1])
  mov.size = [videoSizeRatio * mov.videoSize[0], videoSizeRatio * mov.videoSize[1]]
  
  if xPosition == HPosition.LEFT:
    mov.pos[0] -= win.size[0]/2 - mov.size[0]/2 - hPadding

  if xPosition == HPosition.RIGHT:
    mov.pos[0] += win.size[0]/2 - mov.size[0]/2 - hPadding
  
  return mov

def soundIsFinished(retVal=None):
  return retVal.status == constants.FINISHED

def pressedEnter(retVal=None):
  return event.getKeys('return') or event.getKeys('q')
  
def timeElapsed(s):
  start = time()
  
  def timePassed(retVal=None):
    return time() - start >= s
    
  return timePassed
  
def doNothing(retVal=None):
  pass
  
def pressedIn(m): 
  def mousePressed(stimuli):
    return any([m.isPressedIn(stim) for stim in stimuli])
    
  return mousePressed

def every(conditions):
  def everyCond(args):
    return all([condition(args) for condition in conditions])
    
  return everyCond
  
def some(conditions):
  def someCond(args):
    return any([condition(args) for condition in conditions])
    
  return someCond
  
def stopSound(arg=None):
  arg.stop()
  
def calculateCorrect(correctArr, index):
  def addCorrect(stimuli):
    selectedIndex = findOneIndex(stimuli, lambda stim: m.isPressedIn(stim))
    correctArr.append(selectedIndex == index)
      
  return addCorrect

def runTrial(initFunc, repeatFunc, isCompleteFunc, finishFunc=doNothing, times=[]):
  retVal = initFunc()
  startTime = time()
  while(not isCompleteFunc(retVal)):
    repeatFunc(retVal)
  timeElapsed = time() - startTime
  finishFunc(retVal)
  times.append(timeElapsed)
  return timeElapsed

# Start experiment
mywin = visual.Window([1600,700], monitor="testMonitor", units="pix")
#print("POS", mywin.pos)
#mywin.pos = (0, mywin.pos[1])
#print("POS", mywin.pos)
correctArr = []
times = []
smile = addImages(mywin, ['smile.png', 'smile.png', 'smile.png'])
instructions = addSound(mywin, "Toreador-clipped.wav")
m = event.Mouse(win=mywin)
runTrial(instructions, doNothing, some([soundIsFinished, pressedEnter]), stopSound)
runTrial(smile, doNothing, some([pressedEnter, pressedIn(m)]), calculateCorrect(correctArr, index=1), times)
print("Results", correctArr, times)
# runTrial(smile, doNothing, timeElapsed(6))
# runTrial(smile, doNothing, pressedEnter)

# clean up and exit
mywin.close()
core.quit()
