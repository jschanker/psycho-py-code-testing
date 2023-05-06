from enum import Enum
from psychopy import sound, visual, core, event, constants  # import some libraries from PsychoPy
from time import time, sleep
import pandas as pd
from random import randint
from math import ceil
from pathlib import Path
import os
# from functools import partial

def findOneIndex(arr, f, start=0):
  for i in range(start, len(arr)):
    if f(arr[i]):
      return i

  return -1

def getTraining():
  df = pd.read_excel('Lists_counterbalanced_with_answers.xlsx', sheet_name=0)
  row0 = df.iloc[0].tolist()
  colName = df.columns
  col0 = df.iloc[:,0].tolist()
  #print(df.iloc[1].tolist())
  #print("COL0", col0)
  COLS_IN_TRIAL = 3
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
  
def getSoundFilePath(s):
  #lowercaseFilename = "wav_recordings_diminutive/" + s.lower() + " dim.wav"
  #lowercaseFile = Path(lowercaseFilename)
  #return lowercaseFilename if lowercaseFile.is_file() else upper(lowerCaseFilename)
  lowercaseFilename = s.lower() + " dim.wav"
  dirName = "wav_recordings_diminutive"
  return dirName + "/" + (lowercaseFilename if lowercaseFilename in os.listdir(dirName) else lowercaseFilename.upper())

def getImageFilePath(s):
  #lowercaseFilename = "wav_recordings_diminutive/" + s.lower() + " dim.wav"
  #lowercaseFile = Path(lowercaseFilename)
  #return lowercaseFilename if lowercaseFile.is_file() else upper(lowerCaseFilename)
  fileName = (s.lower() + " dim" if getSoundFilePath(s).find(s.lower()) != -1 else s.upper() + " DIM") + ".JPEG"
  dirName = "PICTURES FOR VISUAL STIMULI DIMINUTIVE"
  return dirName + "/" + fileName

#print("SOUND", getSoundfile("D1"))

def getExperiment():
  df = pd.read_excel('Lists_counterbalanced_with_answers.xlsx', sheet_name=0)
  row1 = df.iloc[1].tolist()
  colName = df.columns
  col0 = df.iloc[:,0].tolist()
  #print(df.iloc[1].tolist())
  #print("COL0", col0)
  #COLS_IN_EXP = 3
  COLS_IN_EXP = 4
  #NUM_OF_LISTS_X = ceil((len(row1) + 2)/(COLS_IN_EXP + 2))
  NUM_OF_LISTS_X = ceil((len(row1) + 1)/(COLS_IN_EXP + 1))
  # print("C0", col0)
  startRowIndex = findOneIndex(col0, lambda x: isinstance(x, str) and len(x) > 0)
  endRowIndex = findOneIndex(col0, lambda x: not isinstance(x, str) or isinstance(x, str) and len(x) == 0, startRowIndex)
  ROWS_IN_EXP = endRowIndex - startRowIndex
  NUM_OF_LISTS_Y = len(col0)/(ROWS_IN_EXP + 1)
  # print("Y", NUM_OF_LISTS_Y)
  NUM_OF_LISTS = NUM_OF_LISTS_X * NUM_OF_LISTS_Y
  experimentRowNum = randint(0, NUM_OF_LISTS_Y - 1)
  experimentColNum = randint(0, NUM_OF_LISTS_X - 1)
  #expRows = df.iloc[experimentRowNum * (ROWS_IN_EXP + 1) + startRowIndex : experimentRowNum * (ROWS_IN_EXP + 1) + startRowIndex + ROWS_IN_EXP,
  #experimentColNum * (COLS_IN_EXP + 2) : (experimentColNum + 1) * (COLS_IN_EXP + 2) - 2]
  expRows = df.iloc[experimentRowNum * (ROWS_IN_EXP + 1) + startRowIndex : experimentRowNum * (ROWS_IN_EXP + 1) + startRowIndex + ROWS_IN_EXP,
  experimentColNum * (COLS_IN_EXP + 1) : (experimentColNum + 1) * (COLS_IN_EXP + 1) - 1]
  print("EXP", experimentRowNum, experimentColNum, expRows.values.tolist())
  #print("ROWS", COLS_IN_EXP, NUM_OF_LISTS_X, NUM_OF_LISTS_Y, ROWS_IN_EXP, experimentRowNum, experimentColNum)
  #print("SLICE", experimentRowNum * (COLS_IN_EXP), (experimentRowNum + 1) * (COLS_IN_EXP), 
  #experimentColNum * ROWS_IN_EXP , (experimentColNum + 1) * ROWS_IN_EXP + 1)
  # soundFilePaths = [getSoundFilePath(row[1]) for row in expRows.values.tolist()] 
  exp = [
    [
     int(row[COLS_IN_EXP-1]),
     1 if getSoundFilePath(row[1]).find(row[1]) == -1 else 0,
     [getImageFilePath(item) for item in row[1:COLS_IN_EXP-1]],
     [3 if item.find("D") == 0 else 1 for item in row[1:COLS_IN_EXP-1]],
     getSoundFilePath(row[1])
     #"wav_recordings/RECEPTIVE CUE " + str(randint(1, 2)) + row[COLS_IN_EXP-1][0].lower() + ".wav"
    ]
    for row in expRows.values.tolist()
  ]
  print("EXPERIMENT ROW", experimentRowNum, "COL", experimentColNum, 
  "chosen from", NUM_OF_LISTS_Y, "rows and", NUM_OF_LISTS_X, "columns:\n", exp)
  print("\n")
  return exp
  
