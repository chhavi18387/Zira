import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
from youtubesearchpython import VideosSearch
import re, requests, subprocess, urllib.parse , urllib.request
from bs4 import BeautifulSoup
import json
import time
import pprint
from newsapi.newsapi_client import NewsApiClient
from pandas.io.json import json_normalize
import pandas as pd
# import PyAudio
# microsoft speech api . windows api to use inbuilt voice in windows
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print voices, we will see there are two voices inbuilt in our computer
# we can install additional voices too
# print(voices)
# print the two voices 
# print(voices[0].id) # david 
# print(voices[1].id) # zira 
# we set which voice we wanna use. david or zira
# here we set to use zira voice 
#  we are setting 'voice' property of engine to zira
engine.setProperty('voice',voices[0].id)

def speak(audio):
	engine.say(audio)
	engine.runAndWait()

def wishMe():
	hour = int(datetime.datetime.now().hour)
	if hour >=0 and hour<12:
		speak("good morning! rise and shine habibi")
	elif hour >=12 and hour <18:
		speak("good afternoon!")
	else :
		speak("good evening you lovely cootie patootie !")

	speak("I'm Jarvis, a virtual friend at your assistance. Please tell how how may i help you?")

def takeCommand():
	'''
	takes microphone input from the user and return string output
	'''
	r=sr.Recognizer()
	with sr.Microphone() as source :
		'''
		initially it was showing a blinking output, i figured out that the problem occured due to
		background noise and that i need to adjust for ambient noise
		the problem could have been that energy_threshold value was initially
		set too high. this adjust_for_ambient_noise sets an apt threshloh automatically

		'''
		r.adjust_for_ambient_noise(source,duration=1)
		print("Listening .....")
		r.pause_threshold=5 
		audio = r.listen(source)
	try :
		print("Recognizing....")
		query = r.recognize_google(audio, language='en-in')
		print(f"Google thinks you said :{ query}\n" )
	except Exception as e :
		print(e)
		print("Say that again please...")
		speak("Say that again please ....")
		return "None"

	return query 

def sendEmail(to,content):
	server = smtplib.SMTP('smtp.gmail.com',587)
	server.ehlo()
	server.starttls()
	server.login('chhai15121512@gmail.com','@Geeta123')
	server.sendmail('chhai15121512@gmail.com',to,content)
	server.close()



def readNews():    

   # speak("Which country are you interested in?") 
   # country=takeCommand()
   # speak("""Which category are you interested in? \nHere are the categories to choose from:\nbusiness\nentertainment\ngeneral\nhealth\nscience\ntechnology""") 
   # category=takeCommand()  
   newsapi = NewsApiClient(api_key='3c7fed1469c84ab58e2259d781c49296')
   top_headlines =newsapi.get_top_headlines(category='general',language='en',country='in')     
   top_headlines=json_normalize(top_headlines['articles'])   
   newdf=top_headlines[["title","url"]]    
   dic=newdf.set_index('title')['url'].to_dict()
   listt = dic.keys()
   listt=list(listt)
   listt=listt[0:5]
   for i in listt:
   		speak(i)
   		time.sleep(2)

   


  
if __name__ == '__main__':
	# wishMe()
	while(1==1):
 		query=takeCommand().lower()

 		#logic for executing tasks based on query

 		if 'wikipedia' in query :
 			speak('Searching wikipedia....')
 			query = query.replace("wikipedia"," ")
 			results = wikipedia.summary(query, sentences=2)
 			speak("According to wikipedia")
 			speak(results)

 		elif 'open youtube' in query:
 			speak('opening youtube')
 			webbrowser.open("youtube.com")

 		elif 'open google' in query:
 			speak('opening google')
 			webbrowser.open("google.com")

 		elif 'open stackoverflow' in query:
 			speak('opening stackoverflow')
 			webbrowser.open("stackoverflow.com")

 		elif 'play music' in query :
 			music_dir = 'D:\\Music'
 			songs = os.listdir(music_dir)
 			print(songs)
 			os.startfile(os.path.join(music_dir, songs[1])) 

 		elif 'what is the time' in query :
 			time = datetime.datetime.now().strftime("%H:%M:%S")
 			speak(f"Hey pretty hooman! the time is {time}")

 		elif 'open discord' in query :
 			path = "C:\\Users\\chhavi munjal\\AppData\\Local\\Discord"
 			os.startfile(path)

 		elif 'email to mum' in query :
 			try :
 				speak("what should i say?")
 				content = takeCommand()
 				print(content)
 				to= "munjalkiran94@gmail.com"
 				sendEmail(to,content)
 				speak("email sent")

 			except Exception as e :
 				print(e)
 				speak("sorry i couldn't send email at the moment")


 		elif 'search on youtube' in query :
 			try :
 				# taking command and generating youtube link according to search query and opening it in webbrowser
 				speak("what should i search for ?")
 				searchInput = takeCommand()
 				query_string = urllib.parse.urlencode({"search_query":searchInput})
 				formatURL = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
 				# findall gives all the links 
 				search_results = re.findall(r"watch\?v=(\S{11})", formatURL.read().decode())
 				clip = requests.get("https://www.youtube.com/watch?v=" + "{}".format(search_results[0]))
 				clip2 = "https://www.youtube.com/watch?v=" + "{}".format(search_results[0])
 				print(clip2)
 				webbrowser.open(clip2)
 				inspect = BeautifulSoup(clip.content, "html.parser")
 				yt_title = inspect.find_all("meta", property="og:title")
 				for concatMusic1 in yt_title:
 					pass
 				print(concatMusic1['content'])
 				
 			except Exception as e :
 				print(e)
 				speak("sorry i couldn't play the video. Please try again!")


 		elif 'news' in query :
 			readNews()




 		if 'quit' in query :
 			exit()
 		
