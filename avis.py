import pygame
import random
import sys
import smtplib
import webbrowser
import os
import time
import speech_recognition as sr
from pygame.locals import *
from gtts import gTTS

pygame.init() # initialising the pygame module
clock = pygame.time.Clock()
FPS = 60 # frames per second
reminderArray = []
todoArray = []
WINDOWX,WINDOWY= 300,150 # these are the dimensions for the Avis window
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
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (192,192,192)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
with open("avisConfig.txt","r+") as avisConfig:
    username = avisConfig.readline()
    password = avisConfig.readline()
    nickname = avisConfig.readline()
threshold = 0.5 # threshold for deciphering function

def textToSpeech(text): # converts text into speech
  print ("Avis said: %s " % text)
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
    return text
  # loop back to continue to listen for speech
  except sr.UnknownValueError:
    textToSpeech("I didn't quite get that!")
    speechToText()
def main(): # main program
    greetings = ("Hello!","Hey there!","What's up?","What can I do for you?")
    textToSpeech((random.choice(greetings)+" "+nickname+"!")) # say a random greeting
    request = speechToText()
    command = decipher(request)
def decipher(text): # finds meaning of users input
    emailWords = ["email","send","to","saying",""]
    todoWords = ["todo","add","this","need","to","do"]
    reminderWords = ["remind","me","minutes","minute"]
    wordDictionary = {"email":emailWords}
    words = text.split(" ")
    x = 0
    y = 0
    for function in wordDictionary:
        for word in words:
            if word in function:
                x = x + 1
            y = y + 1
        percentage = x/y
        if percentage >= threshhold: # if this exceeds the threshold
            return function
def email(): # sends an email to a contact in a contact file
    try:
        s = smtplib.SMTP(host="smtp.gmail.com")
        s.startssl()
        s.login(username,password)
    except:
        textToSpeech("Something went wrong!")
        return False
    textToSpeech("What is the name of the recipient?")
    name = speechToText()
    found = False
    with open("avisContacts.txt","r+") as contacts:
        for line in contacts.readlines():
            contact = line.split(", ")
            if contact[0].title() == name:
                found = True
                emailTo = contact[1]
                textToSpeech("Ok! You would like to send an email to %s" % emailTo)
    if found == False: # adds new contact
        textToSpeech("I don't know who %s is!" % name)
        email = input("What is their email? ")
        with open("avisContacts.txt","a+") as contacts:
            contact = name+", "+email+"/n"
            contacts.write(contact)
            textToSpeech("Contact added!")
    elif found == True: # sends email
        message = MIMEMultipart() # create draft email
        textToSpeech("What would you like to email them?")
        text = speechToText()
        textToSpeech("What would you like the subject line to be?")
        subject = speechToText()
        message["From"] = emailFrom
        message["To"] = MY_ADDRESS
        message["Subject"] = subject
        message.attach(MIMEText(text, "plain"))
        s.send_message(message)
def currency(): # converts one currency to another
    currencyDictionary={"EUR":1.12,
                "USD":1.32,
                "JPY":148.22,
                "RMB":8.68,
               "NGN":473.15,
                "HRK":8.39}
while True:
    DISPLAY.fill(WHITE)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit() # close window
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if mouse[0] > 140 and mouse[0] < 160 and mouse[1] < 145 and mouse[1] > 125:
        pygame.draw.circle(DISPLAY,GREY,(150,135),10) # filled in circle when hovering
        if click[0] == 1: # if user left clicks
            main()
    pygame.draw.circle(DISPLAY,GREY,(150,135),10,3) # button circle
    pygame.display.flip()
    pygame.display.update()
    clock.tick(FPS)
