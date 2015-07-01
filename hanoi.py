#!/usr/bin/python
"""
USAGE: 

    python hanoi.py [OPTIONS] [-h HEIGHT]

OPTIONS:

    help, -help, --help
        Shows the program docstring (this).

    -h HEIGHT
        Set the height of the tower (in disks).

    -p
        Parse instructions from STDIN.  Each instruction must contain two numbers:
        a source, and a destination in that order.  Other characters don't matter,
        so "move 0 to 2" == "0 to 2" == "02".  Note that the pillars are numbered
        0-2 from left to right.
"""
import sys
import os
import pyglet
from pyglet.gl import *
import threading
import signal
    
height=5

def hanoi(height, callback, start, mid, end):
    """Computes Hanoi Solution Recursively
    
    Args:
    height: the height of this tower
    callback: a callback funtion for making a move
    start, mid, and end: represent the pillars"""

class EmptyTowerException(Exception):
    """Error: Tried to remove a disk from and empty pillar"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)

class InvertedTowerException(Exception):
    """Error: Placed large disk on small disk"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)

class HanoiBoard:
    """A model for the columns of a hanoi puzzle
    
    The board is represented as a tuple of pillars
    
    Each pillar is represented as a list of disks
    
    Each disk is represented as a number (it's width)"""
    def __init__(self, height):
        """Constructs a board with all disks on pillars[1]"""
        self.height = height
        self.pillars = ([],[],[])
        for i in range(height):
            self.pillars[0].append(height-i)
    def pop(self,i):
        """Take a disk off the top of pillars[i] and return it"""
        if len(self.pillars[i])>0:
            return self.pillars[i].pop()
        else:
            raise EmptyTowerException(
                "Tried to pull a disk off pillar "+str(i)+
                ", which is empty")
    def push(self, i, disk):
        """Put a disk on top of pillars[i]"""
        if len(self.pillars[i])==0 or self.pillars[i][-1]>disk:
            self.pillars[i].append(disk)
        else:
            raise InvertedTowerException(
                "Tried to put larger disk on smaller disk\n"+
                "    while moving disk of width "+str(disk)+
                " to pillar "+str(i))


def drawRect(win, color, x, y, w, h):
    verts = [ (x  , y+h),
              (x+w, y+h),
              (x  , y),
              (x+w, y)]
    glBegin(GL_TRIANGLE_STRIP)
    for idx in range(len(verts)):
        glColor3ub(*color)
        glVertex2f(*verts[idx])
    glEnd()
    glColor3ub(255,255,255)

