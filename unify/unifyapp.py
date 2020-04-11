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
from kivy.uix.recycleview import RecycleView

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

#TEMPORARY - testing profile, match and event ids
profile = '{"data": {"Profile_Picture": "https://images.unsplash.com/photo-1501743029101-21a00d6a3fb9?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1050&q=80",' \
    ' "Profile_Picture2": "https://images.unsplash.com/photo-1501744025452-768f823e41bc?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1050&q=80", ' \
    ' "Profile_Picture3": "https://images.unsplash.com/photo-1491438590914-bc09fcaaf77a?ixlib=rb-1.2.1&auto=format&fit=crop&w=1050&q=80", "First_Name": "Leyla", ' \
    '"Last_Name": "Moore", "Description": "Hi, I am a first year who would love to meet more like-minded students!", ' \
    '"User_Tag": ["Chemistry", "Archery", "Chess", "Anime", "Jazz", "Terrible Film"], "Instagram_Link": null, "Spotify_Link": null, "Twitter_Link": null, '\
    ' "Linked_In": "https://www.linkedin.com/"}}'

match = '{"data": {"Profile_Picture": "https://images.unsplash.com/photo-1513020954852-86e7e44d3113?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",' \
	' "Profile_Picture2": "https://images.unsplash.com/photo-1504263977680-01bebd8765b1?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1050&q=80", ' \
	' "Profile_Picture3": "https://images.unsplash.com/photo-1514867036548-8c2a9178b4fb?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=720&q=80", "First_Name": "Austin", ' \
	' "Last_Name": "Moran", "Description": "Hi there! I am new to the area and could do with more friends.", ' \
	' "User_Tag": ["Sociology", "Anime", "Film", "Archery", "Judo", "Guitar"], "Instagram_Link": null,' \
	' "Spotify_Link": null, "Twitter_Link": null, '\
	' "Linked_In": "https://www.linkedin.com/"}}'

event = '{"data": {"Event_Picture": "https://images.unsplash.com/photo-1549389594-232f692594d4?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1050&q=80", ' \
	' "Name": "Paintballing", "Description": "Hi! We are going paintballing this weekend to celebrate the end of exam season. Please join us!", "DateTime": "2020-05-23 13:00:00",' \
	' "Event_Location": "Westmoor Lane, LN1 2JW"}}'

# Temporary
class ProfilePayload(object):
	def __init__(self, k):
		self.__dict__ = json.loads(k)


# Initial page shown when app is first downloaded
class Initial(Screen):
	pass


class Login(Screen):
	def on_pre_leave(self):
		j = {"User_ID": "Temp123", "Email:": self.uni_email.text, "Password": self.password.text}
		# GET request
		# user_login = LoginPayload(j)
		# print(j)


class Register(Screen):
	def on_pre_leave(self):

		j = {
			"User_ID": "Temp123", "Email": self.uni_email.text, "First_Name": self.first_name.text,
			"Last_Name": self.last_name.text, "DateOfBirth": self.dob.text, "Password": self.password.text
		}

		# POST request
		# user_info = SignUpPayload(j
		# print(j)


class ProfileCreation(Screen):
	def select(self, *args):
		try:
			profile_pictures = {}
			profile_pictures["pic_one"] = args[1][0]
			profile_pictures["pic_two"] = args[1][1]
			profile_pictures["pic_three"] = args[1][2]

			print(profile_pictures)

		except:
			pass

	def on_pre_leave(self):
		interest_tags = self.tags.text.splitlines()

		j = {
			"User_ID": "Temp123", "Picture_Path": "blank", "Description": self.description.text,
			"User_Tag": interest_tags,
			"LinkedIn_Link": self.linked_in.text
		}

		# POST request
		# user_info = SignUpPayload(j)
		# print(j)



# Class for the profile, find & event sections
class MainSections(Screen):
	pass


class MatchList(BoxLayout):
	pass

class MatchRecycle(RecycleView):

	def on_parent(self,widget,parent): # This function is loaded when the widget is added to the screen
		#self.data = [{'value': ''.join(sample(ascii_lowercase, 6))} for x in range(50)]
		self.populate()
	
	def populate(self):
		# j = {}
		# pl = json.loads(j)
		pl = {'User_ID':'15','First_Name':'Jeremy','Last_Name':"Lee",'Picture_Path':'placeholder','User_Tag':'#nice' }
		self.data.append({'id':pl["User_ID"],'name': pl["First_Name"]+" "+pl["Last_Name"],'tags':pl["User_Tag"],'imagePath':["Picture_Path"]})
		

class EventList(BoxLayout):
	pass


class EventRecycle(RecycleView):

	def on_parent(self,widget,parent): # This function is loaded when the widget is added to the screen
		self.data = [{'value': ''.join(sample(ascii_lowercase, 6))} for x in range(50)]
	

