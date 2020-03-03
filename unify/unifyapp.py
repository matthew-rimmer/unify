from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout  


from os.path import dirname, join
from random import sample
from string import ascii_lowercase


class RV(BoxLayout):
    def populate(self):
        self.rv.data = [{'value': ''.join(sample(ascii_lowercase, 6))} for x in range(50)]


class UnifyScreen(Screen):
    fullscreen = BooleanProperty(False)


class UnifyApp(App):
    """Unify base kivy app

    See unify,kv for kivy widget definition
    """
    
    index = NumericProperty(-1)

    # Build creates and gets the available screens, loads them from the, 
    # the data/screens folders, sets it to the zero index screen
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
        sm = self.root.ids.sm 
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
