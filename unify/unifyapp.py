# ---------------------------------------------------------------------
# Kivy App file
# Defines all the classes for the screens of the Unify app
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

from clientside.resources import (
	User_Requests, 
	Event_Requests, 
	Report_Requests,
	get_image_url
)

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
	# Login login_click:
	# - When the login button is clicked:
	# 	- Send user Request
	#   - Add to store
	def login_click(self):
		j = { "Email": self.uni_email.text, "Password": self.password.text}
		user_details = User_Requests.login(j)
		if user_details is not None:
			UserStore.put(
				'user_info',  
				token=user_details["access_token"], 
				id=user_details["data"]["User_ID"]
			)

	# Login on_leave:
	# - Clears text after leaving screen
	def on_leave(self):
		self.uni_email.text = ''
		self.password.text = ''

# ------------
# Register Screen
# ------------
class Register(Screen):
	def save_user(self):

		j = {
			"Email": self.uni_email.text, "First_Name": self.first_name.text,
			"Last_Name": self.last_name.text, "DateOfBirth": self.dob.text, 
			"Password": self.password.text
		}

		created_user = User_Requests.create(j)
		if created_user is not None:
			UserStore.put(
				'user_info',  
				token=created_user["access_token"], 
				id=created_user["data"]["User_ID"]
			)

	def on_leave(self):
		self.uni_email.text = ''
		self.first_name.text = ''
		self.last_name.text = ''
		self.dob.text = ''
		self.password.text = ''

# ------------
# Profile Creation Screen
# ------------
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

			self.filechooser.selection.clear()
			
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
			'Description': self.description.text if self.description.text is not None else '',
			'Twitter_Link': self.twitter.text if self.twitter.text is not None else '',
			'Instagram_Link': self.instagram.text if self.instagram.text is not None else '',
			'Spotify_Link': self.spotify.text if self.spotify.text is not None else '',
			'LinkedIn_Link':self.linked_in.text if self.linked_in.text is not None else ''
		}

		user_edits = User_Requests.edit(
			UserStore.get('user_info')['id'],
			UserStore.get('user_info')["token"],
			j
		)

		user_tags = User_Requests.add_tags(
			UserStore.get('user_info')['id'],
			UserStore.get('user_info')["token"],
			interest_tags
		)

	def on_leave(self):
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
		verif = User_Requests.verify(
			UserStore.get('user_info')['id'],
			UserStore.get('user_info')["token"],
			code
		)

		if verif is not None:
			App.get_running_app().root.current = 'profile_creation'
		else:
			popupWindow = Popup(
				title="Code Incorrect!",
				content=Label(
					text="Provided code was incorrect!",
					font_size=14, halign='center'),
				size_hint=(None, None), size=(200, 200)
			)
			popupWindow.open()

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
		self.populate()
	
	# MatchRecycle populate:
	# - Populates the screen with loaded json users
	def populate(self):

		matches = User_Requests.get_matches(
			UserStore.get('user_info')["token"]
		)

		print(matches)

		if matches is not None:
			for match in matches['data']:
				self.data.append({
					'id':str(match["User_ID"]),
					'name': match["First_Name"]+" "+match["Last_Name"],
					'tags':str(match["Matches"]),
					'picture': get_image_url(
						match['User_ID'],
						match["Picture_Path"]
					) if match['Picture_Path'] is not '' else User_Requests.get_default_image()
				})

# -----
# MatchRow 
# -----
class MatchRow(BoxLayout):
	def load_profile(self, user_id):
		UserStore.put('curr_profile', id=user_id)
		App.get_running_app().go_screen(6)

