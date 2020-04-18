# ---------------------------------------------------------------------
# Kivy App file
# Defines all the classes for the screens of the app
# ---------------------------------------------------------------------


# Kivy imports
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout  
from kivy.uix.carousel import Carousel

from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label

from kivy.uix.button import Button
from kivy.uix.behaviors.touchripple import TouchRippleBehavior
from kivy.clock import Clock
from kivy.uix.recycleview import RecycleView
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.storage.jsonstore import JsonStore

# Misc. Imports

from os.path import dirname, join
from random import sample
from string import ascii_lowercase

import os
import webbrowser

# ??? REMOVE ???
import requests
import json
import jwt
from datetime import datetime
import time

from clientside.resources import User_Requests

UserStore = JsonStore('userdata/UserStore.json') 

# ------------
# Initial Screen
# ------------
class Initial(Screen):
	pass	

# ------------
# Login Screen
# ------------
class Login(Screen):
	
	# REDUNDANT, ??? REMOVE ???
	#def on_pre_leave(self):
	#	j = {"User_ID": "Temp123", "Email:": self.uni_email.text, "Password": self.password.text}
		
	# Login on_leave:
	# - Clears text after leaving screen
	def on_leave(self):
		self.uni_email.text = ''
		self.password.text = ''


	# Login login_click:
	# - When the login button is clicked:
	# 	- Send user Request
	#   - Add to store
	def login_click(self):
		j = { "Email": self.uni_email.text, "Password": self.password.text}
		user_details = User_Requests.login(j)
		if user_details is not None:
			UserStore.put('user_info',  token=user_details["access_token"], id=user_details["data"]["User_ID"])
	

class Register(Screen):
	def save_user(self):

		j = {
			"Email": self.uni_email.text, "First_Name": self.first_name.text,
			"Last_Name": self.last_name.text, "DateOfBirth": self.dob.text, 
			"Password": self.password.text
		}

		createdUser = User_Requests.create(j)
		if createdUser is not None:
			UserStore.put(
				'user_info',  
				token=createdUser["access_token"], 
				id=createdUser["data"]["User_ID"]
			)
		
		# POST request (POST/user/create)

	def on_leave(self):
		self.uni_email.text = ''
		self.first_name.text = ''
		self.last_name.text = ''
		self.dob.text = ''
		self.password.text = ''


class AccountVerification(Screen):
	def verify(self, code):
		pass

		# PATCH request (PATCH/user/{USER_ID}/verify
		# Verification_Code


class ProfileCreation(Screen):
	
	# ProfileCreation select:
	# - When a photo is selected:
	# 	- Open/close popupwindow
	#   - Get the selection
	#   - Send picture request !!! ADD !!!
	def select(self, filename):
		try:
			popupWindow = Popup(
				title="Photo Selection",
				content=Label(
					text="Photo selected and saved! \n \n Click anywhere on the \n screen to continue...",
					font_size=14, halign='center'),
				size_hint=(None, None), size=(200, 200)
			)
			popupWindow.open()

			user_image = User_Requests.upload_image(
				UserStore.get('user_info')["token"],
				filename[0]
			)
			print(user_image)
			
			self.filechooser.selection.clear()
			

			# POST REQ	!!! ADD !!!
		except:
			pass
	
	# ProfileCreation save_profile:
	# - When the save button is clicked:
	#   - Add all info to json
	#   - Send request
	#   - Add user to userstore
	def save_profile(self):

		interest_tags = self.tags.text.splitlines()

		j = { 
			'Description': self.description.text,
			'Twitter_Link': self.twitter.text,
			'Instagram_Link': self.instagram.text,
			'Spotify_Link': self.spotify.text,
			'LinkedIn_Link':self.linked_in.text
		}

		user_edits = User_Requests.edit(
			UserStore.get('user_info')['id'],
			UserStore.get('user_info')["token"],
			j
		)

		tags = {
			'User_Tags':interest_tags
		}

		user_tags = User_Requests.add_tags(
			UserStore.get('user_info')['id'],
			UserStore.get('user_info')["token"],
			tags
		)

		# POST request (POST/image/{User_ID}/upload)

	def on_leave(self):
		self.uni_email.text = ''
		self.first_name.text = ''
		self.last_name.text = ''
		self.dob.text = ''
		self.password.text = ''
		self.description.text = ''
		self.instagram.text = ''
		self.twitter.text = ''
		self.spotify.text = ''
		self.linked_in.text = ''

		
