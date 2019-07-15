from pygame import mixer
import smtplib
import webbrowser
import os
import time
from gtts import gTTS
import speech_recognition as sr

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

def assistant(command):
  print ("Command Received!")

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

while True: # Continuously running
  background()
