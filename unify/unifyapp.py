from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout  
from kivy.uix.carousel import Carousel

from os.path import dirname, join
from random import sample
from string import ascii_lowercase
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

from kivy.uix.button import Button
from kivy.uix.behaviors.touchripple import TouchRippleBehavior
from kivy.clock import Clock
import webbrowser

import requests
import json
import jwt
from datetime import datetime
import time

#This generates a json token for each request
now = datetime.now()
date_time_string = now.strftime("%Y-%m-%d %H:%M:%S")
date_time = date_time_string
date_order = '%Y-%m-%d %H:%M:%S'
iat = int(time.mktime(time.strptime(date_time, date_order))) #issued at
nbf = int(time.mktime(time.strptime(date_time, date_order))) - 1 #not before
exp = int(time.mktime(time.strptime(date_time, date_order))) + 20 #expires
signature = "secret"

json_token = jwt.encode({"iat": iat, "nbf": nbf, "exp":exp}, signature, algorithm='HS256').decode('utf-8')

header = {"content-type": "application/json", "Authorization": "jwt {}".format(json_token)}
http_link = 'http://api.unifyapp.xyz:3828'

applicationRoutes = {
   'create_user' : '/user/create/', # POST, PATCH
   'user_control' : '/user/'        # GET, PUT, DELETE
}



#j = '{"data":  { "Description": "description here", "First_Name": "John", "Instagram_Link": null, "Last_Name": "Doe", "Profile_Picture": null, "Twitther_Link": null}}'


		
#j = {"User_ID":"Temp123","Friend_ID":"Wall123"} #Find friend payload layout
class FindFriendPayload(object):
	def __init__(self,j):
		response = requests.get(
		http_link + applicationRoutes['user_control'] + j["User_ID"], 
		data = j, 
		headers = header
		)
		self._dict_ = response.text #might be this -- response.json() or json.loads(j)		
		
		
#Profile payload not needed, because the login payload will return the profile if the user_id and password are correct
#j = {"User_ID":"Temp123","Password":"Temppassword123"} #Login payload layout
class LoginPayload(object): 
	def __init__(self,j):
		response = requests.get(
		http_link + applicationRoutes['user_control'] + j["User_ID"], 
		data = j, 
		headers = header
		)
		self._dict_ = response.text #might be this -- response.json() or json.loads(j)


	
##### ----------------- THE POST REQUEST DOESN'T CURRENTLY WORK! ------------------ #####
	
#Sign up payload layout
#j = {"User_ID":"Temp123","Email":"temp@gmail.com","First_Name":"Temp","Last_Name":"Chair","DateOfBirth":"2000-05-27","Password":"Temppassword123","Profile_Picture":null,"Twitter_Link":"https://twitter.com/temp/","Instagram_Link":"https://www.instagram.com/temp/","Description":"Temp likes Computer Science","User_Created":"2020-02-20T14:02:32Z","Last_Login":"2020-02-27T17:40:32Z"}
class SignUpPayload(object):
	def __init__(self,j):
		response = requests.post(
		http_link + applicationRoutes['create_user'] + j["User_ID"],
		json = j, 
		headers = header
		)
		self.__dict__ = response.text #might be this -- response.json() or json.loads(j)

	
#j = {"User_ID":"Temp123","Event_ID":"CS123"} #Event payload layout
class EventPayload(object):
	def __init__(self,j):
		response = requests.get(
		http_link + applicationRoutes['user_control'] + j["User_ID"], 
		data = j, 
		headers = header
		)
		self._dict_ = response.text #might be this -- response.json() or json.loads(j)

#TEMPORARY - testing profile ids

k = '{"data": {"Profile_Picture": "https://images.unsplash.com/photo-1501743029101-21a00d6a3fb9?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1050&q=80",' \
    ' "Profile_Picture2": "https://images.unsplash.com/photo-1501744025452-768f823e41bc?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1050&q=80", ' \
    ' "Profile_Picture3": "https://images.unsplash.com/photo-1491438590914-bc09fcaaf77a?ixlib=rb-1.2.1&auto=format&fit=crop&w=1050&q=80", "First_Name": "Leyla", ' \
    '"Last_Name": "Moore", "Description": "Hi, I am a first year who would love to meet more like-minded students!", ' \
    '"User_Tag": "Chemistry", "User_Tag2": "Archery", "User_Tag3": "Chess", "User_Tag4": "Anime", "User_Tag5": "Jazz",' \
    ' "User_Tag6": "Terrible Film", "Instagram_Link": null, "Spotify_Link": null, "Twitter_Link": null, '\
    ' "Linked_In": "https://www.linkedin.com/"}}'

class ProfilePayload(object):
	def __init__(self, k):
		self.__dict__ = json.loads(k)


# Initial page shown when app is first downloaded
class Initial(Screen):
	pass


# Login class
class Login(Screen):
	pass


# Register class
class Register(Screen):
	pass


# Profile creation class
class ProfileCreation(Screen):
	def select(self, *args):
		try:
			print(args[1][0])

		except:
			pass



# Class for the profile, find & event sections
class MainSections(Screen):
	pass


class RV(BoxLayout):
	def populate(self):
		self.rv.data = [{'value': ''.join(sample(ascii_lowercase, 6))} for x in range(50)]
		#p = ProfilePayload(j)
		#self.rv.data.append({'value' : p.data["First_Name"]}) 

	
