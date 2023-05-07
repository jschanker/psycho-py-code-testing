from enum import Enum
from psychopy import sound, visual, core, event, constants  # import some libraries from PsychoPy
from time import time, sleep
import pandas as pd
from random import randint
# from functools import partial
from psychopy import gui
import os

def getTraining():
  df = pd.read_excel('TRAINING_PHASE.xlsx', sheet_name=0)
  row0 = df.iloc[0].tolist()
  colName = df.columns
  col0 = df.iloc[:,0].tolist()
  #print(df.iloc[1].tolist())
  #print("COL0", col0)
  COLS_IN_TRIAL = row0.index("Audio") - row0.index("Accurate answer") + 1
  accurateAnswerRowIndex = col0.index("Accurate answer")
  NUM_OF_TRAINING_TRIALS = len(col0) - accurateAnswerRowIndex - 1
  trainingRows = df.iloc[accurateAnswerRowIndex + 1 : accurateAnswerRowIndex + 1 + NUM_OF_TRAINING_TRIALS,
  0 : COLS_IN_TRIAL]
  # print("HIGHLIGHTED", findIndex(trainingRows.values.tolist()[0], lambda x: x)
  #print("ROWS", COLS_IN_EXP, NUM_OF_LISTS_X, NUM_OF_LISTS_Y, ROWS_IN_EXP, experimentRowNum, experimentColNum)
  #print("SLICE", experimentRowNum * (COLS_IN_EXP), (experimentRowNum + 1) * (COLS_IN_EXP), 
  #experimentColNum * ROWS_IN_EXP , (experimentColNum + 1) * ROWS_IN_EXP + 1)
  print("TRAINING ROWS", COLS_IN_TRIAL, accurateAnswerRowIndex, NUM_OF_TRAINING_TRIALS, trainingRows.values.tolist())
  trial = [
    [
     [pict[-1].lower() for pict in row[1:COLS_IN_TRIAL-1]].index(row[0].split()[2].lower()), 
     ["PICTURES FOR VISUAL STIMULI/" + img + ".jpeg" for img in row[1:COLS_IN_TRIAL-1]], 
     row[COLS_IN_TRIAL-1]] 
     for row in trainingRows.values.tolist()
  ]
  print(NUM_OF_TRAINING_TRIALS, "TRIALS In training data", trial)
  print("\n")
  return trial
  
def getNumberOfListsInExperiment():
  df = pd.read_excel('EXPERIMENTAL_PHASE.xlsx', sheet_name=0)
  row0 = df.iloc[0].tolist()
  colName = df.columns
  col0 = df.iloc[:,0].tolist()
  #print(df.iloc[1].tolist())
  #print("COL0", col0)
  COLS_IN_EXP = row0.index("Audio") - row0.index("Accurate answer") + 1
  NUM_OF_LISTS_X = len(row0)/COLS_IN_EXP
  accurateAnswerRowIndex = col0.index("Accurate answer")
  ROWS_IN_EXP = col0.index("Accurate answer", accurateAnswerRowIndex + 1) - accurateAnswerRowIndex - 2
  NUM_OF_LISTS_Y = (len(col0) + 1)/(ROWS_IN_EXP + 2)
  NUM_OF_LISTS = int(NUM_OF_LISTS_X * NUM_OF_LISTS_Y)
  return NUM_OF_LISTS

