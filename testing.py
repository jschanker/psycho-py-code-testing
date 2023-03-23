from enum import Enum
from psychopy import visual, core, event, constants  # import some libraries from PsychoPy
from time import time
from functools import partial


def every(conditionFunctions):
  return partial(all, [condition() for condition in conditions])
 
def some(conditionFunctions):
  return partial(any, [condition() for condition in conditions])
 
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
 
  return initImgs


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
 
def addImage(win, filePath, xPosition=HPosition.CENTER, yPosition=VPosition.MIDDLE, fitNum=2, vPadding=10, hPadding=10):
  img = visual.ImageStim(
    win,
    filePath,    # path to image file
    #size=(640, 318),
    #units='pix',
    #size=None,
    pos=(0,0),
    units="pix",
    flipVert=False,
    flipHoriz=False)
  print("PIX", img.size[0]/2, img.size[1]/2)
  availableX = (win.size[0] - (fitNum + 1) * hPadding)/fitNum
  availableY = (win.size[1] - 2 * vPadding)
  imgSizeRatio = min(availableX/img.size[0], availableY/img.size[1])
  img.size = [imgSizeRatio * img.size[0], imgSizeRatio * img.size[1]]
 
  if xPosition == HPosition.LEFT:
    img.pos[0] -= win.size[0]/2 - img.size[0]/2 - hPadding


  if xPosition == HPosition.RIGHT:
    img.pos[0] += win.size[0]/2 - img.size[0]/2 - hPadding
   
  #img.pos[1] = win.size[1]/2 - img.size[1]/2 + 2*vPadding
  #print("POSITION", win.size[1]/2, img.size[1]/2, img.pos[1])
 
  def initImg():
    img.draw()
    win.flip()
 
  return initImg


def pressedEnter():
  return event.getKeys('return') or event.getKeys('q')
 
def timeElapsed(s):
  start = time()
 
  def timePassed():
    return time() - start >= s
   
  return timePassed
 
def doNothing():
  pass


def runTrial(initFunc, repeatFunc, isCompleteFunc):
  initFunc()
  while(not isCompleteFunc()):
    repeatFunc()


#create a window
# mywin = visual.Window([1600,700], monitor="testMonitor", units="deg")
# 1600, 1300
#mov = addMovie(mywin,'collagen-stimuli1-sampleA.mp4')


#mov = visual.MovieStim(mywin, 'collagen-stimuli1-sampleA.mp4', flipVert=False, size=(256, 256))
'''
mov = visual.MovieStim(
    mywin,
    'collagen-stimuli1-sampleA.mp4',    # path to video file
    size=(640, 318),
    #units='pix',
    #size=None,
    #pos=(-470,0),
    anchor="left",
    flipVert=False,
    flipHoriz=False,
    loop=False,
    noAudio=False,
    volume=0.1,
    autoStart=False)


print("SIZE", mov.videoSize)


mov2 = visual.MovieStim(
    mywin,
    'collagen-stimuli2-sample/Video/collagen-stimuli2-sample.mp4',    # path to video file
    size=(640, 318),
    pos=(320, 0),
    flipVert=False,
    flipHoriz=False,
    loop=False,
    noAudio=False,
    volume=0.1,
    autoStart=False)
'''


# mov = addMovie(mywin,'collagen-stimuli1-sampleA.mp4', xPosition=HPosition.LEFT)
# mov2 = addMovie(mywin,'collagen-stimuli2-sample/Video/collagen-stimuli2-sample.mp4', xPosition=HPosition.RIGHT)
#smile = addImages(mywin, 'smile.png', xPosition=HPosition.RIGHT)
mywin = visual.Window([1600,700], monitor="testMonitor", units="pix")
#print("POS", mywin.pos)
#mywin.pos = (0, mywin.pos[1])
#print("POS", mywin.pos)
smile = addImages(mywin, ['smile.png', 'smile.png'])
m = event.Mouse(win=mywin)
runTrial(smile, doNothing, timeElapsed(6))
runTrial(smile, doNothing, pressedEnter)


'''
smile.draw()
mywin.flip()
while True:
  if event.getKeys('q'):   # quit
    break
'''


#while mov.status != constants.FINISHED:
'''
while not mov.isFinished or not mov2.isFinished:
  mov.draw()
  mov2.draw()
  # flip buffers so they appear on the window
  mywin.flip()
  if event.getKeys('q'):   # quit
    break
  elif event.getKeys('s'):  # play/start
    mov.play()
    mov2.play()
  elif m.isPressedIn(mov):
    print("Clicked movie 1")
  elif m.isPressedIn(mov2):
    print("Clicked movie 2")
  #if mov.status == constants.FINISHED:
    #print("FINISHED MOV 1")
  #except Exception as err:
  #  print(f"Unexpected {err=}, {type(err)=}")
  #  break


# stop the movie, this frees resources too
mov.stop()
mov2.stop()
'''
# clean up and exit
mywin.close()
core.quit()


#mov.play()

#mov = visual.MovieStim(mywin, 'collagen-stimuli1-sample.mp4', flipVert=False)
#print("Duration", mov.duration)
# give the original size of the movie in pixels:
#print("Dim")
#mov.draw()
#print("Dimensions", mov.format.width, mov.format.height)


#mov.draw()  # draw the current frame (automagically determined)
#core.wait(5.0)


#create some stimuli
#grating = visual.GratingStim(win=mywin, mask="circle", size=3, pos=[-4,0], sf=3)
#fixation = visual.GratingStim(win=mywin, size=0.5, pos=[0,0], sf=0, rgb=-1)


#core.wait(20.0)


#draw the stimuli and update the window
#grating.draw()
#fixation.draw()
#mywin.update()


#pause, so you get a chance to see it!
#core.wait(5.0)

