from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json, glob, random
from pathlib import Path
from datetime import datetime
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

Builder.load_file("design.kv")

class LoginScreen(Screen):

    def sign_up(self):
        self.manager.transition.direction = 'left'
        self.manager.current = "sign_up_screen"
        self.ids.loginWrong.text = ""
        self.ids.username.text = ""
        self.ids.password.text = ""
    
    def forgot(self):
        self.manager.transition.direction = 'left'
        self.manager.current = "forgot_password"
        self.ids.loginWrong.text = ""
        self.ids.username.text = ""
        self.ids.password.text = ""

    def loginSuccess(self, uname, pword):
        with open("users.json", 'r') as file:
            users = json.load(file)
        if uname in users and pword == users[uname]['password']:
            self.manager.transition.direction = 'left'
            self.manager.current = "login_success"
            self.ids.loginWrong.text = ""
            self.ids.username.text = ""
            self.ids.password.text = ""
        else:
            self.ids.loginWrong.text = "Wrong username or password"

class SignUpScreen(Screen):

    def add_user(self, uname, pword):
        #print(uname, pword)
        with open("users.json") as file:
            users = json.load(file)
            #print(users)
            users[uname] = {'username': uname, 'password': pword,
             'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            
        with open("users.json", 'w') as file:
            json.dump(users, file)
        self.manager.transition.direction = 'left'
        self.manager.current = "sign_up_success"
        self.ids.username.text = ""
        self.ids.password.text = ""
        
    
class SignUpSuccess(Screen):

    def goToLogin(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"

class LoginSuccess(Screen):

    def logout(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"
        self.ids.quote.text = ""
        self.ids.feeling.text = ""

    def quote(self, feel):
        feel = feel.lower()
        feelings = glob.glob("quotes/*txt")
        feelings = [Path(filename).stem for filename in feelings]
        
        if feel in feelings:
            with open(f"quotes/{feel}.txt", encoding="utf-8") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try another feeling"
                
class ForgotPassword(Screen):
    def sign_up(self):
        self.manager.transition.direction = 'left'
        self.manager.current = "sign_up_screen"

class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget() 

if __name__ == "__main__":
    MainApp().run()