# ------------
# Account Verification Screen
# ------------
class AccountVerification(Screen):
	def verify(self, code):
		pass

		# PATCH request (PATCH/user/{USER_ID}/verify
		# Verification_Code
		# !!! ADD !!!
		

# ----------------------------------------------------------------
# Main Screens
# ----------------------------------------------------------------

# ------------
# Config
# ------------

# Class for the profile, match & event sections
class MainSections(Screen):
	pass

class UnifyScreen(Screen):
	fullscreen = BooleanProperty(False)

# ------------
# MatchList Screen
# ------------

class MatchList(BoxLayout):
	pass

# -----
# MatchRecycle RecycleView
# -----
# Used for displaying all the matched users

class MatchRecycle(RecycleView):

	# MatchRecycle on_parent:
	# - Function is loaded when the widget is added to the screen
	# - Get match list Request from server
	# - Populates screen
	def on_parent(self,widget,parent): 
		# REQUEST !!! ADD !!!
		self.populate()
	
	# MatchRecycle populate:
	# - Populates the screen with loaded json users !!! ADD !!!
	def populate(self):
		# j = {}
		# pl = json.loads(j)
		pl = {'User_ID':'15','First_Name':'Jeremy','Last_Name':"Lee",'Picture_Path':'placeholder','User_Tag':'#nice' }
		self.data.append({
			'id':pl["User_ID"],
			'name': pl["First_Name"]+" "+pl["Last_Name"],
			'tags':pl["User_Tag"],
			'imagePath': pl["Picture_Path"]
			})
		
# ------------
# Match Profile Screen
# ------------

class MatchProfile(Screen):
	tags_filled = False

	def on_parent(self, widget, parent):
		self.populate_match()

	def populate_match(self, *args):
		pass
		# j = {}
		# match = json.loads(j)

		# Temporary
		#match = {
				#"UserID": "Temp235", 
				#"Profile_Picture": "https://images.unsplash.com/photo-1513020954852-86e7e44d3113?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
				#"Profile_Picture2": "https://images.unsplash.com/photo-1504263977680-01bebd8765b1?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1050&q=80",
				#"Profile_Picture3": "https://images.unsplash.com/photo-1514867036548-8c2a9178b4fb?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=720&q=80",
				#"First_Name": "Austin", "Last_Name": "Moran", 
				#"Description": "Hi there! I am new to the area and could do with more friends.",
				#"User_Tag": ["Sociology", "Anime", "Film", "Archery", "Judo", "Guitar"], 
				#"Linked_In": "https://www.linkedin.com/", "Instagram_Link": "@AusMoran", 
				#"Twitter_Link": "@AusMoran", "Spotify_Link": "AusMoran"
			#}

		# photos
		#self.img.source = match["Profile_Picture"]
		#self.img2.source = match["Profile_Picture2"]
		#self.img3.source = match["Profile_Picture3"]

		# full name
		#self.fullname.text = match["First_Name"] + " " + match["Last_Name"]

		# about me description
		#self.description.text = match["Description"]

		# interest tags
		#tags = match["User_Tag"]

		#if not self.tags_filled:
			#for x in tags:
				#button = OutlinedButton(text="#" + x)
				#self.tag_grid.add_widget(button)
			#self.tags_filled = True

		#if self.tags_filled:
			#pass

		# instagram handle
		#self.instagram.text = match["Instagram_Link"]

		# twitter handle
		#self.twitter.text = match["Twitter_Link"]

		# spotify username
		#self.spotify.text = match["Spotify_Link"]

		# linked in
		#self.linkedin_link = match["Linked_In"]

	def getText(self):
		return "View LinkedIn [ref=profile][color=DC143C]profile[/color][/ref] "

	# Opens LinkedIn profile in the browser
	def urlLink(self, url, ref):
		url = "https://www.linkedin.com/"
		#self.linkedin_link
		_dict = {"profile": url}

		# Opens new tab in browser
		webbrowser.open(_dict[ref], new=1)