def getExperiment(i=None):
  df = pd.read_excel('EXPERIMENTAL_PHASE.xlsx', sheet_name=0)
  row0 = df.iloc[0].tolist()
  colName = df.columns
  col0 = df.iloc[:,0].tolist()
  #print(df.iloc[1].tolist())
  #print("COL0", col0)
  COLS_IN_EXP = row0.index("Audio") - row0.index("Accurate answer") + 1
  NUM_OF_LISTS_X = int(len(row0)/COLS_IN_EXP)
  accurateAnswerRowIndex = col0.index("Accurate answer")
  ROWS_IN_EXP = col0.index("Accurate answer", accurateAnswerRowIndex + 1) - accurateAnswerRowIndex - 2
  NUM_OF_LISTS_Y = int((len(col0) + 1)/(ROWS_IN_EXP + 2))
  NUM_OF_LISTS = NUM_OF_LISTS_X * NUM_OF_LISTS_Y
  if i is None or i == "Random":
    experimentRowNum = randint(0, NUM_OF_LISTS_Y - 1)
    experimentColNum = randint(0, NUM_OF_LISTS_X - 1)
  else:
    experimentRowNum = (i - 1) // NUM_OF_LISTS_X
    experimentColNum = int((i - 1) % NUM_OF_LISTS_X)
  expRows = df.iloc[experimentRowNum * (ROWS_IN_EXP + 2) + 1 : experimentRowNum * (ROWS_IN_EXP + 2) + 1 + ROWS_IN_EXP,
  experimentColNum * (COLS_IN_EXP) : (experimentColNum + 1) * (COLS_IN_EXP)]
  #print("ROWS", COLS_IN_EXP, NUM_OF_LISTS_X, NUM_OF_LISTS_Y, ROWS_IN_EXP, experimentRowNum, experimentColNum)
  #print("SLICE", experimentRowNum * (COLS_IN_EXP), (experimentRowNum + 1) * (COLS_IN_EXP), 
  #experimentColNum * ROWS_IN_EXP , (experimentColNum + 1) * ROWS_IN_EXP + 1)
  exp = [
    [
     [pict[-1].lower() for pict in row[1:COLS_IN_EXP-1]].index(row[0].split()[1].lower()), 
     ["PICTURES FOR VISUAL STIMULI/" + img + ".jpeg" for img in row[1:COLS_IN_EXP-1]],
     "wav_recordings/RECEPTIVE CUE " + str(randint(1, 2)) + row[COLS_IN_EXP-1][0].lower() + ".wav"
    ]
    for row in expRows.values.tolist()
  ]
  print("EXPERIMENT ROW", experimentRowNum, "COL", experimentColNum, 
  "chosen from", NUM_OF_LISTS_Y, "rows and", NUM_OF_LISTS_X, "columns:\n", exp)
  print("\n")
  return exp

def findOneIndex(arr, f):
  for i in range(len(arr)):
    if f(arr[i]):
      return i

  return -1
  
def addImages(win, filePaths, vPadding=10, hPadding=10, scaleToFit=True):
  fitNum = len(filePaths)
  availableX = (win.size[0] - (fitNum + 1) * hPadding)/fitNum
  availableY = (win.size[1] - 2 * vPadding)
  imgs = [visual.ImageStim(win, filePath, units="pix", anchor="left") for filePath in filePaths]
  #imgSizeRatio = min(*[min(availableX/img.size[0], availableY/img.size[1]) for img in imgs])
  #if (not scaleToFit): imgSizeRatio = min(imgSizeRatio, 1)
  
  for index in range(len(imgs)):
    img = imgs[index]
    # if fp != '': # actual image, not used for placeholder
    #img.size = [imgSizeRatio * img.size[0], imgSizeRatio * img.size[1]]
    img.size = [availableX, availableX/img.size[0]*img.size[1]]
    img.pos[0] = (index + 1) * hPadding + index * img.size[0] - win.size[0]/2
    # img.pos[0] = -1
    #print("x", img.pos[0])
    
  def initImgs():
    [img.draw() for img in imgs]
    win.flip()
    return imgs
  
  return initImgs
  
def addSound(win, soundPath):
  snd = sound.Sound(soundPath)
  
  def initSound():
    # win.flip()
    # nextFlip = win.getFutureFlipTime(clock='ptb')
    # sound.play(when=nextFlip)
    snd.play()
    return snd

  return initSound
  
def addImagesWithSound(win, imageFilePaths, soundPath, delay=0, waitUntilSoundComplete=True, vPadding=10, hPadding=10, scaleToFit=True):
  initSound = addSound(win, soundPath)
  initImgs = addImages(win, imageFilePaths, vPadding, hPadding, scaleToFit)
  
  def initImagesWithSound():
    imgs = initImgs()
    sleep(delay)
    snd = initSound()
    while waitUntilSoundComplete and not soundIsFinished(snd):
      pass
    return [imgs, snd]
    
  return initImagesWithSound
    

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
    if type(stimuli[0]) is list:
      stimuli = stimuli[0] # hack to deal with [image, sound]
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
  if type(arg) is list:
    [x.stop() if hasattr(x, 'stop') else "" for x in arg]
  else:
    arg.stop()
    
def isImage(img):
  return hasattr(img, size) # look up class type to use instanceof instead
    
def getTrialSoundPath(index, isCue=False):
  answers = 'abcdefghij' # up to 10 letters
  suffix = 'Cue' if isCue else 'Feedback'
  return 'wav_recordings/T' + str(index + 1) + answers[index] + ' ' + suffix + '.wav'

def respondWithFeedback(index):
  def respond(stimuli):
    #print("STIMULI", stimuli)
    if type(stimuli[0]) is list:
      stimuli = stimuli[0] # hack to deal with [image, sound],
                           # need to fix this if images are not in 0th position
    selectedIndex = findOneIndex(stimuli, lambda stim: m.isPressedIn(stim))
    if selectedIndex == index:
      snd = sound.Sound(getTrialSoundPath(index))
      snd.play()
      while not soundIsFinished(snd):
        pass
    else:
      print("Wrong answer selected") # need incorrect feedback
    
  return respond
  