# ------------
# Match Profile Screen
# ------------
class MatchProfile(Screen):
	def on_parent(self, widget, parent):
		if UserStore.exists('curr_profile'):
			self.populate_match(id=UserStore.get('curr_profile')['id'])

	def populate_match(self, id=None):

		this_user = User_Requests.get_info(
			id,
			UserStore.get('user_info')["token"]
		)

		for pic in this_user['data']['pictures']:
			self.user_pictures.add_widget(
				AsyncImage(source=pic)
			)
		
		for tag in this_user['data']['tags']:
			self.tag_grid.add_widget(
				OutlinedButton(text='#' + tag)
			)

		self.fullname.text = this_user['data']["First_Name"] + " " + this_user['data']["Last_Name"]
		self.description.text = this_user['data']["Description"] if this_user['data']["Description"] is not None else ''
		self.instagram.text = this_user['data']["Instagram_Link"] if this_user['data']["Instagram_Link"] is not None else 'Not Provided'
		self.twitter.text = this_user['data']["Twitter_Link"] if this_user['data']["Twitter_Link"] is not None else 'Not Provided'
		self.spotify.text = this_user['data']["Spotify_Link"] if this_user['data']["Spotify_Link"] is not None else 'Not Provided'
		self.linkedin_link = this_user['data']["LinkedIn_Link"] if this_user['data']["LinkedIn_Link"] is not None else 'Not Provided'

		self.getText()

	# Assigns the text to the LinkedIn section of the profile
	def getText(self):
		if self.linkedin_link != 'Not Provided':
			self.linked_in.text = "View LinkedIn [ref=profile][color=DC143C]profile[/color][/ref]"

		else:
			self.linked_in.text = "Not Provided"

	# Opens LinkedIn profile in the browser
	def urlLink(self, url, ref):
		url = self.linkedin_link
		_dict = {"profile": url}

		# Opens new tab in browser
		webbrowser.open(_dict[ref], new=1)
	
	def on_leave(self, *args):
		UserStore.delete('curr_profile')
		self.user_pictures.clear_widgets()
		self.tag_grid.clear_widgets()

# ------------
# User Profile Screen
# ------------
class Profile(Screen):
	def on_parent(self, widget, parent):
		self.populate_profile()

	def populate_profile(self, *args):
		
		this_user = User_Requests.get_info(
			UserStore.get('user_info')['id'],
			UserStore.get('user_info')["token"]
		)

		for pic in this_user['data']['pictures']:
			self.user_pictures.add_widget(
				AsyncImage(source=pic)
			)
		
		for tag in this_user['data']['tags']:
			self.tag_grid.add_widget(
				OutlinedButton(text='#' + tag)
			)

		self.fullname.text = this_user['data']["First_Name"] + " " + this_user['data']["Last_Name"]
		self.description.text = this_user['data']["Description"] if this_user['data']["Description"] is not None else ''
		self.instagram.text = this_user['data']["Instagram_Link"] if this_user['data']["Instagram_Link"] is not None else 'Not Provided'
		self.twitter.text = this_user['data']["Twitter_Link"] if this_user['data']["Twitter_Link"] is not None else 'Not Provided'
		self.spotify.text = this_user['data']["Spotify_Link"] if this_user['data']["Spotify_Link"] is not None else 'Not Provided'
		self.linkedin_link = this_user['data']["LinkedIn_Link"] if this_user['data']["LinkedIn_Link"] is not None else 'Not Provided'

		self.getText()

	# Assigns the text to the LinkedIn section of the profile
	def getText(self):
		if self.linkedin_link != 'Not Provided':
			self.linked_in.text = "View LinkedIn [ref=profile][color=DC143C]profile[/color][/ref]"

		else:
			self.linked_in.text = "Not Provided"

	# Opens LinkedIn profile in the browser
	def urlLink(self, url, ref):
		url = self.linkedin_link
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

# class EventFindScreen(UnifyScreen):
# 	def on_enter(self, *args):
# 	 	self.efs.rvEvent.populate()

class EventList(BoxLayout):
	def getText(self):
		return "[ref=Create][color=800080]Create[/color][/ref] your own event!"

class EventRow(BoxLayout):

	def load_event(self, event_id):
		UserStore.put('curr_event', id=event_id)
		App.get_running_app().go_screen(10)