# ------------
# User Profile Screen
# ------------
	
class Profile(Screen):
	tags_filled = False

	def on_parent(self, widget, parent):
		self.populate_profile()

	def populate_profile(self, *args):
		pass
		# j = {}
		# profile = json.loads(j)

		#profile = {
				#"UserID": "Temp123", "Profile_Picture": "https://images.unsplash.com/photo-1501743029101-21a00d6a3fb9?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1050&q=80",
				#"Profile_Picture2": "https://images.unsplash.com/photo-1501744025452-768f823e41bc?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1050&q=80",
				#"Profile_Picture3": "https://images.unsplash.com/photo-1491438590914-bc09fcaaf77a?ixlib=rb-1.2.1&auto=format&fit=crop&w=1050&q=80", "First_Name": "Leyla",
				#"Last_Name": "Moore", "Description": "Hi, I am a first year who would love to meet more like-minded students!",
				#"User_Tag": ["Chemistry", "Archery", "Chess", "Anime", "Jazz", "Terrible Film"],
				#"Linked_In": "https://www.linkedin.com/"
		#}

		# photos
		#self.img.source = profile["Profile_Picture"]
		#self.img2.source = profile["Profile_Picture2"]
		#self.img3.source = profile["Profile_Picture3"]

		# full name
		#self.fullname.text = profile["First_Name"] + " " + profile["Last_Name"]

		# about me description
		#self.description.text = profile["Description"]

		# interest tags
		#tags = profile["User_Tag"]

		#if not self.tags_filled:
			#for x in tags:
				#button = OutlinedButton(text="#" + x)
				#self.tag_grid.add_widget(button)
			#self.tags_filled = True

		#if self.tags_filled:
			#pass

		# instagram handle
		#self.instagram.text = ["Instagram_Link"]

		# twitter handle
		#self.twitter.text = ["Twitter_Link"]

		# spotify username
		#self.spotify.text = ["Spotify_Link"]

		# linked in
		#self.linkedin_link = profile["Linked_In"]

	def getText(self):
		return "View LinkedIn [ref=profile][color=DC143C]profile[/color][/ref] "

	# Opens LinkedIn profile in the browser
	def urlLink(self, url, ref):
		url = "https://www.linkedin.com/"
		#self.linkedin_link
		_dict = {"profile": url}

		# Opens new tab in browser
		webbrowser.open(_dict[ref], new=1)
	


# ------------
# Friends Screen
# ------------

class Friends(Screen):
	pass



# ------------
# EventList Screen
# ------------


class EventList(BoxLayout):
	def getText(self):
		return "[ref=Create][color=800080]Create[/color][/ref] your own event!"


class EventRecycle(RecycleView):
	def on_parent(self,widget,parent): # This function is loaded when the widget is added to the screen
		#self.data = [{'value': ''.join(sample(ascii_lowercase, 6))} for x in range(50)]
		self.populate()

	def populate(self):
		# j = {}
		# pl = json.loads(j)
		pl = {'Event_ID':'15','Name':'Paintball','Picture_Path':'placeholder' }
		self.data.append({'id':pl["Event_ID"],'name': pl["Name"], 'imagePath': pl["Picture_Path"]})



# ------------
# Create Event Screen
# ------------

