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
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors.touchripple import TouchRippleBehavior
from kivy.clock import Clock
from kivy.uix.recycleview import RecycleView
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.storage.jsonstore import JsonStore

from kivy.config import Config
Config.set('graphics', 'width', '540')
Config.set('graphics', 'height', '960')

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
		if 'error' not in user_details:
			UserStore.put(
				'user_info',  
				token=user_details["access_token"], 
				id=user_details["data"]["User_ID"]
			)
			App.get_running_app().go_screen(5)

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
		if 'error' not in created_user:
			UserStore.put(
				'user_info',  
				token=created_user["access_token"], 
				id=created_user["data"]["User_ID"]
			)
			App.get_running_app().go_screen(5)

	# - Clears text after leaving screen
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
	#   - Send picture request
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

	# - Clears text after leaving screen
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

		if 'error' not in verif:
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

# Class for the user profile, find friends & find event sections
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

		if 'error' not in matches:
			for match in matches['data']:
				tags = ''
				for i in range(0,len(match['Matches'])):
					if i < 3:
						tags += '#{}'.format(match['Matches'][i])
						if i != len(match['Matches']) - 1:
							tags += '\n'
					else:
						tags += '...'
						break

				self.data.append({
					'id':str(match["User_ID"]),
					'name': match["First_Name"]+" "+match["Last_Name"],
					'tags':tags,
					'picture': match['Picture_Path']
				})
	
	def on_pre_enter(self):
		print('matches')

# -----
# MatchRow 
# -----
class MatchRow(ButtonBehavior,BoxLayout):

	def load_profile(self, user_id):
		UserStore.put('curr_profile', id=user_id)
		App.get_running_app().go_screen(6)

	def on_press(self):
		self.load_profile(self.id)

# ------------
# Match Profile Screen
# ------------
class MatchProfile(Screen):

	_urls = {
		'Instagram':'',
		'Twitter':'',
		'Spotify':'',
		'LinkedIn':''
	}

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

		self.user_id = str(id)
		self.fullname.text = this_user['data']["First_Name"] + " " + this_user['data']["Last_Name"]

		if this_user['data']["Description"] is not None or this_user['data']["Description"] == '':
			self.description.size_hint_y = None
			self.description.text = this_user['data']["Description"]
		else:
			self.description.size_hint_y = 0

		self.getText(this_user)

	def get_link(self, item, service):
		if service in self._urls:
			self._urls[service] = item
			return "View {service} [ref={service}][color=800080]profile[/color][/ref]".format(
				service = service
			) if item is not None and item != '' else 'Not Provided'

	# Assigns text to the labels
	def getText(self, this_user):
		self.instagram.text = self.get_link(this_user['data']["Instagram_Link"], 'Instagram')
		self.twitter.text = self.get_link(this_user['data']["Twitter_Link"], 'Twitter')
		self.spotify.text = self.get_link(this_user['data']["Spotify_Link"], 'Spotify')
		self.linked_in.text = self.get_link(this_user['data']["LinkedIn_Link"], 'LinkedIn')

	# Opens URLs in the browser
	def urlLink(self, url, ref):
		webbrowser.open(self._urls[ref], new=1)
	
	def add_user(self, user_id):
		request = User_Requests.send_friend_request(
			user_id,
			UserStore.get('user_info')["token"]
		)
		if 'error' not in requests:
			UserStore.put('marked_request', id=user_id)
			App.get_running_app().go_screen(5)
	
	def pass_user(self, user_id):
		UserStore.put('marked_request', id=user_id)
		App.get_running_app().go_screen(5)

	def on_leave(self, *args):
		self.user_pictures.clear_widgets()
		self.tag_grid.clear_widgets()

