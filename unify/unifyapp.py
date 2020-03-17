from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout  


from os.path import dirname, join
from random import sample
from string import ascii_lowercase
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image


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


#Initial page shown when app is first downloaded
class Initial(Screen):
    pass


# Login class
class Login(Screen):
    pass


# Register class
class Register(Screen):
    pass


# ProfileCreation class
class ProfileCreation(Screen):
    pass


# Class for the profile, find & message sections
class MainSections(Screen):
    pass


class RV(BoxLayout):
    def populate(self):
        self.rv.data = [{'value': ''.join(sample(ascii_lowercase, 6))} for x in range(50)]
        p = ProfilePayload(j)
        self.rv.data.append({'value' : p.data["First_Name"]}) 

class UnifyScreen(Screen):
    fullscreen = BooleanProperty(False)
    
    
# Profile class
class Profile(Screen):
    pass


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
            'message','match','profile']) # Explicitly sets the available screens
        self.screen_names = self.available_screens 
        curdir = dirname(__file__)
        self.available_screens = [join(curdir, 'data', 'screens', '{}.kv'.format(fn).lower()) for fn in self.available_screens] # Create a list of available screens from the kv files
        self.go_screen(0) # goto screen 0
        
        #print(len(self.available_screens))
        
        return self.root

    def go_screen(self, idx):
        self.index = idx # set the current screen index
        screen = self.load_screen(self.index) # build the screen kv form
        sm = self.root.ids.main.ids.sm
        sm.switch_to(screen, direction='left') # switch the screen
        #self.populate()
        
    
    def load_screen(self, index):
        # print('loading screen')
        if index in self.screens:
                return self.screens[index]
        screen = Builder.load_file(self.available_screens[index]) # build the screen
        return screen




# main
if __name__ == '__main__':
        UnifyApp().run()
