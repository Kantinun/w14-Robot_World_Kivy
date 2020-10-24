from typing import Sized
from kivy.app import App
from kivy.core import window
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.window import Window

class Robot(Widget):
      def  __init__(self, ro, co, size):
        self.size = (size,size)
        self.x = Window.width/(co*2)-self.size[0]/2
        self.y = Window.height/(ro*2)-self.size[1]/2

      def draw(self):
            Rectangle(pos=(self.x,self.y),size=self.size)  
          
class World(Widget):
    def __init__(self,r, c,**kwargs):
        super().__init__(**kwargs)
        self.row = int(r)
        self.column = int(c)
        ro = Robot(self.row, self.column, 100)

        with self.canvas:
          for i in range(1,self.column+1):
            Rectangle(pos=(i*Window.width/self.column,0),size=(2,Window.height))
            
          for i in range(1,self.row+1):
            Rectangle(pos=(0,i*Window.height/self.row),size=(Window.width,2))
          
          ro.draw()          

class RobotWorld(App):
    def build(self):
        return World(4, 4)

if __name__ == "__main__":
    RobotWorld().run()