# ------------
# User Profile Screen
# ------------
class Profile(Screen):

	_urls = {
		'Instagram':'',
		'Twitter':'',
		'Spotify':'',
		'LinkedIn':''
	}

	def on_parent(self, widget, parent):
		if UserStore.exists('current_user') == False:
			self.populate_profile()
			print('LOADING USER')

	def populate_profile(self, *args):
		
		self.user_pictures.clear_widgets()
		self.tag_grid.clear_widgets()

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

		if this_user['data']["Description"] is not None or this_user['data']["Description"] == '':
			self.description.size_hint_y = None
			self.description.text = this_user['data']["Description"]
		else:
			self.description.size_hint_y = 0

		self.getText(this_user)

		UserStore.put('current_user', data=this_user['data'])

	def get_link(self, item, service):
		if service in self._urls:
			self._urls[service] = item
			return "View {service} [ref={service}][color=800080]profile[/color][/ref]".format(
				service = service
			) if item is not None and item is not '' else 'Not Provided'

	# Assigns text to the labels
	def getText(self, this_user):
		self.instagram.text = self.get_link(this_user['data']["Instagram_Link"], 'Instagram')
		self.twitter.text = self.get_link(this_user['data']["Twitter_Link"], 'Twitter')
		self.spotify.text = self.get_link(this_user['data']["Spotify_Link"], 'Spotify')
		self.linked_in.text = self.get_link(this_user['data']["LinkedIn_Link"], 'LinkedIn')

	# Opens URLs in the browser
	def urlLink(self, url, ref):
		webbrowser.open(self._urls[ref], new=1)
	
# ------------
# Friends List and Friend Request Screens
# ------------
class FriendList(BoxLayout):
	pass

# -----
# FriendRow 
# -----
class FriendRow(ButtonBehavior, BoxLayout):
	def load_profile(self, user_id):
		UserStore.put('curr_profile', id=user_id)
		App.get_running_app().go_screen(6)

	def on_press(self):
		self.load_profile(self.id)

# -----
# FriendRecycle RecycleView
# -----
class FriendRecycle(RecycleView):

	def on_parent(self,widget,parent): 
		if not UserStore.exists('friends_loaded'):
			print('LOADING FRIENDS')
			self.populate()
	
	# FriendRecycle populate:
	def populate(self):

		friends = User_Requests.get_friends(
			UserStore.get('user_info')["id"],
			UserStore.get('user_info')["token"]
		)

		if 'error' not in friends:
			for friend in friends['data']:
				self.data.append({
					'id':str(friend["User_ID"]),
					'name': friend["First_Name"]+" "+friend["Last_Name"],
					'picture': friend['Picture_Path']
				})

		UserStore.put('friends_loaded', value=True)

# -------------
# FriendRequest Row 
# -------------
class FriendRequestRow(ButtonBehavior, BoxLayout):
	def load_profile(self, user_id):
		UserStore.put('curr_profile', id=user_id)
		App.get_running_app().go_screen(6)

	def accept_request(self, user_id):
		request = User_Requests.accept_friend_request(
			user_id,
			UserStore.get('user_info')["token"]
		)
		if 'error' not in request:
			self.delete_entry()

	def decline_request(self, user_id):
		request = User_Requests.decline_friend_request(
			user_id,
			UserStore.get('user_info')["token"]
		)
		if 'error' not in request:
			App.get_running_app().go_screen(5)

	def disable_buttons(self):
		self.accept_button.disabled = True
		self.decline_button.disabled = True

	def delete_entry(self):
		self.parent.parent.data.pop(int(self.index))

	def on_press(self):
		self.load_profile(self.id)

# ----------------
# FriendRequestRecycle RecycleView
# ----------------
class FriendRequestRecycle(RecycleView):

	def on_parent(self,widget,parent): 
		self.populate()
	
	# FriendRequestRecycle populate:
	def populate(self):

		self.data = []

		friends = User_Requests.get_friend_requests(
			UserStore.get('user_info')["id"],
			UserStore.get('user_info')["token"]
		)

		if 'error' not in friends:
			index = 0
			for friend in friends['data']:
				self.data.append({
					'id':str(friend["User_ID"]),
					'name': friend["First_Name"]+" "+friend["Last_Name"],
					'picture': friend['Picture_Path'],
					'index': str(index)
				})
				index += 1

# ------------
# EventList Screen
# ------------
class EventList(BoxLayout):
	def getText(self):
		return "[ref=Create][color=800080]Create[/color][/ref] your own event!"

