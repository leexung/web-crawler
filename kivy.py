from kivy.app import App
from kivy.uix.button import Button
from kivy.core.window import Window
class TestApp(App):
    def build(self):
        return Button(text='Hello World')

TestApp().run()