def calculateCorrect(correctArr, index):
  def addCorrect(stimuli):
    if type(stimuli[0]) is list:
      stimuli = stimuli[0] # hack to deal with [image, sound],
                           # need to fix this if images are not in 0th position
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
  
# Start training
mywin = visual.Window([700,700], monitor="testMonitor", units="pix")
training = getTraining()
numOfLists = getNumberOfListsInExperiment()
myDlg = gui.Dlg(title="Polish receptive skills experiment")
myDlg.addText('Subject info')
myDlg.addField('Participant number:')
myDlg.addText('List info')
myDlg.addField('List:', choices=["Random"] + [i for i in range(1, numOfLists + 1)])
[participantNum, listNum] = myDlg.show()  # show dialog and wait for OK or Cancel
if myDlg.OK:  # or if ok_data is not None
  print("Participant Number:", participantNum, "\nList Number:", listNum)
else:
  print('Experiment cancelled')
  core.quit()

instructions = addSound(mywin, "Toreador-clipped.wav") # need instructions
runTrial(instructions, doNothing, some([pressedEnter, soundIsFinished]), stopSound)
smileWithSound = addImagesWithSound(mywin, ['smile.png'], "Toreador-clipped.wav", waitUntilSoundComplete=False)
runTrial(smileWithSound, doNothing, some([pressedEnter]), stopSound)
#runTrial(doNothing, doNothing, some([pressedEnter, timeElapsed(1)])) # pause for 1 second
# instructions = addSound(mywin, "Toreador-clipped.wav")

m = event.Mouse(win=mywin)
for [ans, imageArr, snd] in training:
  images = addImagesWithSound(mywin, imageArr, getTrialSoundPath(ans, isCue=True), delay=1 if ans==1 else 0)
  runTrial(images, doNothing, some([pressedEnter, pressedIn(m), timeElapsed(5) if ans==2 else lambda x: False]), respondWithFeedback(ans))
  sleep(0.25) # delay quarter of a second to make sure long click isn't applied to next trial
  #if(ans == 2):
    # hack - add previous images just to get background color to change, do in loop to have access to images
    # mywin.setColor([0, 0, 1], colorSpace='rgb')
    # runTrial(images, doNothing, timeElapsed(0))
    # mywin.flip()

mywin.setColor([0, 0, 1], colorSpace='rgb')
smile = addImages(mywin, ['smile.png'])
mywin.flip()
# hack - draw image of size 0 to force background color to change
# grating = visual.GratingStim(win=mywin, mask="circle", size=14, pos=[0,0], sf=3)
# hack draw smile for 0 to force background color change
runTrial(smile, doNothing, timeElapsed(0))
mywin.flip()
core.wait(3.0)
# grating.draw()
# mywin.flip()
# core.wait(4.0)
# mywin.flip()

# Start experiment
exp = getExperiment(listNum)
#print("POS", mywin.pos)
#mywin.pos = (0, mywin.pos[1])
#print("POS", mywin.pos)
correctArr = []
times = []
for [ans, imageArr, snd] in exp:
  # images = addImages(mywin, imageArr)
  images = addImagesWithSound(mywin, imageArr, snd, delay=0, waitUntilSoundComplete=False) # sounds are all wrong
  runTrial(images, doNothing, some([pressedEnter, pressedIn(m)]), calculateCorrect(correctArr, index=ans), times)
  sleep(0.25) # delay quarter of a second to make sure long click isn't applied to next trial
  

#smile = addImages(mywin, ['smile.png', 'smile.png', 'smile.png'])
# instructions = addSound(mywin, "Toreador-clipped.wav")
#instructions = addSound(mywin, "recordings/D1-DIMM.mp3")
# runTrial(instructions, doNothing, some([soundIsFinished, pressedEnter]), stopSound)
#runTrial(smile, doNothing, some([pressedEnter, pressedIn(m)]), calculateCorrect(correctArr, index=1), times)
print("Results", correctArr, times)
# runTrial(smile, doNothing, timeElapsed(6))
# runTrial(smile, doNothing, pressedEnter)
includeHeadings = "polish-exp-results.csv" not in os.listdir("./")
with open('polish-exp-results.csv', 'a') as f:
  if includeHeadings:
    #f.write(",".join
    f.write("Participant Number,List Number," + ",".join(["Question " + str(i + 1) + " correct, Time" for i in range(len(correctArr))]))
  f.write("\n" + str(participantNum) + "," + str(listNum) + "," + ",".join([str(correctArr[i]) + "," + str(times[i]) for i in range(len(correctArr))]))

# clean up and exit
mywin.close()
core.quit()
