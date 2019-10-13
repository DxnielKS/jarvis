###################IMPORTS##########################

import pygame
import sys
import smtplib
import webbrowser
import os
import time
import speech_recognition as sr
from pygame.locals import *
from gtts import gTTS

###################DISPLAY##########################

pygame.init() # initialising the pygame module
clock = pygame.time.Clock()
FPS = 60 # The frames per second
WINDOWX,WINDOWY= 300,150 # These are the dimensions for the Avis window
WINDOWBORDERWIDTHX,WINDOWBORDERWIDTHY= 7,0 # Dimensions for the border of the window border
RESOLUTION =(2560,1600) # Resolution of the screen
"""w,h=pygame.display.get_window_size()"""
x = RESOLUTION[0]-WINDOWX-WINDOWBORDERWIDTHX # The width of the entire GUI
y = WINDOWBORDERWIDTHY
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
DISPLAY = pygame.display.set_mode((WINDOWX,WINDOWY))
pygame.display.set_caption("Avis")
icon = pygame.image.load("logo.png")
pygame.display.set_icon(icon)

####################COLOURS#########################

BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (192,192,192)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

####################MAIN############################

def textToSpeech(text): # converts text into speech
  print (text)
  tts = gTTS(text=text, lang = "en")
  tts.save("speech.mp3")
  pygame.mixer.init()
  pygame.mixer.music.load("speech.mp3")
  pygame.mixer.music.play()
def speechToText(): # converts speech to text
  r = sr.Recognizer()
  with sr.Microphone() as source:
    r.pause_thresh = 1
    r.adjust_for_ambient_noise(source, duration = 1)
    audio = r.listen(source)
  try:
    text = r.recognize_google(audio)
    print ("You said: %s" % text)
  # loop back to continue to listen for speech
  except sr.UnknownValueError:
    print ("[!] I didn't quite get that!")
    speechToText()
  return text
while True: # main program loop
    DISPLAY.fill(WHITE)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit() # close window
    pygame.draw.circle(DISPLAY,GREY,(150,135),10,3) # button circle
    pygame.display.flip()
    pygame.display.update()
    clock.tick(FPS)
