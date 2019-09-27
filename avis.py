import pygame
from pygame.locals import *
import sys
import smtplib
import webbrowser
import os
import time
from gtts import gTTS
import speech_recognition as sr

###################################################

pygame.init()
FPS = 60 # The frames per second
WINDOWX,WINDOWY= 300,150 # These are the dimensions for the Avis window
WINDOWBORDERWIDTHX,WINDOWBORDERWIDTHY= 7,23 # Dimensions for the border of the window border

###################################################

BLACK = (0,0,0)
WHITE = (255,255,255)
RESOLUTION =(2560,1600) # Resolution of the screen
"""w,h=pygame.display.get_window_size()"""
x = RESOLUTION[0]-WINDOWX-WINDOWBORDERWIDTHX
y = WINDOWBORDERWIDTHY

###################################################

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
DISPLAY = pygame.display.set_mode((WINDOWX,WINDOWY))
pygame.display.set_caption("Avis")

###################################################

def talkToMe(audio):
  print (audio)
  tts = gTTS(text=audio, lang = "en")
  tts.save("audio.mp3")
  mixer.init()
  mixer.music.load("audio.mp3")
  mixer.music.play()
# listens for command

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

while True:
        pygame.draw.circle(DISPLAY,WHITE,(150,135),10,3)
        for event in pygame.event.get():
                if event.type == QUIT:  
                        pygame.quit()
                        sys.exit()
        pygame.display.flip()
