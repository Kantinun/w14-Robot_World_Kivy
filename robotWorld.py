from random import randint
from kivy.app import App
from kivy.core import window
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
import random

class Robot(Widget):
      def  __init__(self, ro, co, size):
        self.size = (size,size)
        self.x = Window.width/(co*2)-self.size[0]/2
        self.y = Window.height/(ro*2)-self.size[1]/2
        self.angle = 0
        self.velX = Window.width/co
        self.velY = Window.height/ro

      def draw(self):
          self.robot = Rectangle(pos=(self.x,self.y),size=self.size)  
      
      def move(self):
        if self.angle==0 :
          self.y += self.velY
        if abs(self.angle)==180:
          self.y-=self.velY
        if self.angle == 270 or self.angle==-90:
          self.x+=self.velX
        if self.angle == 90 or self.angle ==-270:
          self.x-=self.velX
      
      def turnLeft(self):
        self.angle += 90
        if self.angle>=360:
            self.angle =0;
      
      def turnRight(self):
        self.angle -= 90
        if self.angle<= -360:
            self.angle =0;
        
class Target(Widget):
    def __init__(self, ro, co, size):
        self.size = (size, size)
        self.column = co
        self.row = ro
        self.x = randint(1,co-1)*Window.width/(co)-self.size[0]/2+Window.width/(co*2)
        self.y = randint(1,ro-1)*Window.height/(ro)-self.size[1]/2+Window.height/(ro*2)
    
    def draw(self):
          self.target = Rectangle(pos=(self.x,self.y),size = self.size)
    
    def randomPosition(self):
          self.x = randint(1,self.column-1)*Window.width/(self.column)-self.size[0]/2+Window.width/(self.column*2)
          self.y = randint(1,self.row-1)*Window.height/(self.row)-self.size[1]/2+Window.height/(self.row*2)

class World(Widget):
    def __init__(self,r, c,**kwargs):
        super().__init__(**kwargs)
        self.row = int(r)
        self.column = int(c)
        self.ro = Robot(self.row, self.column, 100)
        self.tar = Target(self.row, self.column, 70)
        self.input = InputProcessor("w","a","d")
        self.keyboard = Window.request_keyboard(self.on_key_closed,self)
        self.keyboard.bind(on_key_down=self.on_Key_Down)
        self.keyboard.bind(on_key_up=self.on_Key_up)

        self.keyPressed = set()

        with self.canvas:
          for i in range(1,self.column+1):
            Rectangle(pos=(i*Window.width/self.column,0),size=(2,Window.height))
            
          for i in range(1,self.row+1):
            Rectangle(pos=(0,i*Window.height/self.row),size=(Window.width,2))
          print(self.ro.pos)
          self.ro.draw()
          self.tar.draw()
          
    def on_key_closed(self):
        self.keyboard.unbind(on_key_down=self.on_Key_Down)
        self.keyboard.unbind(on_key_up=self.on_Key_up)
        self.keyboard = None
    
    def on_Key_Down(self, keyboard, keycode, text, modifiers):
        self.keyPressed.add(text)
        self.input.robotMove(self.ro, self.keyPressed)
        self.update()
                   

    def on_Key_up(self, keyboard, keycode):
        text = keycode[1]
        if text in self.keyPressed:
            self.keyPressed.remove(text)
    
    def collides(self, e1, e2):
        r1x = e1.pos[0]
        r1y = e1.pos[1]
        r2x = e2.pos[0]
        r2y = e2.pos[1]
        r1w = e1.size[0]
        r1h = e1.size[1]
        r2w = e2.size[0]
        r2h = e2.size[1]

        if (r1x < r2x + r2w and r1x + r1w > r2x and r1y < r2y + r2h and r1y + r1h > r2y):
            return True
        else:
            return False

    def update(self):
          while(self.collides(self.ro.robot, self.tar.target)):
              self.tar.randomPosition()
              self.tar.target.pos = (self.tar.x, self.tar.y)    
          
class InputProcessor(Widget):
    def __init__(self, fKey, lKey, rKey):
        self.forward = str(fKey)
        self.left = str(lKey)
        self.r = str(rKey)
    
    def robotMove(self, robot, keyList):
        if self.left in keyList:
            robot.turnLeft()
            
        if self.r in keyList:
            robot.turnRight()

        if self.forward in keyList:
            robot.move()
            if robot.y <= Window.height/8-robot.size[1]/2:
                robot.y = Window.height/8-robot.size[1]/2
            if robot.y >= 7*Window.height/8-robot.size[1]/2:
                robot.y= 7*Window.height/8-robot.size[1]/2   
            if robot.x <= Window.width/8-robot.size[0]/2:
                robot.x = Window.width/8-robot.size[0]/2
            if robot.x >= 7*Window.width/8-robot.size[0]/2:
                robot.x = 7*Window.width/8-robot.size[0]/2  

            robot.robot.pos = (robot.x, robot.y)     
    
class RobotWorld(App):
    def build(self):
          return World(4, 4)

if __name__ == "__main__":
    RobotWorld().run()