class MatchProfile(Screen):
	def on_pre_enter(self, *args):
		print("number of match_prof ids = ", len(self.ids))
		# photos
		#self.img.source =
		#self.img2.source =
		#self.img3.source =

		# full name
		#self.fullname.text =

		# about me description
		#self.description.text =

		# interest tags x6
		#self.course.text = "#" +
		#self.tag2.text = "#" +
		#self.tag3.text = "#" +
		#self.tag4.text = "#" +
		#self.tag5.text = "#" +
		#self.tag6.text = "#" +

	def getText(self):
		return "View LinkedIn [ref=profile][color=DC143C]profile[/color][/ref] "

	# Opens LinkedIn profile in the browser
	def urlLink(self, url, ref):
		#url =
		#_dict = {"profile": url}
		_dict = {"profile": "https://www.linkedin.com/"}

		# Opens new tab in browser
		webbrowser.open(_dict[ref], new=1)


class UnifyScreen(Screen):
	fullscreen = BooleanProperty(False)

	
# Profile class
class Profile(Screen):
	def on_pre_enter(self, *args):
		p = ProfilePayload(k)

		# photos
		self.img.source = p.data["Profile_Picture"]
		self.img2.source = p.data["Profile_Picture2"]
		self.img3.source = p.data["Profile_Picture3"]

		# full name
		self.fullname.text = p.data["First_Name"] + " " + p.data["Last_Name"]

		# about me description
		self.description.text = p.data["Description"]

		# interest tags x6
		self.course.text = "#" + p.data["User_Tag"]
		self.tag2.text = "#" + p.data["User_Tag2"]
		self.tag3.text = "#" + p.data["User_Tag3"]
		self.tag4.text = "#" + p.data["User_Tag4"]
		self.tag5.text = "#" + p.data["User_Tag5"]
		self.tag6.text = "#" + p.data["User_Tag6"]

	def getText(self):
		return "View LinkedIn [ref=profile][color=DC143C]profile[/color][/ref] "

	# Opens LinkedIn profile in the browser
	def urlLink(self, url, ref):
		p = ProfilePayload(k)

		url = p.data["Linked_In"]
		_dict = {"profile": url}

		# Opens new tab in browser
		webbrowser.open(_dict[ref], new=1)
	
		
# Friends class
class Friends(BoxLayout):
	pass
		
	
# Events class
class Events(BoxLayout):
	def getText(self):
		return "[ref=Create][color=800080]Create[/color][/ref] your own event!"


# Create event class
class CreateEvent(Screen):
	def select(self, *args):
		try:
			print(args[1][0])

		except:
			pass


# View event class
class ViewEvent(Screen):
	pass


# Settings class
class AppSettings(Screen):
	pass


# Report event class
class ReportEvent(Screen):
	pass


# Report user class
class ReportUser(Screen):
	pass


# Code for RoundedButton adapted from Youtuber 'Daniel kolim'
# Available at https://www.youtube.com/watch?v=lo6KFW2kt84
class RoundedButton(TouchRippleBehavior, Button):
	def on_touch_down(self, touch):
		collide_point = self.collide_point(touch.x, touch.y)
		if collide_point:
			touch.grab(self)

			self.background_color[3] = 0

			self.ripple_show(touch)

			self.dispatch('on_press')
			return True
		return False


	def on_touch_up(self, touch):
		if touch.grab_current is self:
			touch.ungrab(self)
			self.ripple_fade()

			def defer_release(dt):
				self.dispatch('on_release')

			Clock.schedule_once(defer_release, self.ripple_duration_out)
			return True
		return False


# Acts like a button & an image
class ImageButton(ButtonBehavior, Image):
	pass
	

class UnifyApp(App):
	"""Unify base kivy app

	See unify,kv for kivy widget definition
	"""
	
	index = NumericProperty(-1)

	# Build creates and gets the available screens, loads them from, 
	# the data/screens folder, sets it to the zero index screen
	def build(self):
		self.screens = {} # Empty screen list
		self.available_screens = sorted([	
			'app_settings', 'create_event', 'eventFind', 'friends', 'match', 'match_profile', 'profile',
		'report_event', 'report_user', 'view_event']) # Explicitly sets the available screens
		self.screen_names = self.available_screens 
		curdir = dirname(__file__)
		self.available_screens = [join(curdir, 'data', 'screens', '{}.kv'.format(fn).lower()) for fn in self.available_screens] # Create a list of available screens from the kv files
		self.go_screen(4) # goto match screen 
		
		#print(len(self.available_screens))
		
		return self.root

	def go_screen(self, idx):
		self.index = idx # set the current screen index
		screen = self.load_screen(self.index) # build the screen kv form
		sm = self.root.ids.main.ids.sm
		sm.switch_to(screen, direction='left') # switch the screen
		#self.populate()

		if self.index == 0:
			title = self.root.ids.main.ids.title
			title.text = "Settings"
		elif self.index == 1:
			title = self.root.ids.main.ids.title
			title.text = "Create Event"
		elif self.index == 2:
			title = self.root.ids.main.ids.title
			title.text = "Find Events"
		elif self.index == 3:
			title = self.root.ids.main.ids.title
			title.text = "My Friends"
		elif self.index == 4:
			title = self.root.ids.main.ids.title
			title.text = "Find Friends"
		elif self.index == 5:
			title = self.root.ids.main.ids.title
			title.text = "Student's Profile"
		elif self.index == 6:
			title = self.root.ids.main.ids.title
			title.text = "My Profile"
		elif self.index == 7:
			title = self.root.ids.main.ids.title
			title.text = "Report an Event"
		elif self.index == 8:
			title = self.root.ids.main.ids.title
			title.text = "Report a User"
		elif self.index == 9:
			title = self.root.ids.main.ids.title
			title.text = "View Event"
		
	
	def load_screen(self, index):
		# print('loading screen')
		if index in self.screens:
				return self.screens[index]
		else:
				self.screens[index] = screen = Builder.load_file(self.available_screens[index]) # build the screen
				return screen

# main
if __name__ == '__main__':
		UnifyApp().run()