#getExperiment()
#core.quit()
  
def addImages(win, filePaths, scaleArr, vPadding=10, hPadding=10, scaleToFit=True):
  # fitNum = len(filePaths)
  # fitNum = sum([3 if filePath.find("D") == -1 else 1 for filePath in filePaths]) # images 3 * space if big
  fitNum = sum(scaleArr)
  availableX = (win.size[0] - (len(filePaths) + 1) * hPadding)/fitNum
  availableY = (win.size[1] - 2 * vPadding)
  imgs = [visual.ImageStim(win, filePath, units="pix", anchor="left") for filePath in filePaths]
  #imgSizeRatio = min(*[min(availableX/img.size[0], availableY/img.size[1]) for img in imgs])
  #if (not scaleToFit): imgSizeRatio = min(imgSizeRatio, 1)
  
  for index in range(len(imgs)):
    img = imgs[index]
    scale = scaleArr[index]
    # scale = 3 if filePaths[index].find("D") == -1 else 1
    # if fp != '': # actual image, not used for placeholder
    #img.size = [imgSizeRatio * img.size[0], imgSizeRatio * img.size[1]]
    img.size = [availableX * scale, availableX * scale/img.size[0]*img.size[1]]
    img.pos[0] = (index + 1) * hPadding + sum(scaleArr[0:index]) * availableX - win.size[0]/2
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
  
def addImagesWithSound(win, imageFilePaths, scaleArr, soundPath, delay=0, waitUntilSoundComplete=True, vPadding=10, hPadding=10, scaleToFit=True):
  initSound = addSound(win, soundPath)
  initImgs = addImages(win, imageFilePaths, scaleArr, vPadding, hPadding, scaleToFit)
  
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
  
mywin = visual.Window([700,700], monitor="testMonitor", units="pix")
m = event.Mouse(win=mywin)
# Start experiment
exp = getExperiment()
#print("POS", mywin.pos)
#mywin.pos = (0, mywin.pos[1])
#print("POS", mywin.pos)
correctArr = []
times = []
for [ans, ans, imageArr, scaleArr, snd] in exp:
  # images = addImages(mywin, imageArr)
  images = addImagesWithSound(mywin, imageArr, scaleArr, snd, delay=0, waitUntilSoundComplete=False) # sounds are all wrong
  runTrial(images, doNothing, some([pressedEnter, pressedIn(m)]), calculateCorrect(correctArr, index=ans), times)
  sleep(0.25) # delay quarter of a second to make sure long click isn't applied to next trial
  
print("Results", correctArr, times)  

core.quit()