class MatchProfile(Screen):
	def on_pre_enter(self, *args):
		p = ProfilePayload(match)

		# photos
		self.img.source = p.data["Profile_Picture"]
		self.img2.source = p.data["Profile_Picture2"]
		self.img3.source = p.data["Profile_Picture3"]

		# full name
		self.fullname.text = p.data["First_Name"] + " " + p.data["Last_Name"]

		# about me description
		self.description.text = p.data["Description"]

		# interest tags
		tags = p.data["User_Tag"]

		for x in tags:
			button = OutlinedButton(text="#" + x)
			self.tag_grid.add_widget(button)
			
	def on_pre_leave(self):
		self.tag_grid.clear_widgets()


	def getText(self):
		return "View LinkedIn [ref=profile][color=DC143C]profile[/color][/ref] "

	# Opens LinkedIn profile in the browser
	def urlLink(self, url, ref):
		p = ProfilePayload(match)

		url = p.data["Linked_In"]
		_dict = {"profile": url}

		# Opens new tab in browser
		webbrowser.open(_dict[ref], new=1)


class UnifyScreen(Screen):
	fullscreen = BooleanProperty(False)

	
class Profile(Screen):
	def on_pre_enter(self, *args):
		p = ProfilePayload(profile)

		# photos
		self.img.source = p.data["Profile_Picture"]
		self.img2.source = p.data["Profile_Picture2"]
		self.img3.source = p.data["Profile_Picture3"]

		# full name
		self.fullname.text = p.data["First_Name"] + " " + p.data["Last_Name"]

		# about me description
		self.description.text = p.data["Description"]

		# interest tags
		tags = p.data["User_Tag"]

		for x in tags:
			button = OutlinedButton(text="#" + x)
			self.tag_grid.add_widget(button)

	def on_pre_leave(self):
		self.tag_grid.clear_widgets()

	def getText(self):
		return "View LinkedIn [ref=profile][color=DC143C]profile[/color][/ref] "

	# Opens LinkedIn profile in the browser
	def urlLink(self, url, ref):
		p = ProfilePayload(k)

		url = p.data["Linked_In"]
		_dict = {"profile": url}

		# Opens new tab in browser
		webbrowser.open(_dict[ref], new=1)
	
		
class Friends(BoxLayout):
	pass


class CreateEvent(Screen):
	def select(self, *args):
		try:
			event_picture = args[1][0]

			print(event_picture)
		except:
			pass

	def on_pre_leave(self):

		j = {
			"User_ID": "Temp123", "Name": self.event_name.text, "Description": self.description.text,
			"DateTime": self.datetime.text, "Event_Location": self.location.text
		}

		# POST request
		# event_info =
		# print(j)


class ViewEvent(Screen):
	def on_pre_enter(self):
		p = ProfilePayload(event)

		# event picture
		self.event_img.source = p.data["Event_Picture"]

		# event name
		self.event_name.text = p.data["Name"]

		# event creator
		# self.creator.text =

		# event description
		self.description.text = p.data["Description"]

		# event date & time
		self.datetime.text = p.data["DateTime"]

		# event location
		self.location.text = p.data["Event_Location"]


class AppSettings(Screen):
	def select(self, *args):
		try:
			profile_pictures = {}
			profile_pictures["pic_one"] = args[1][0]
			profile_pictures["pic_two"] = args[1][1]
			profile_pictures["pic_three"] = args[1][2]

			print(profile_pictures)
		except:
			pass

	def on_pre_leave(self):
		new_tags = self.new_tags.text.splitlines()

		j = {
			"User_ID": "Temp123", "Picture_Path": "fill", "Description": self.new_description.text,
			"User_Tag": new_tags
		}

		# POST request
		# new_info =  SignUpPayload(j)
		# print(j)


class ReportEvent(Screen):
	def on_pre_leave(self):

		report_event_reason = [None, None, None, None]
		if self.reason1.active:
			report_event_reason[0] = "Objectionable content on the event's page"

		if self.reason2.active:
			report_event_reason[1] = "Fears over the safety of the event"

		if self.reason3.active:
			report_event_reason[2] = "Fraud and deception"

		if self.reason4.text != '':
			report_event_reason[3] = self.reason4.text

		print(report_event_reason)

		self.reason1.active = False
		self.reason2.active = False
		self.reason3.active = False
		self.reason4.text = ''

		j = {
			"Reporting_User_ID": "fill", "Reported_Event_ID": "fill", "Report_Reason": report_event_reason
		}

		# POST request
		# print(j)


class ReportUser(Screen):
	def on_pre_leave(self):

		report_reason = [None, None, None, None]
		if self.reason1.active:
			report_reason[0] = "Objectionable content in profile"

		if self.reason2.active:
			report_reason[1] = "Bullying and harrassment through social media"

		if self.reason3.active:
			report_reason[2] = "Fake profile - student does not exist"

		if self.reason4.text != '':
			report_reason[3] = self.reason4.text

		print(report_reason)

		self.reason1.active = False
		self.reason2.active = False
		self.reason3.active = False
		self.reason4.text = ''

		j = {
			"Reporting_User_ID": "fill", "Reported_Event_ID": "fill", "Report_Reason": report_reason
		}

		# POST request
		# print(j)


class OutlinedButton(Button):
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
