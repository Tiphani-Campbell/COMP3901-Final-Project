from turtle import title
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivymd.toast import toast
from kivy import platform
from kivymd.uix.card import MDCard
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import sqlite3 
from datetime import date
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.screenmanager import ScreenManager
from plyer import stt
from plyer import tts
from kivy.uix.checkbox import CheckBox

class WindowManager(ScreenManager):
    Builder.load_file("screenbuild.kv")  

class Login(MDScreen):
    #enter code for verification user here
    def login_user(self):
        username = self.username.text #this is how you get text from the fields. it's self.<textfield id>.text
        password = self.password.text
        if username != "" and password != "": #edit this to check for username and password verfifcation
            con = sqlite3.connect('journaldata.db')
            curs = con.cursor()
            check = f"SELECT username FROM user WHERE username = '{username}' AND password = '{password}';"
            curs.execute(check)
            if not curs.fetchone() :
                if platform == "android":
                    toast("Please enter a valid username or password", gravity=80)# gravity=80 is to ensure it pops up at the bottom of the screen for the phone, it would pop up in the center if this wasn't here
                else:
                    toast("Please enter a valid username or password")
            else:
                self.manager.transition.direction = "left"
                self.manager.current = "dashboard"  
                


            con.commit()
            con.close()

                
        else:# this section is to display an invalid message for a short period of time at the bottom of the screen
            if platform == "android":
                toast("Please fill all fields", gravity=80)# gravity=80 is to ensure it pops up at the bottom of the screen for the phone, it would pop up in the center if this wasn't here
            else:
                toast("Please fill all fields")


    
   

class Signup(MDScreen):
    #enter code for saving user
    #Required fields are set on the page so check if they're empty and do the toast thing I did in the login class for any errors
    #Ensure, when you are using the toast method to flash a message on the screen, to test for the platfrom being android, the else was for it to display on the laptop
    def signup_user(self):
        uname = self.ids.name.text
        username = self.ids.username.text
        password = self.ids.password.text
        confirm = self.ids.confirmpass.text
        if uname != "" and username != "" and password != "" and confirm != "" :
            if password == confirm:
                con = sqlite3.connect('journaldata.db')
                curs = con.cursor()
                curs.execute("INSERT INTO user VALUES(:name, :username, :password)",
                    {
                        'name' : uname,
                        'username': username,
                        'password': password
                    }
                )
               
 

                con.commit()
                con.close()

                self.manager.transition.direction = "right" #anything with self.manager is responsible for changing the screen
                self.manager.current = "login"
            else:
                if platform == "android":
                    toast("Not the same password! Please try again", gravity=80)
                else:
                    toast("Not the same password! Please try again")
       
        else:
            if platform == "android":
                toast("Please fill all fields", gravity=80)
            else:
                toast("Please fill all fields")
       

class Dashboard(MDScreen):
    #edit this section to generate the recommended plans from the database.
    def on_enter(self):
        for i in range(0,10):
            self.ids.reclist.add_widget(RecommendedPlans(plan_title='Plan', exercises='8 exercises'))
    

class Journal(MDScreen):
    #edit this function to receive the list of entry records from the query
    #firstly check if the person has any journal entries and if they do run the for loop(to the amount of entries they have)
    #the text variable will store the title and date of the entry
    def on_enter(self):
        con = sqlite3.connect('journaldata.db')
        curs = con.cursor()
        check = f"SELECT COUNT (*) FROM journalentries;"
        numentries = curs.execute(check)
        if numentries != 0:
            curs.execute("SELECT * FROM journalentries")
            entries = curs.fetchall()


            self.ids.entrylist.clear_widgets()
     
            for entry in entries:
                self.ids.entrylist.add_widget(
                    Entry(text=entry[2], text1=entry[0])
                )
     
                    

        con.commit()
        con.close()
               
                     

class JournalEntry(MDScreen):
    #add code to save entry
    def save(self):
        title = self.ids.title.text
        entry = self.ids.entry.text
        con = sqlite3.connect('journaldata.db')
        curs = con.cursor()
        curs.execute("INSERT INTO journalentries VALUES (:title, :entry, :date) ",
        {
            'title' : title,
            'entry' : entry,
            'date': date.today()

        }
        )

        self.ids.title.text = ''
        self.ids.entry.text = ''


        con.commit()
        con.close()
        self.manager.transition.direction = "right"
        self.manager.current = "journal"
        

