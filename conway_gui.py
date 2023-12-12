#!/usr/bin/python3

from kivy.app import App
import kivy
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.graphics import Line
from kivy.core.window import Window
from kivy.config import Config
from kivy.clock import Clock
from kivy.graphics import *
from conway import *

kivy.config.Config.set('graphics','resizable', False)


class SetupScreen(Screen):
    def __init__(self, **kwargs):
        super(SetupScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=40)
        self.input_text = TextInput(hint_text='Entrez une valeur', multiline=False, halign='center', size_hint_y=None, height=40)
        layout.add_widget(self.input_text)
        button = Button(text='Suivant', on_press=self.switch_to_second_screen, size_hint_y=None, height=40)
        layout.add_widget(button)
        self.add_widget(layout)

    def switch_to_second_screen(self, instance):
        # Récupérer la valeur de l'input
        input_value = self.input_text.text

        # Accéder au ScreenManager et changer d'écran avec une animation de slide
        app = App.get_running_app()
        app.root.transition = SlideTransition(direction='left')
        
        # Passer la valeur au deuxième écran
        app.root.get_screen('main_screen').dim = int(input_value)

        app.root.current = 'main_screen'

class MainScreen(Screen):
    def __init__(self,**kwargs):
        super(MainScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.drawing_area = Widget()
        layout.add_widget(self.drawing_area)
        self.add_widget(layout)

        self.game = None

    def draw_grid(self):
        self.drawing_area.canvas.clear()
        cell_size = 800/self.dim  
        line_width = 1  

        top_left = {'x':100,'y':900}
        bottom_left = {'x':100,'y':100}
        top_right = {'x':900,'y':900}
        bottom_right = {'x':900,'y':100}

        with self.drawing_area.canvas:

            #lignes qui délimitent
            Line(points=[bottom_left['x'], bottom_left['y'], bottom_right['x'], bottom_right['y']], width=2)
            Line(points=[top_left['x'], top_left['y'], top_right['x'], top_right['y']], width=2)
            Line(points=[top_left['x'], top_left['y'], bottom_left['x'], bottom_left['y']], width=2)
            Line(points=[top_right['x'], top_right['y'], bottom_right['x'], bottom_right['y']], width=2)
            
            #on dessine les lignes
            for i in range(1,self.dim):
                Line(points=[bottom_left['x'], bottom_left['y']+i*cell_size, bottom_right['x'], bottom_right['y']+i*cell_size], width=2)

            #et puis les colonnes
            for j in range(0,self.dim):
                x1 = top_left['x']+j*cell_size
                y1 = top_left['y']
                x2 = bottom_left['x']+j*cell_size
                y2 = bottom_left['y']
                Line(points=[x1,y1,x2,y2], width=2)

            Color(1., 0, 0)


            current_table = self.game.table
            for i in range(len(current_table)):
                for j in range(len(current_table[i])):
                    if current_table[i][j] == '1':
                        Color(1, 0, 0)  # Couleur des cellules
                        Rectangle(pos=(top_left['x'] + (j-1) * cell_size, top_left['y'] - i * cell_size), size=(cell_size, cell_size))

                        
    

    def update(self, dt):
        self.game.update()
        self.draw_grid()

    def start_update_loop(self):
        Clock.schedule_interval(self.update, 0.2)

    def on_enter(self):
        # on initialise le jeu
        self.game = Conway(self.dim)
        self.game.print_mat()


        self.start_update_loop()

class Conway_GUI(App):
    def build(self):
        # Créer un ScreenManager
        Window.size = (1000,1000)
        sm = ScreenManager()

        # Ajouter les écrans au ScreenManager
        sm.add_widget(SetupScreen(name='setup_screen'))
        sm.add_widget(MainScreen(name='main_screen'))

        return sm

if __name__ == '__main__':
    Conway_GUI().run()
