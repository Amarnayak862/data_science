import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import smtplib
import webbrowser as wb
import os
import pyautogui
import psutil
import pyjokes


engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
newVoiceRate = 190
engine.setProperty('rate', newVoiceRate)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time():
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    speak("The current time is")
    speak(Time)

def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    day = int(datetime.datetime.now().day)
    speak("Today's date is")
    speak(day)
    speak(month)
    speak(year)

def day():
    day = datetime.datetime.today().weekday() + 1
    day_dict = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}

    if day in day_dict.keys():
        day_of_the_week = day_dict[day]
        print(day_of_the_week)
        speak("The day is " + day_of_the_week)

def wishme():
    speak("Welcome back Boss!!")
    hour = datetime.datetime.now().hour

    if hour >= 6 and hour < 12:
        speak("Good Morning")
    elif hour >=12 and hour < 18:
        speak("Good Afternoon")
    elif hour >= 18 and hour <= 24:
        speak("Good evening")
    else:
        speak("Good Night") 

    speak("My name is Darvis!! How may I Help You?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language =  "en-in")
        print(query)
    except Exception as e:
        print(e)
        speak("Can you repeat please...")

        return "None"

    return query

def sendmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("amarnayak8763@gmail.com", "Amar@8763")
    server.sendmail("amarnayak8763@gmail.com", to, content)
    server.close()
def screenshot():
    img = pyautogui.screenshot()
    img.save("D:\ss.png")
def cpu():
    usage = str(psutil.cpu_percent())
    speak("CPU is at" + usage)
    
def jokes():
    speak(pyjokes.get_joke())

if __name__ == "__main__":

    wishme()

    while True:
        query = takeCommand().lower()
        print(query)

        if "time" in query:
            speak("current time is!!")
            time()

        elif "date" in query:
            date()

        elif "day" in query:
            day()

        elif "offline" in query:
            speak("I am taking your leave sir, please recall if you have any other work with me!! Thankyou.")
            quit()

        elif "wikipedia" in query:
            speak("Searching...")
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences = 2)
            speak(result)

        elif "send email" in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "amarnayak862@gmail.com"
                sendmail(to, content)
                speak("Email sent successfully")
            except Exception as e:
                speak(e)
                speak("Unable to send message")

        elif "search in chrome" in query:
            speak("What should i search?")
            chromepath = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s"
            search = takeCommand().lower()
            wb.get(chromepath).open_new_tab(search + ".com")

        elif "Logout" in query:
            os.system("Shutdown - l")

        elif "shutdown" in query:
            os.system("Shutdown /s /t 1")

        elif "restart" in query:
            os.system("Shutdown /r /t 1")

        elif "play songs" in query:
            songs_dir = "D:\Moosic"
            songs = os.listdir(songs_dir)
            os.startfile(os.path.join(songs_dir, songs[0]))
            speak("Enjoy")
            quit()

        elif "remember that" in query:
            speak("what should i remember")
            data = takeCommand()
            speak("you said me to remember " + data)
            remember = open("data.txt", "w")
            remember.write(data)
            remember.close()

        elif "do you know anything" in query:
            remember = open("data.txt", "r")
            speak("you said to remember that" + remember.read())

        elif "screenshot" in query:
            screenshot()
            speak("Done!")
            quit()

        elif "cpu" in query:
            cpu()
        elif "jokes" in query:
            jokes()