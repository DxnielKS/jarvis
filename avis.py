###################IMPORTS##########################

import pygame, sys, smtplib, webbrowser, os, time, speech_recognition as sr
from pygame.locals import *
from gtts import gTTS

###################DISPLAY##########################

pygame.init() # initialising the pygame module
clock = pygame.time.Clock()
FPS = 60 # The frames per second
WINDOWX,WINDOWY= 300,150 # These are the dimensions for the Avis window
WINDOWBORDERWIDTHX,WINDOWBORDERWIDTHY= 7,23 # Dimensions for the border of the window border
RESOLUTION =(2560,1600) # Resolution of the screen
"""w,h=pygame.display.get_window_size()"""
x = RESOLUTION[0]-WINDOWX-WINDOWBORDERWIDTHX # The width of the entire GUI
y = WINDOWBORDERWIDTHY
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
DISPLAY = pygame.display.set_mode((WINDOWX,WINDOWY))
pygame.display.set_caption("Avis")

####################COLOURS#########################

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

####################MAIN############################

def talkToMe(audio):
  print (audio)
  tts = gTTS(text=audio, lang = "en")
  tts.save("audio.mp3")
  mixer.init()
  mixer.music.load("audio.mp3")
  mixer.music.play() # plays the audio file from
# text to speech module
def myCommand():
  r = sr.Recognizer()
  with sr.Microphone() as source:
    talkToMe("I am ready for your next command!")
    r.pause_thresh = 1
    r.adjust_for_ambient_noise(source, duration = 1)
    audio = r.listen(source)
  try:
    command = r.recognize_google(audio)
    print ("You said: %s" % command)
  # loop back to continue to listen for commands
  except sr.UnknownValueError:
    print ("[!] I didn't quite get that!")
    assistant(myCommand())
  return command
# takes the audio from the user as a command
def background():
  r = sr.Recognizer()
  with sr.Microphone() as source:
    talkToMe("I am ready for your next command!")
    r.pause_thresh = 1
    r.adjust_for_ambient_noise(source, duration = 1)
    audio = r.listen(source)
  try:
    text = r.recognize_google(audio)
  except:
    background()
  if "what's up" in text:
    myCommand()
# listens to user in the background
def decipher():
    None
# algorithm to decide what function to carry out
while True:
    DISPLAY.fill(WHITE)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit() # close window
    pygame.draw.circle(DISPLAY,WHITE,(150,135),10,3) # button circle
    pygame.display.flip()
    pygame.display.update()
    clock.tick(FPS)
# main program loop