class CreateEvent(Screen):
	def select(self, filename):
		try:
			popupWindow = Popup(
				title="Photo Selection",
				content=Label(
					text="Picture selected and saved! \n \n Click anywhere on the \n screen to continue...",
					font_size=14, halign='center'),
				size_hint=(None, None), size=(200, 200)
			)
			popupWindow.open()

			# POST REQ, ADD HERE: filename[0]
			self.filechooser.selection.clear()
			

			# POST REQ	!!! ADD !!!

		except:
			pass

	def save_event(self):

		j = {
			"Name": self.event_name.text, "Description": self.description.text,
			"DateTime": self.datetime.text, "Event_Location": self.location.text
		}

		# POST request

	def on_leave(self):
		self.event_name.text = ''
		self.description.text = ''
		self.datetime.text = ''
		self.location.text = ''
		

# ------------
# View Event Screen
# ------------


class ViewEvent(Screen):
	def on_parent(self, widget, parent):
		self.populate_event()

	def populate_event(self, *args):
		pass
		# j = {}
		# event = json.loads(j)

		# Temporary
		#event = {
				#"Event_ID": "CS123", "User_ID": "Temp123", "Event_Picture": "https://images.unsplash.com/photo-1549389594-232f692594d4?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1050&q=80",
				#"Name": "Paintballing", "Description": "Hi! We are going paintballing this weekend to celebrate the end of exam season. Please join us!", "DateTime": "2020-05-23 13:00:00",
				#"Event_Location": "Westmoor Lane, LN1 2JW"
			#}

		# event picture
		#self.event_img.source = event["Event_Picture"]

		# event name
		#self.event_name.text = event["Name"]

		# event creator
		# self.creator.text =

		# event description
		#self.description.text = event["Description"]

		# event date & time
		#self.datetime.text = event["DateTime"]

		# event location
		#self.location.text = event["Event_Location"]


# ------------
# App settings Screen
# ------------

class AppSettings(Screen):
	def select(self, filename):
		try:
			popupWindow = Popup(
				title="Photo Selection",
				content=Label(
					text="Photo selected and saved! \n \n Click anywhere on the \n screen to continue...",
					font_size=14, halign='center'),
				size_hint=(None, None), size=(200, 200)
			)
			popupWindow.open()

			# POST REQ, ADD HERE: filename[0]
			self.filechooser.selection.clear()
			

			# POST REQ	!!! ADD !!!
		except:
			pass


	def change_settings(self):
		# for users table
		j = {
			"Description": self.new_description.text
		}

		# PATCH request


		# for usertags table
		interest_tags = self.new_tags.text.splitlines()

		n = [{"User_ID": "Temp123", "UserTag": interest_tags[0]}, {"User_ID": "Temp123", "UserTag": interest_tags[1]}]

		# PATCH request (PATCH/user/{User_ID})
		# tags:[{User_ID": <ID>, "User_Tag": "<tag>}, {...}]

	def on_leave(self):
		self.new_description.text = ''
		self.new_tags.text = ''

# ------------
# Change pass Screen
# ------------

class ChangePassword(Screen):
	def check_code(self, code):
		# comparison 
		
		
		# user only sees the 'enter new password' section if their code is correct
		self.prompt.text = "Enter your new password: "
		self.new_pass.height = dp(30)
		self.save.back_color = (192, 192, 192, 0.3)
		self.save.height = dp(30)
		self.save.text = "Save"

	def save_password(self, new_password):
		# for users table
		j = {
			"Password": new_password
		}

		# PATCH request

		# hides the 'enter new password' section again
		self.prompt.text = ''
		self.new_pass.height = dp(0)
		self.new_pass.text = ''
		self.save.back_color = (192, 192, 192, 0)
		self.save.height = dp(0)
		self.save.text = ''

		self.pass_code.text = ''
		
# ------------
# Report Screen
# ------------

