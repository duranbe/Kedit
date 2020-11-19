import kivy
import os

kivy.require('1.10.0')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.codeinput import CodeInput
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty


class CurrentObject(object): # We manage the open file  as an object
    def __init__(self,co_name,co_path):
        self.co_name = co_name
        self.co_path = co_path

CO = CurrentObject('','')

class OpenInterface(FloatLayout): # Interface to browse folders
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    defpath = "C:\\Users"
class SaveInterface(FloatLayout): # Interface to save in special path
    save = ObjectProperty(None)
    text_input2 = ObjectProperty(None)
    cancel = ObjectProperty(None)

class ErrorInterface(FloatLayout): # Interface if an error occured
    error_string = ObjectProperty(None) # Text 
    close = ObjectProperty(None) # Close button


class Screen(BoxLayout): # Main view
    cinput = ObjectProperty(None)
    Path = ObjectProperty(None)

    def dismiss_popup2(self):
        self.popup2.dismiss()
    
    def dismiss_popup(self):
        self._popup.dismiss()
    
    def error_popup(self,err_text):
        content = ErrorInterface(error_string=err_text,close=self.dismiss_popup2)
        self.popup2 = Popup(title="Error", content=content,size_hint=(0.9, 0.9))
        self.popup2.open()
    
    def open_popup(self):
        content = OpenInterface(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()
    
    def load(self, path, filename):
        try:
       
            with open(os.path.join(path, filename[0])) as stream:
            
                self.cinput.text = stream.read()
                self.Path=os.path.join(path, filename[0])
                CO.co_name=filename[0]
                CO.co_path=path
            self.dismiss_popup()
        except:
            self.error_popup("Error")

    
    def save_popup(self): # Save as
        content = SaveInterface(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,size_hint=(0.9, 0.9))
        self._popup.open()
    
    def save(self, path, filename): 
        try: 
            with open(os.path.join(path, filename), 'w') as stream:
                stream.write(self.cinput.text)

            self.dismiss_popup()
        except PermissionError:
            self.error_popup("Cannot save here")
            
        except FileNotFoundError:
            self.error_popup("File not found ")
            

    def saving(self,text): # Fast save
        if CO.co_name != "":
            fichier = open(CO.co_name, "w") 
            fichier.write(text)
            fichier.close()
            
    
    def execute(self,text):
        if CO.co_name != '':
            print(">>>Start>>>")  
            fichier = open(CO.co_name, "w") 
            fichier.write(text)
            fichier.close()
            debug = "py " + CO.co_name
            os.system(debug)
            print("<<<End<<")
    
    
class KeditApp(App):
    def build(self):
        return Screen()

Factory.register('OpenInterface', cls=OpenInterface)
Factory.register('SaveInterface', cls=SaveInterface)
Factory.register('ErrorInterface', cls=ErrorInterface)

KeditApp().run()