class ChatBot(MDScreen):
    
    #start=0
    #def com_talk(self,message):
       # speak = wincl.Dispatch("SAPI.SpVoice")
        #speak.Speak(message)

    def on_enter(self):
        self.ids.chatbox.clear_widgets()
        mess='Hello! How are you doing?'
        tts.speak(message=mess)
        self.ids.chatbox.add_widget(Response(text=mess))
        
    #add code to listen and respond to a user here
    #there's a label that says tap to speak, change it when to 'Listening' when the app is waiting for input,
    #change it to 'Speaking' when the app is speaking
    def talk(self):
        pass
        '''
        usermess=self.ids.usertext.text
        size=0

        if len(usermess)<=6:
            size = 0.08
        if len(usermess)<=14:
            size = 0.22 
        else:
            size = 0.4

        
        speak = wincl.Dispatch("SAPI.SpVoice")
        self.ids.chatbox.add_widget(UserMessage(text=usermess, size_hint_x = size))
     
        self.com_talk(usermess) 
        
        say_this= "What else?" 
        self.ids.chatbox.add_widget(Response(text=say_this))

        self.com_talk(say_this)

        self.ids.usertext.text = ""
        '''

class Progress(MDScreen):
    pass

class ChosenPlan(MDScreen):
    #edit this section to show all chosen plans
    def on_enter(self):
        for i in range(0,12):
            self.ids.aclist.add_widget(ActivePlans(plan_title='Plan', exercises='8 exercises'))
        pass

class Entry(BoxLayout):
    text = StringProperty()
    text1 = StringProperty()
    
    def open_menu(self):
        self.menu_list=[
            {
                "text": "View Entry",
                "viewclass":"OneLineListItem",
                "on_release": lambda x = "View":self.viewentry()
            },
            {
                "text" : "Delete Entry",
                "viewclass": "OneLineListItem",
                "on_release": lambda x = "Delete" :self.deleteentry()
            }
        ]

        
        self.menu = MDDropdownMenu(
            caller =self.ids.menubutton,
            items = self.menu_list,
            width_mult = 2
        )
        self.menu.open()

    #works now, so edit this to view entry
    def viewentry(self):
        MDApp.get_running_app().screen_manager.transition.direction = "left"
        MDApp.get_running_app().screen_manager.current = "journalentry"
        MDApp.get_running_app().screen_manager.get_screen("journalentry").ids.title.text = "Blue"
        MDApp.get_running_app().screen_manager.get_screen("journalentry").ids.entry.text = "Grape"
        self.menu.dismiss()
        
    
    #put code here to delete an entry
    def deleteentry(self):
        title = self.ids.title.text
        date = self.ids.date.text
        entry = Entry(text=date, text1=title)
        con = sqlite3.connect('journaldata.db')
        curs = con.cursor()
        task= "DELETE FROM journalentries WHERE title=?"
        curs.execute(task, (title,))
        
        con.commit()
        con.close()
        MDApp.get_running_app().screen_manager.get_screen("journal").remove_widget(entry)

        con = sqlite3.connect('journaldata.db')
        curs = con.cursor()
        check = f"SELECT COUNT (*) FROM journalentries;"
        numentries = curs.execute(check)
        if numentries != 0:
            curs.execute("SELECT * FROM journalentries")
            entries = curs.fetchall()


            MDApp.get_running_app().screen_manager.get_screen("journal").ids.entrylist.clear_widgets()
     
            for entry in entries:
                MDApp.get_running_app().screen_manager.get_screen("journal").ids.entrylist.add_widget(
                    Entry(text=entry[2], text1=entry[0])
                )           

        con.commit()
        con.close()
        self.menu.dismiss()


        
        
class UserMessage(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    

class Response(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()

class RecommendedPlans(MDCard):
    plan_title = StringProperty()
    exercises = StringProperty() #number of exercises

    #write code here to choose a plan
    def choose_plan(self):
        MDApp.get_running_app().screen_manager.transition.direction = "left"
        MDApp.get_running_app().screen_manager.current = "plans"
        
    

class ActivePlans(MDCard):
    plan_title = StringProperty() 
    exercises = StringProperty() #number of exercises

    #write code here to delete a plan, the steps are similar to deleting a journal entry
    def delete_plan(self):
        pass
    
    def view_exercises(self):
        MDApp.get_running_app().screen_manager.transition.direction = "left"
        MDApp.get_running_app().screen_manager.current = "progress"
        

class SmallStepsApp(MDApp):
    def build(self):
        con = sqlite3.connect('journaldata.db')
        curs = con.cursor()
        curs.execute("""CREATE TABLE if not exists user (name text, username text, password text)""")
        curs.execute("""CREATE TABLE if not exists journalentries (title text, entry text, date text)""")
        curs.execute("""CREATE TABLE if not exists journal (title text, entry text, date text)""")

        
        con.commit()
        con.close()

        self.screen_manager = WindowManager()
        

        return self.screen_manager

if __name__ == "__main__":
    SmallStepsApp().run()