class ReportEvent(Screen):
	def save_event_report(self):
		report_event_reason = ['', '', '', '']
		if self.reason1.active:
			report_event_reason[0] = "Objectionable content on the event's page"

		if self.reason2.active:
			report_event_reason[1] = "Fears over the safety of the event"

		if self.reason3.active:
			report_event_reason[2] = "Fraud and deception"

		if self.reason4.text != '':
			report_event_reason[3] = self.reason4.text

		reasons = []

		# if item is not an empty string then add the item to the reasons list
		for x in report_event_reason:
			if x != '':
				reasons.append(x)

		# join the items in the reasons list into a single string
		event_reasons = ' & '.join(reasons)


		j = {
			"Reporting_User_ID": '', "Reported_Event_ID": '', "Report_Reason": event_reasons
		}

		# POST request

	def on_leave(self):	
		self.reason1.active = False
		self.reason2.active = False
		self.reason3.active = False
		self.reason4.text = ''
		


class ReportUser(Screen):
	def save_user_report(self):
		report_reason = ['', '', '', '']
		if self.reason1.active:
			report_reason[0] = "Objectionable content in profile"

		if self.reason2.active:
			report_reason[1] = "Bullying and harrassment through social media"

		if self.reason3.active:
			report_reason[2] = "Fake profile - student does not exist"

		if self.reason4.text != '':
			report_reason[3] = self.reason4.text

		reasons = []

		# if item is not an empty string then add the item to the reasons list
		for x in report_reason:
			if x != '':
				reasons.append(x)

		# join the items in the reasons list into a single string
		user_reasons = ' & '.join(reasons)
		

		j = {
			"Reporting_User_ID": '', "Reported_User_ID": '', "Report_Reason": user_reasons
		}

		# POST request

	def on_leave(self):
		self.reason1.active = False
		self.reason2.active = False
		self.reason3.active = False
		self.reason4.text = ''


# ------------
# Button Code
# ------------

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


class ImageButton(ButtonBehavior, Image):
	pass
	


# ----------------------------------------------------------------
# App definition
# ----------------------------------------------------------------

class UnifyApp(App):
	"""Unify base kivy app

	See unify,kv for kivy widget definition
	"""
	
	index = NumericProperty(-1)

	# Build creates and gets the available screens, loads them from, 
	# the data/screens folder, sets it to the zero index screen
	def build(self):
		print('BUILD HERE')
		self.screens = {} # Empty screen list
		self.available_screens = sorted([	
			'app_settings', 'change_password', 'create_event', 'eventfind', 'friends', 'match', 'match_profile', 'profile',
		'report_event', 'report_user', 'view_event']) # Explicitly sets the available screens
		self.screen_names = self.available_screens 
		curdir = dirname(__file__)
		self.available_screens = [join(curdir, 'data', 'screens', '{}.kv'.format(fn).lower()) for fn in self.available_screens] # Create a list of available screens from the kv files
		self.go_screen(5) # goto match screen 
		
		#print(len(self.available_screens))
		
		if UserStore.exists("user_info"):
			if UserStore.get('user_info')["token"] is not None:
				query = User_Requests.login({}, auth_token=UserStore.get('user_info')["token"])
				if query is not None:
					self.root.current = "main"
					self.go_screen(5)

		return self.root

	def go_screen(self, idx):
		self.index = idx # set the current screen index
		screen = self.load_screen(self.index) # build the screen kv form
		sm = self.root.ids.main.ids.sm
		sm.switch_to(screen, direction='left') # switch the screen

		screen_titles = {
			0: "Settings",
			1: "Change Your Password",
			2: "Create Event",
			3: "Find Events",
			4: "My Friends",
			5: "Find Friends",
			6: "Student Profile",
			7: "My Profile",
			8: "Report This Event",
			9: "Report This User",
			10: "View Event"
		}

		for x, y in screen_titles.items():
			if self.index == x:
				title = self.root.ids.main.ids.title
				title.text = y
		
	
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
