from time import sleep

import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics.context_instructions import Color, Logger
from kivy.graphics.vertex_instructions import Rectangle
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.tabbedpanel import TabbedPanel

import os

from Encrypt import AESCipher

kivy.require('1.10.0')
Builder.load_file(filename="layout.kv")

path = ""

class FileScreen(Screen):

    def accept(self, filename):
        # Gui().ids.filepath.text = 'File path: ' + filename[0]
        if len(filename) > 0:
            global path
            path = filename[0]
            self.manager.current = 'gui'
        # Gui().setPath(filename[0])
        # Gui().setPath()


class Gui(TabbedPanel,Screen):
    path = ''
    password = ''

    def on_enter(self, *args):
        self.ids.filepath.text = 'File path: ' + path
        print(path)
        print(os.path.dirname(os.path.abspath(path)))

    def encrypt(self):
        print(self.password)
        print(path)
        if path != '':
            cipher = AESCipher(self.password)
            cipher.encryptFile(path)



    def clear(self):
        self.ids.textinput.text = ''

    def setPassword(self):
        self.password = self.ids.textinput.text
        print(self.password)
        self.ids.labelinput.text = 'Password: ' + self.password


    # def setPath(self, path):
    #     self.path = path
    #     print('elko ' + self.path)


    def file(self):
        # self.fileChooser = fileChooser = FileChooserListView(size_hint_y=None, path='C')
        # with open(os.path.join(path, filename[0])) as f:
        #     print(f.read())
        self.manager.current = 'file'

    # def selected(self, filename):
    #     print(
    #     "selected: %s" % filename[0])
    #     print(os.path.dirname(os.path.abspath(filename)))


sm = ScreenManager()
sm.add_widget(Gui(name='gui'))
sm.add_widget(FileScreen(name='file'))

class EncryptionApp(App):

    def build(self):
        return sm

    def on_start(self):
        Window.size = (400, 400)
        self.title = 'File Encryptor'


if __name__ == '__main__':
    EncryptionApp().run()