# -----
# EventRow 
# -----
class EventRow(ButtonBehavior,BoxLayout):

	def load_event(self, event_id):
		UserStore.put('curr_event', id=event_id)
		App.get_running_app().go_screen(10)
	
	def on_press(self):
		self.load_event(self.id)

# ----------------
# EventRecycle RecycleView
# ----------------
class EventRecycle(RecycleView):
	def on_parent(self,widget,parent): # This function is loaded when the widget is added to the screen
		self.populate()

	def populate(self):
		events = User_Requests.get_feed(
			UserStore.get('user_info')["token"],
			limit = 100
		)

		if 'error' not in events:
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
			
			if 'error' not in event_image:
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

		if 'error' not in event:
			self.load_event(event['data']['Event_ID'])

	def load_event(self, event_id):
		UserStore.put('curr_event', id=event_id)
		App.get_running_app().go_screen(10)

	# - Clears text after leaving screen
	def on_leave(self):
		self.event_name.text = ''
		self.description.text = ''
		self.datetime.text = ''
		self.location.text = ''

# ------------
# View Event Screen
# ------------
class ViewEvent(Screen):

	_attendees = []

	def on_parent(self, widget, parent):
		if UserStore.exists('curr_event'):
			self.populate_event(id=UserStore.get('curr_event')['id'])

	def populate_event(self, id=None):
		if id is not None:
			event = Event_Requests.get(
				int(id),
				UserStore.get('user_info')["token"],
			)
			if 'error' not in event:
				self.event_img.source = event['data']['Picture_Path']
				self.event_name.text = event['data']['Name']
				self.description.text = event['data']["Description"]
				self.datetime.text = event['data']["DateTime"]
				self.location.text = event['data']["Location"]
				self.creator.text = 'Created By: {fname} {lname}'.format(
					fname = event['data']['Creator']['First_Name'],
					lname = event['data']['Creator']['Last_Name']
				)
				self._attendees = event['data']['Attendees']

	def on_leave(self, *args):
		#UserStore.delete('curr_event')
		pass

	def show_attendees(self):
		layout_popup = GridLayout(cols=1, spacing=10, size_hint_y=None)
		layout_popup.bind(minimum_height=layout_popup.setter('height'))
		

		for a in self._attendees:
			lbl = Label(
				text='{fname} {lname}'.format(
					fname = a['First_Name'],
					lname = a['Last_Name']
				), 
				size_hint_y=None)

		content_popup = ScrollView(size_hint=(1, None))
		content_popup.add_widget(layout_popup)
		popup = Popup(title='Attendees', content=content_popup, size_hint=(.75,.5))
		popup.open()

		
# ------------
# App Settings Screen
# ------------
class AppSettings(Screen):
	def on_parent(self, widget, parent):
		if UserStore.exists('current_user'):
			user_data = UserStore.get('current_user')['data']
			self.description.text = user_data['Description'] if user_data['Description'] is not None else ''
			self.twitter.text = user_data['Twitter_Link'] if user_data['Twitter_Link'] is not None else ''
			self.instagram.text = user_data['Instagram_Link'] if user_data['Instagram_Link'] is not None else ''
			self.spotify.text = user_data['Spotify_Link'] if user_data['Spotify_Link'] is not None else ''
			self.linked_in.text = user_data['LinkedIn_Link'] if user_data['LinkedIn_Link'] is not None else ''

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


	def change_profile(self):
		UserStore.delete('current_user')

		if UserStore.exists('friends_loaded'):
			UserStore.delete('friends_loaded')
			
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

		App.get_running_app().go_screen(7)

	def log_out(self):
		UserStore.delete('user_info')
		App.get_running_app().root.current = "initial_screen"

	# - Clears text after leaving screen
	def on_leave(self):
		self.description.text = ''
		self.tags.text = ''
		self.twitter.text = ''
		self.instagram.text = ''
		self.spotify.text = ''
		self.linked_in.text = ''

