Tower of Hanoi Game
===================

This is a python visualization of 
[Tower of Hanoi](https://en.wikipedia.org/wiki/Tower_of_Hanoi).

This program does not solve the Tower of hanoi problem, but it will:

 * Let you play the game with a mouse
 * Test your Tower of Hanoi solving program

For details:

    python hanoi.py help

This program uses [pyglet](https://bitbucket.org/pyglet/pyglet/wiki/Home), which
you'll need to install (`pip install pyglet` in bash/powershell should do it)

**Features include:**

 * Interactive Mode (where you move the pieces with a mouse)
 * CLI Mode (where your program plays for you via stdin)
 * Ability to setp through piped-in moves
 * Customizable height
 * Decorative disk image
 * Helpful help messages
 * Documentation

**Features may someday include:**

 * Less Multithreading (I didn't know what I was doing)
 * Animation

**Features do not include:**

 * A program that solves Tower of Hanoi for you


Play as a Human:
----------------

If you want to play the game as a human:

    python hanoi.py

If you want to change the height of the tower to 3 (5 by default):

    python hanoi.py -h 3

Test a Tower of Hanoi solving Program:
--------------------------------------

Your program will need to print solution instructions line by line.
Each instruction must contain two numbers: a source, and a
destination in that order.  Other characters don't matter,
so "move 0 to 2" == "0 to 2" == "02".  Note that the pillars are numbered
0-2 from left to right.

Example output for solving `python hanoi.py -h 2`:

    0 1
    0 2
    1 2

If you want to see an animated test of your Tower of Hanoi solver:

    python solver.py | hanoi.py -p

If you want to make it spend 2.5 seconds on each move (1 sec by default):

    python solver.py | hanoi.py -p -t 2.5

If you want to move on each key press:

    python solver.py | hanoi.py -p -d

Note that you'll get a warning if you try to run a test that will take more than a minute:

    python solver.py 12 | hanoi.py -p -h 12
    Aboriting. This may take over 4095 seconds to complete. Use -f to run anyway.
    
But you can bypass this warning by adding `-f`:

    python solver.py 12 | hanoi.py -p -h 12 -f
    moving from 0 to 1
    moving from 0 to 2
    ...

BUT WHY!?
---------

I'm mostly making this as an educational tool. When I learned recursion, I was
told to make a fibonacci function, and was forbade from using loops for a few
months. As a result, recursion  (outside of tree traversal) looked like a 
stupid, inefficient technique used by those who congradulate themselves for 
cryptic coding that newbies might not understand.

Then I learned about the Tower of Hanoi, and saw that it only made sense to
solve it recursively.  Immediately, recursion went from a stupid (yet somehow
elitist) idea, to a technique that was elegant and important.

Because of this, when teaching other people about recursion, I want to use
Tower of Hanoi as an illustration.  The problem is, Tower of Hanoi is
harder to explain than

    F(0)=1
    F(1)=1
    F(n)=F(n-1)+F(n-2)

The program in this repository is my attempt to overcome that problem.
