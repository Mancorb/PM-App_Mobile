from kivy.app import App
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen,NoTransition

Config.set('graphics', 'width', '300')


class Creator(Screen):
    pass


#stuff for login page
class LoginLayout(Screen):
    #user input password
    key = ObjectProperty(None)

    def __init__(self, **kw):
        super(LoginLayout,self).__init__(**kw)

    def obtainPass (self):
        keyPass = self.key.text
        if len(keyPass) >0:
            self.changeScreen()
    
    def changeScreen(self):
        if self.manager.current == "loginPage":
            self.manager.current = "createPage"
        else:
            self.manager.current = "loginPage"

#Declare Screens
class Manager(ScreenManager):
    loginScreen = ObjectProperty(None)
    createScreen = ObjectProperty(None)

#Builder
class PassManager(App):
    def build(self):
        m = Manager(transition = NoTransition())
        return m

if __name__ == '__main__':
   app =PassManager()
   app.run()