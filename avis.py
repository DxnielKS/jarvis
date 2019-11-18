import pygame, random, sys, smtplib, webbrowser, os, time, pickle
from datetime import datetime
import speech_recognition as sr
from pygame.locals import *
from gtts import gTTS
pygame.init() # initialising the pygame module
clock = pygame.time.Clock()
FPS = 60 # frames per second
WINDOWX,WINDOWY= 300,150 # these are the dimensions for the Avis window
infoObject = pygame.display.Info()
RESOLUTION =(infoObject.current_w,infoObject.current_h) # Resolution of the screen
startx = RESOLUTION[0]-WINDOWX # The width of the entire GUI
starty = 0
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (startx,starty)
DISPLAY = pygame.display.set_mode((WINDOWX,WINDOWY))
pygame.display.set_caption("Avis")
#button1 = pygame.image.load("button1.png")
#button2 = pygame.image.load("button2.png")
icon = pygame.image.load("logo.png")
pygame.display.set_icon(icon)
BLACK = (0,0,0) # colours
WHITE = (255,255,255)
GREY = (192,192,192)
DARKGREY= (169,169,169)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
with open("avisConfig.txt","r+") as avisConfig: # read in all user's details and remove enter "\n"
    username = avisConfig.readline().strip("\n")
    password = avisConfig.readline().strip("\n")
    nickname = avisConfig.readline().strip("\n")
with open("functionWords","rb+") as functionFile:
  functionWords = pickle.load(functionFile)
with open("todo","rb+") as todoFile:
    todoList = pickle.load(todoFile)
DISPLAY.fill(WHITE)
n = 1
def wipe(): # when conversation goes beneath screen
    global n
    DISPLAY.fill(WHITE)
    n = n + 1
class chatbox: # object for chatboxes
    def __init__(self,text):
        self.text = text
    def draw(self,position):
        pygame.font.init()
        position = position % 4
        if position == 0:
            position = 1
            wipe()
        if len(str(self.text)) > 50:
            font = pygame.font.SysFont('Courier New Bold.ttf', 10)
        else:
            font = pygame.font.SysFont('Courier New Bold.ttf', 14)
        mytext = font.render(str(self.text), True, DARKGREY)
        if position == 1:
            pygame.draw.rect(DISPLAY,DARKGREY,(10,10,280,30),1)
            DISPLAY.blit(mytext,(15,17))
        elif position == 2:
            pygame.draw.rect(DISPLAY,DARKGREY,(10,45,280,30),1)
            DISPLAY.blit(mytext,(15,52))
        elif position == 3:
            pygame.draw.rect(DISPLAY,DARKGREY,(10,80,280,30),1)
            DISPLAY.blit(mytext,(15,87))
        pygame.display.flip()
        pygame.display.update()
box1 = (10,10) # coordinates for boxes
box2 = (10,45)
box3 = (10,80)
row1 = [box1] # list to graphically show boxes
row2 = [box2]
row3 = [box3]
def decipher(text): # deciphers the intent behind speech from user.
    thresholds = [] # a list where all the thresholds will be
    print("Deciphering: %s" % text)
    words = text.lower().split()
    threshold = 0.74
    if "change" in words and "nickname" in words:
        return "changenick"
    for function in functionWords:
        x = 0 # words in compared word list
        y = 0 # total words
        for word in words:
            if word in function:
                x = x + 1
            y = y + 1
        if x/y >= threshold: # if the percentage similarity is above a certain threshold of accuracy
            for word in words: # for each word in the set of said words
                if word not in function: # adds words not already in data set into function
                    function.append(word)
                    with open("functionWords","wb+") as functionFile:
                        pickle.dump(functionWords, functionFile)
            return function[0]
        else: # if the threshold is not met
            line = [function[0],x/y]
            thresholds.append(line)
    print(thresholds)
    for i in range(0,len(thresholds)):
        if i == 0:
            global toRun
            biggest = thresholds[0][1] # the first one is initially the biggest
            toRun = thresholds[0][0]
        elif thresholds[i][1] > biggest:
            pos = i
            biggest = thresholds [i][1]
            toRun = thresholds[i][0]
    if biggest == 0:
        return None
    textToSpeech("Did you mean %s?" % toRun)
    response = speechToText()
    if "yes" in response.lower() or "yeah" in response.lower() or "yep" in response.lower():
        for function in functionWords:
            if function[0] == toRun:
                for word in words:
                    if word not in function:
                        function.append(word)
                with open("functionWords","wb+") as functionFile:
                    pickle.dump(functionWords, functionFile)
        return toRun
    return None