# ------------
# Change Password Screen
# ------------
class ChangePassword(Screen):

	def on_parent(self, widget, parent):
		get_code = User_Requests.get_change_password_code(
			UserStore.get('user_info')['token']
		)

	def check_code(self, code):
		# Comparison 
		check = User_Requests.check_change_password_code(
			UserStore.get('user_info')['token'],
			code
		)
		if 'error' not in check:
			# User only sees the 'enter new password' section if their code is correct
			self.prompt.text = "Enter your new password: "
			self.new_pass.height = dp(30)
			self.save.back_color = (192, 192, 192, 0.3)
			self.save.height = dp(30)
			self.save.text = "Save"

	def save_password(self, new_password):
		change = User_Requests.change_password(
			UserStore.get('user_info')['token'],
			new_password
		)

		if 'error' not in change:
			App.get_running_app().go_screen(7)
			Popup(
				title="Password Successfully Changed!",
				size_hint=(.5, .1)
			).open()

		# Hides the 'enter new password' section again
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
		report_reason = []

		if self.reason1.active:
			report_reason.append("Objectionable content in profile")

		if self.reason2.active:
			report_reason.append("Bullying and harassment through social media")

		if self.reason3.active:
			report_reason.append("Fake profile - student does not exist")

		if self.reason4.text != '':
			report_reason.append(self.reason4.text)

		user_reasons = '\n'.join(report_reason)
	
		report = Report_Requests.report_user(
			UserStore.get('curr_profile')['id'],
			UserStore.get('user_info')['token'],
			user_reasons
		)

		Popup(
			title="User has been reported.",
			size_hint=(.5, .1)
		).open()

	# - Clears text and sets the checkboxes to their unchecked state after leaving screen
	def on_leave(self):
		self.reason1.active = False
		self.reason2.active = False
		self.reason3.active = False
		self.reason4.text = ''


class ReportEvent(Screen):
	def save_event_report(self):
		report_reason = []

		if self.reason1.active:
			report_reason.append("Objectionable content on the event's page")

		if self.reason2.active:
			report_reason.append("Fears over the safety of the event")

		if self.reason3.active:
			report_reason.append("Fraud and deception")

		if self.reason4.text != '':
			report_reason.append(self.reason4.text)

		user_reasons = '\n'.join(report_reason)
	
		report = Report_Requests.report_event(
			UserStore.get('curr_event')['id'],
			UserStore.get('user_info')['token'],
			user_reasons
		)

		Popup(
			title="Event has been reported.",
			size_hint=(.5, .1)
		).open()

	# - Clears text and sets the checkboxes to their unchecked state after leaving screen
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
		if UserStore.exists('current_user'):
			UserStore.delete('current_user')

		if UserStore.exists('friends_loaded'):
			UserStore.delete('friends_loaded')

		if UserStore.exists('curr_profile'):
			UserStore.delete('curr_profile')

		if UserStore.exists('curr_event'):
			UserStore.delete('curr_event')

		self.screens = {} # Empty screen list
		self.available_screens = sorted([	
			'app_settings', 'change_password', 'create_event', 'eventfind', 'friends', 'match', 'match_profile', 'profile',
		'report_event', 'report_user', 'view_event']) # Explicitly sets the available screens
		self.screen_names = self.available_screens 
		curdir = dirname(__file__)
		self.available_screens = [join(curdir, 'data', 'screens', '{}.kv'.format(fn).lower()) for fn in self.available_screens] # Create a list of available screens from the kv files
		#self.go_screen(5) # goto match screen 
		
		if UserStore.exists("user_info"):
			if UserStore.get('user_info')["token"] is not None:
				query = User_Requests.login({}, auth_token=UserStore.get('user_info')["token"])
				if 'error' not in query:
					self.go_screen(5)
					self.root.current = "main"

		return self.root

	def go_screen(self, idx):
		self.index = idx # set the current screen index
		screen = self.load_screen(self.index) # build the screen kv form
		sm = self.root.ids.main.ids.sm
		sm.switch_to(screen, direction='left') # switch the screen

		# Dictionary for the titles of the app screens
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

		# Sets the label text to the corresponding screen name
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
