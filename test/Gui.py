import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.tabbedpanel import TabbedPanel

import os

from encryption.Encrypt import AESCipher


Builder.load_file(filename="layout.kv")

data = {
    'dirEnc': os.path.abspath(''),
    'dirDec': os.path.abspath(''),
    'passwordEnc': 'password',
    'passwordDec': 'password',
    'fChooserEnc': '',
    'fChooserDec': '',
    'pathEnc': '',
    'pathDec': '',
    'window': 'enc'
}


class FileScreen(Screen):

    def on_enter(self, *args):
        if data['window'] == 'enc':
            self.ids.filechooser.filters = ['*', '!.rar']
            self.ids.filechooser.path = data['dirEnc']
            self.ids.pathinput.text = data['dirEnc']
            if data['fChooserEnc'] != '':
                self.ids.labelchooser.text = data['fChooserEnc']
            if data['pathEnc'] != '':
                self.ids.filechooser.path = data['pathEnc']
        else:
            self.ids.filechooser.filters = ['*.enc']
            self.ids.filechooser.path = data['dirDec']
            self.ids.pathinput.text = data['dirDec']
            if data['fChooserDec'] != '':
                self.ids.labelchooser.text = data['fChooserDec']
            if data['pathDec'] != '':
                self.ids.filechooser.path = data['pathDec']

    def accept(self):
        if len(self.ids.labelchooser.text) > 0:
            if data['window'] == 'enc':
                data['pathEnc'] = self.ids.labelchooser.text
            else:
                data['pathDec'] = self.ids.labelchooser.text
            self.manager.current = 'gui'
            Window.size = (400, 300)

    def back(self):
        self.manager.current = 'gui'
        Window.size = (400, 300)

    def selected(self, filename):
        if len(filename) > 0 and not os.path.isdir(filename[0]):
            if data['window'] == 'enc':
                data['fChooserEnc'] = str(filename[0])
                self.ids.labelchooser.text = data['fChooserEnc']
            else:
                data['fChooserDec'] = str(filename[0])
                self.ids.labelchooser.text = data['fChooserDec']

    def setFileChooser(self, choosePath):
        if data['window'] == 'enc':
            data['pathEnc'] = choosePath
            self.ids.filechooser.path = data['pathEnc']
        else:
            data['pathDec'] = choosePath
            self.ids.filechooser.path = data['pathDec']


class Gui(TabbedPanel, Screen):

    def on_enter(self, *args):
        if data['window'] == 'enc':
            self.ids.filepath.text = os.path.basename(data['fChooserEnc'])
        else:
            self.ids.filepathdecrypt.text = os.path.basename(data['fChooserDec'])

    def changeCrypt(self):
        if data['window'] == 'enc':
            data['window'] = 'dec'
        else:
            data['window'] = 'enc'

    def encrypt(self):
        if data['pathEnc'] != '':
            cipher = AESCipher(data['passwordEnc'])
            cipher.encryptFile(data['pathEnc'])

    def decrypt(self):
        if data['pathDec'] != '':
            cipher = AESCipher(data['passwordDec'])
            cipher.decryptFile(data['pathDec'])

    def clear(self):
        self.ids.textinput.text = ''

    def clearDecrypt(self):
        self.ids.textinputdecrypt.text = ''

    def setPassword(self):
        data['passwordEnc'] = self.ids.textinput.text
        self.ids.labelinput.text = data['passwordEnc']

    def setPasswordDecrypt(self):
        data['passwordDec'] = self.ids.textinputdecrypt.text
        self.ids.labelinputdecrypt.text = data['passwordDec']
        self.ids.textinputdecrypt.text = 'Enter PASS'

    def file(self):
        self.manager.current = 'file'
        Window.size = (500, 600)


sm = ScreenManager()
sm.add_widget(Gui(name='gui'))
sm.add_widget(FileScreen(name='file'))


class EncryptionApp(App):

    def build(self):
        return sm

    def on_start(self):
        Window.size = (400, 300)
        self.title = 'File Encryptor'


if __name__ == '__main__':
    EncryptionApp().run()
