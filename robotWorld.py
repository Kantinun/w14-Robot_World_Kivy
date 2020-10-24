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
        self.angle = 0
        self.velX = Window.width/co
        self.velY = Window.height/ro

      def draw(self):
          self.robot = Rectangle(pos=(self.x,self.y),size=self.size)  
      
      def move(self):
        if abs(self.angle)==360:
          self.angle =0;
        if self.angle==0:
          self.y += self.velY
        if abs(self.angle)==180:
          self.y-=self.velY
        if self.angle == 270 or self.angle==-90:
          self.x+=self.velX
        if self.angle == 90 or self.angle ==-270:
          self.x-=self.velX
      
      def turnLeft(self):
        self.angle += 90
      
      def turnRight(self):
        self.angle -= 90
        
      
      
class World(Widget):
    def __init__(self,r, c,**kwargs):
        super().__init__(**kwargs)
        self.row = int(r)
        self.column = int(c)
        self.ro = Robot(self.row, self.column, 100)
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
          
          self.ro.draw()

    def on_key_closed(self):
        self.keyboard.unbind(on_key_down=self.on_Key_Down)
        self.keyboard.unbind(on_key_up=self.on_Key_up)
        self.keyboard = None
    
    def on_Key_Down(self, keyboard, keycode, text, modifiers):
        self.keyPressed.add(text)
        self.input.robotMove(self.ro, self.keyPressed)
                   

    def on_Key_up(self, keyboard, keycode):
        text = keycode[1]
        if text in self.keyPressed:
            self.keyPressed.remove(text)

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
