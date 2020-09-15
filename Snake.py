import cv2
import numpy as np
import signal
import random as rand
from pynput import keyboard
import sys

direction = 0
game_status = 1

def generate_candy():
    x = rand.randrange(6,294,6)
    y = rand.randrange(6,294,6)
    return [x,y]

candy = generate_candy()

def makeWindow():

    WINDOW = np.zeros((300,300), np.uint8)
    return WINDOW

def on_press(key):
    if key == keyboard.Key.up:
        if mysnake.direction == 180 or mysnake.direction == 0:
            mysnake.direction = 270
    elif key == keyboard.Key.right:
        if mysnake.direction == 270 or mysnake.direction == 90:
            mysnake.direction = 0
    elif key == keyboard.Key.down:
        if mysnake.direction == 0 or mysnake.direction == 180:
            mysnake.direction = 90
    elif key == keyboard.Key.left:
        if mysnake.direction == 90 or mysnake.direction == 270:
            mysnake.direction = 180


class Snake():

    def __init__(self,window):
        self.direction = 0
        self.segment_thickness = 2
        #self.headpos = (10,10)
        self._body = [[150,150]]
        self.snakelength = 4
        self._window = window
        
        for s in range(self.snakelength):
            self._body.append([self._body[0][0] -(self.segment_thickness * 3 * (s + 1)),self._body[0][1]])

        self.drawsnake(self._body,window)



    def drawsnake(self,body,window):
        st = self.segment_thickness
        stc = st

        cv2.rectangle(window,(0,0),(300,300),(0,0,0),thickness = -1)
        
        cv2.rectangle(window,(candy[0] - stc,candy[1]-stc),(candy[0]+stc,candy[1]+stc),(255,255,0), -1)

        for segment in body:
            cv2.rectangle(window,(segment[0]-st,segment[1]-st),(segment[0]+st,segment[1]+st),(255,255,255),thickness=-1)
        cv2.imshow("SNAKE",window)
        cv2.waitKey(200)

    def movesnake(self,dir):
        pop_seg = True
        st = self.segment_thickness
        stb = st + st
        global candy
        global game_status
        if dir == 0:
            xdir = 1
            ydir = 0
        elif dir == 90:
            xdir = 0
            ydir = 1
        elif dir == 180:
            xdir = -1
            ydir = 0
        elif dir == 270:
            xdir = 0
            ydir = -1

        movedbody = self._body
 
        #print(movedbody.index(movedbody[0][0],start = 1))


        

        movedbody.insert(0,[self._body[0][0] + (st * 3 * xdir),self._body[0][1] + (st * 3 * ydir)])

        try:
            index = movedbody.index(movedbody[0],1)
        except:
            pass
        else:
            game_status = -1
            

        if (movedbody[0][0] == candy[0]) and (movedbody[0][1] == candy[1]):
            candy = generate_candy()
            pop_seg = False

        if pop_seg:
            movedbody.pop(len(movedbody)-1)
        if (game_status != -1):
            self.drawsnake(movedbody,self._window)

GAME_WINDOW = makeWindow()
mysnake = Snake(GAME_WINDOW)
listener = keyboard.Listener(
    on_press=on_press)
listener.start()
while(True):
    if (game_status == 1):
        direction = 0
        game_status = 1
        candy = generate_candy()
        GAME_WINDOW = makeWindow()
        mysnake = Snake(GAME_WINDOW)
        game_status = 0
    if (game_status == 0):
        mysnake.movesnake(mysnake.direction)
    if (game_status == -1):

        cv2.putText(GAME_WINDOW,"Game Over!",(50,150),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3)
        cv2.putText(GAME_WINDOW,"Press a key to play again.",(50,170),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)
        cv2.imshow("SNAKE",GAME_WINDOW)
        cv2.waitKey(0)
        #cv2.destroyAllWindows()
        game_status = 1