class EventRecycle(RecycleView):
	def on_parent(self,widget,parent): # This function is loaded when the widget is added to the screen
		self.populate()

	def populate(self):
		events = User_Requests.get_feed(
			UserStore.get('user_info')["token"],
			limit = 100
		)

		if events is not None:
			for e in events['data']:
				self.data.append({
					'id':str(e['Event_ID']),
					'name': e["Name"], 
					'imagePath': e["Picture_Path"] if e['Picture_Path'] is not None else '',
					#'attendees': e['Attendees']
				})


# ------------
# Create Event Screen
# ------------
class CreateEvent(Screen):

	_image = ''

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

			event_image = Event_Requests.upload_image(
				UserStore.get('user_info')["token"],
				filename[0]
			)
			
			if event_image is not None:
				print(event_image['data']['image'])
				self._image = event_image['data']['image']

			self.filechooser.selection.clear()

		except:
			pass

	def save_event(self):

		got_date_time = self.datetime.text.split()
		if len(got_date_time) > 1:
			got_date_time = '{date}T{time}Z'.format(date=got_date_time[0],time=got_date_time[1])

		j = {
			"Name": self.event_name.text, "Description": self.description.text,
			"DateTime": got_date_time, "Location": self.location.text,
			'Picture_Path': self._image
		}

		event = Event_Requests.create(
			UserStore.get('user_info')["token"],
			j
		)

		if event is not None:
			self.load_event(event['data']['Event_ID'])

	def load_event(self, event_id):
		UserStore.put('curr_event', id=event_id)
		App.get_running_app().go_screen(10)

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
		if UserStore.exists('curr_event'):
			self.populate_event(id=UserStore.get('curr_event')['id'])

	def populate_event(self, id=None):
		if id is not None:
			event = Event_Requests.get(
				int(id),
				UserStore.get('user_info')["token"],
			)
			if event is not None:
				self.event_img.source = event['data']['Picture_Path']
				self.event_name.text = event['data']['Name']
				self.description.text = event['data']["Description"]
				self.datetime.text = event['data']["DateTime"]
				self.location.text = event['data']["Location"]
				self.creator.text = '{fname} {lname}'.format(
					fname = event['data']['Creator']['First_Name'],
					lname = event['data']['Creator']['Last_Name']
				)

	def on_leave(self, *args):
		UserStore.delete('curr_event')


# ------------
# App Settings Screen
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

			self.filechooser.selection.clear()
			
		except:
			pass


	def change_profile(self):
		new_tags = self.new_tags.text.splitlines()

		
		j = {
			"Description": self.new_description.text
		}

	def log_out(self):
		UserStore.delete('user_info')
		App.get_running_app().root.current = "initial_screen"

	def on_leave(self):
		self.new_description.text = ''
		self.new_tags.text = ''

# ------------
# Change Password Screen
# ------------
class ChangePassword(Screen):
	def check_code(self, code):
		# user only sees the 'enter new password' section if their code is correct
		self.prompt.text = "Enter your new password: "
		self.new_pass.height = dp(30)
		self.save.back_color = (192, 192, 192, 0.3)
		self.save.height = dp(30)
		self.save.text = "Save"

	def save_password(self, new_password):

		j = {
			"Password": new_password
		}

		# hides the 'enter new password' section again
		self.prompt.text = ''
		self.new_pass.height = dp(0)
		self.new_pass.text = ''
		self.save.back_color = (192, 192, 192, 0)
		self.save.height = dp(0)
		self.save.text = ''

		self.pass_code.text = ''
		
# ------------
# Report Screens
# ------------
class ReportUser(Screen):
	def save_user_report(self):
		report_reason = ['', '', '', '']
		if self.reason1.active:
			report_reason[0] = "Objectionable content in profile"

		if self.reason2.active:
			report_reason[1] = "Bullying and harassment through social media"

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
			"Report_Reason": user_reasons
		}

	def on_leave(self):
		self.reason1.active = False
		self.reason2.active = False
		self.reason3.active = False
		self.reason4.text = ''


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
			"Report_Reason": event_reasons
		}

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
# App Definition
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
		if index in self.screens:
				return self.screens[index]
		else:
				self.screens[index] = screen = Builder.load_file(self.available_screens[index]) # build the screen
				return screen

# main
if __name__ == '__main__':
		UnifyApp().run()