def drawDisk(win, towerHeight, width, x, y):
    ratio = (width*1.0/towerHeight)
    iratio = 1.0-ratio
    color = (int(16+144*iratio), int(96+64*iratio), int(32+32*iratio))
    drawRect(win, color, x+128*iratio//2, y, 128*ratio,16)
    if not texture==False:
        texture.get_region(128*iratio//2,0,128*ratio,16).blit(x+128*iratio//2,y)

def drawPillar(win, pillar, height, x, y):
    drawRect(win, (32,112,196), x+60, y, 8, 20*height)
    i=0
    for disk in pillar:
        drawDisk(win, height, disk, x, y+i*20)
        i += 1

def drawBoard(win, board, x, y):
    """Draws a board with dimensions 384, 20*board.height"""
    i = 0
    for pillar in board.pillars:
        drawPillar(win, pillar, board.height, x+i*128, y)
        i += 1

def runInteractive():
    """Runs the program in interactive mode

    lets the user click and drag to move disks"""
    #'global' things are accessable from anywhere
    global texture
    global grabbed
    global height
    grabbed = 0
    window = pyglet.window.Window()
    label = pyglet.text.Label("Tower of Hanoi",
                              font_name="Times New Roman",
                              font_size=36,
                              x=window.width//2, y=window.height,
                              anchor_x="center", anchor_y="top")
    board = HanoiBoard(height)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) 
    try:
        texture = pyglet.resource.image("Sandy.png")
    except pyglet.resource.ResourceNotFoundException:
        print("Sandy.png (the decorative 128x16 image drawn over the disks) is missing.")
        texture = False
    winx = window.width//2-192

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        global grabbed
        if (winx<=x and x<winx+384 and 
            64<=y and y<64+board.height*20) and grabbed==0:
            i = (x-winx)//128
            try:
                grabbed = board.pop(i)
            except EmptyTowerException as e:
                print(str(e))

    @window.event
    def on_mouse_release(x, y, button, modifiers):
        global grabbed
        if (winx<=x and x<winx+384 and 
            64<=y and y<64+board.height*20) and not grabbed==0:
            i = (x-winx)//128
            try:
                grabbed = board.push(i, grabbed)
                grabbed = 0
            except InvertedTowerException as e:
                print(str(e))
    
    @window.event
    def on_mouse_motion(x, y, dx, dy):
        global mousex
        global mousey
        mousex = x
        mousey = y
    
    @window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        global mousex
        global mousey
        mousex = x
        mousey = y

    @window.event
    def on_draw():
        window.clear()
        label.draw()
        drawBoard(window, board, winx, 64)
        if not grabbed==0:
            drawDisk(window, board.height, grabbed, mousex-64,mousey-8)
    pyglet.app.event_loop.run()

def parseLine(text, board):
    """Parses and runs a text instruction for tower of hanoi.

    text must contain two numbers, both 0-2, that represent
    the source and destination pillars. All of the following
    are the same:

    0 to 2

    move 0 to 2

    02

    any text that does not match, or begins with #,
    will be ignored"""
    if len(text)==0 or text[0]=='#':
        return
    numbers = []
    for char in text:
        if char in "012":
            numbers.append(int(char))
    if len(numbers)==2:
        print("moving from "+str(numbers[0])+" to "+str(numbers[1]))
        disk = 0
        try:
            disk = board.pop(numbers[0])
        except EmptyTowerException as e:
            print("ERROR: Pillar "+str(numbers[0])+" is empty")
        if disk>0:
            try:
                board.push(numbers[1],disk)
            except InvertedTowerException as e:
                print("ERROR: Cannot move a big disk onto a small disk")
                board.push(numbers[0],disk)

#creates an input buffer for stdin
bufferLock=threading.Lock()
inputBuffer=[]

class StdinParser(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        global inputBuffer
        running = True
        while running:
            try:
                instruction=raw_input()
                bufferLock.acquire()
                if inputBuffer == False:
                    running = False
                else:
                    inputBuffer.insert(0,instruction)
                bufferLock.release()
            except EOFError:
                running = False
        pyglet.app.exit()

def runStdin():
    """Runs tower of hanoi using input from stdin

    this is so that a program can use the display
    (this does not work yet)"""
    global texture
    global grabbed
    global height
    grabbed = 0
    window = pyglet.window.Window()
    label = pyglet.text.Label("Tower of Hanoi",
                              font_name="Times New Roman",
                              font_size=36,
                              x=window.width//2, y=window.height,
                              anchor_x="center", anchor_y="top")
    board = HanoiBoard(height)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) 
    try:
        texture = pyglet.resource.image("Sandy.png")
    except pyglet.resource.ResourceNotFoundException:
        print("Sandy.png (the decorative 128x16 image drawn over the disks) is missing.")
        texture = False
    winx = window.width//2-192
    
    def check_for_input(dt):
        bufferLock.acquire()
        if len(inputBuffer)>0:
            instruction = inputBuffer.pop()
            parseLine(instruction,board)
        bufferLock.release()

    @window.event
    def on_draw():
        window.clear()
        label.draw()
        drawBoard(window, board, winx, 64)
    pyglet.clock.schedule_interval(check_for_input, 1)
    pyglet.app.event_loop.run()


if "help" in sys.argv or "-help" in sys.argv or "--help" in sys.argv:
    print(__doc__)
else:
    inputHeight=-1
    if "-h" in sys.argv:
        inputHeight=sys.argv.index("-h")
    if inputHeight>=0:
        height=int(sys.argv[inputHeight+1])
    if "-p" in sys.argv:
        inputThread=StdinParser()
        inputThread.start()
        runStdin()
        bufferLock.acquire()
        inputBuffer=False
        bufferLock.release()
        print("Exiting Main Thread")
    else:
        runInteractive()