def textToSpeech(text): # converts text into speech
    global n
    print ("Avis said: %s" % text)
    chatbox1 = chatbox(text)
    chatbox1.draw(n)
    n = n + 1
    pygame.display.update()
    try:
        tts = gTTS(text=str(text), lang = "en")
        tts.save("speech.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load("speech.mp3")
        pygame.mixer.music.play()
        time.sleep(1.5)
    except:
        print("[!] Not able to connect to text to speech services!")
def speechToText(): # converts speech to text
    global n
    r = sr.Recognizer()
    heard = False
    while heard == False: # in order to get an input from the user.
        with sr.Microphone() as source:
            r.pause_thresh = 1.5
            r.adjust_for_ambient_noise(source, duration = 1)
            pygame.mixer.music.load("siri.mp3")
            pygame.mixer.music.play()
            print("Speak..")
            audio = r.listen(source)
        try:
            pygame.mixer.music.load("finished.mp3")
            pygame.mixer.music.play()
            text = r.recognize_google(audio) # changes audio object into string
            print ("You said: %s" % text)
            heard = True
          # loop back to continue to listen for speech
        except sr.UnknownValueError:
            textToSpeech("I didn't quite get that!")
    chatbox2 = chatbox(text)
    chatbox2.draw(n)
    n = n + 1
    pygame.display.update()
    return text
def email(): # sends an email to a contact in a contact file
    try:
        server = smtplib.SMTP("smtp.gmail.com:587")
        server.ehlo()
        server.starttls()
        server.login(username,password)
    except:
        textToSpeech("[!] Something went wrong!")
        return False
    textToSpeech("What is the name of the recipient?")
    name = speechToText()
    found = False
    with open("avisContacts.txt","r+") as contacts:
        lines = contacts.readlines()
        for line in lines:
            contact = line.split(", ")
            if contact[0] == name.lower():
                found = True
                emailTo = contact[1]
                textToSpeech("Ok! You would like to send an email to %s" % emailTo.strip("\n"))
                time.sleep(6)
                break
    if found == False: # adds new contact
        textToSpeech("I don't know who %s is!" % name)
        email = input("What is their email? ")
        with open("avisContacts.txt","a+") as contacts:
            contact = name.lower()+", "+email+"\n"
            contacts.write(contact)
            textToSpeech("Contact added!")
    elif found == True: # sends email
        textToSpeech("What would you like to email them?")
        text = speechToText()
        textToSpeech("What would you like the subject line to be?")
        subject = speechToText()
        message = "Subject:"+subject+"\n\n"+text
        server.sendmail(username,emailTo,message)
        textToSpeech("Email sent!")
    pygame.display.update()
def todo(): # makes and edits a todo list
    textToSpeech("You have %s events in your to-do list! These events are.." % len(todoList))
    for event in todoList: # each event in the list
        textToSpeech(event)
    textToSpeech("Would you like to add or remove to your to-do list?")
    response = speechToText()
    if "add" in response.lower(): # if the user would like to add to the todo list.
        textToSpeech("What event would you like to add?")
        event = speechToText()
        todoList.append(event)
        with open("todo","wb+") as todoFile:
            pickle.dump(todoList,todoFile)
        textToSpeech("Event added!")
    elif "remove" in response.lower(): # if the user would like to remove from the list
        textToSpeech("What number event would you like to remove?")
        index = speechToText()
        todoList.pop((int(index)-1))
        with open("todo","wb+") as todoFile:
            pickle.dump(todoList,todoFile)
        textToSpeech("Event removed!")
    else:
        textToSpeech("Ok!")
    pygame.display.update()
def web(): # web questions
    textToSpeech("What would you like to search?")
    url = speechToText()
    url = url.replace(" ","+")
    template = "https://www.google.com/search?q="
    search = template+url.lower()
    webbrowser.open(search)
    textToSpeech("Query searched!")
    pygame.display.update()
def gettime():
    now = datetime.now() # gets time
    current_time = now.strftime("%H:%M:%S") # in format HH:MM:SS
    textToSpeech(("The time is "+current_time))
def currency(): # converts one currency into another
    GBPToHome={"EUR":0.89,
            "USD":0.76,
            "JPY":0.0067,
            "RMB":0.12,
            "NGN":0.0021,
            "HRK":0.12} # currency dictionary
    currencyList = ["1 European Euro EUR","2 American Dollar USD","3 Japanese Yen JPY","4 Chinese Yuan RMB","5 Nigerian Naira NGN","6 Croatian Kuna HRK"]
    textToSpeech("Do you want to convert GBP into another currency?")
    response = speechToText()
    if "yes" in response or "yeah" in response or "yep" in response: # GBP to homeland
        textToSpeech("How much would you like to convert?")
        amount = int(speechToText())
        textToSpeech("What number conversion would you like to carry out?")
        for country in currencyList:
            textToSpeech(country)
        currencyNo = speechToText()
        for country in currencyList:
            if currencyNo in country:
                newAmount = amount * GBPToHome[(country.split()[3])]
                textToSpeech(newAmount)
    else: # homeland to GBP
        textToSpeech("How much would you like to convert?")
        amount = int(speechToText())
        textToSpeech("What number conversion would you like to carry out?")
        for country in currencyList:
            textToSpeech(country)
        currencyNo = speechToText()
        for country in currencyList:
            if currencyNo in country:
                newAmount = amount / int(GBPToHome[country.split()[2]])
                textToSpeech(newAmount)
def changenick(): # changes the nickname of the user
    textToSpeech("Change your nickname to?")
    newNick = speechToText()
    global nickname
    nickname = newNick
    with open("avisConfig.txt","w") as avisConfig: # read in all user's details and remove enter "\n"
        avisConfig.write((username+"\n"+password+"\n"+nickname))
    textToSpeech("Nickname changed!")
def main(): # main program
    greetings = ["Hello!"+" "+nickname,"Hey there!"+" "+nickname,"What's up?"+" "+nickname,"What can I do for you?"+" "+nickname]
    greeting = random.choice(greetings)
    textToSpeech(greeting) # say a random greeting
    command = speechToText()
    function = decipher(command)
    if function == None:
        textToSpeech("I don't know what you want!")
        return;
    eval((function+"()")) # run the name of the function e.g. email+() = email()
while True: # update loop
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    pygame.draw.circle(DISPLAY,DARKGREY,(150,135),10) # button
    if mouse[0] > 140 and mouse[0] < 160 and mouse[1] < 145 and mouse[1] > 125:
            pygame.draw.circle(DISPLAY,GREY,(150,135),10) # filled in circle when hovering
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit() # close window
        if mouse[0] > 140 and mouse[0] < 160 and mouse[1] < 145 and mouse[1] > 125 and click[0] == 1:
            main()
    pygame.display.update()
    clock.tick(FPS)
