Tower of Hanoi Game
===================

This is a python visualization of 
[Tower of Hanoi](https://en.wikipedia.org/wiki/Tower_of_Hanoi).
In this game, there is a stack of disks on one of three pillars. The disks are 
large at the bottom, and get smaller towards the top. The goal is to move the 
disks to a different pillar following two rules:

1. You may only move one disk at a time
2. You may never put a larger disk on top of a smaller disk

For more information, run:

    python hanoi.py help

Features include:

 * Interactive Mode (where you move the pieces with a mouse)
 * CLI Mode (where your program plays for you via stdin)
 * Ability to setp through piped-in moves
 * Customizable height
 * Decorative disk image
 * Helpful help messages
 * Occasional documentation

If you have a program that prints instructions for solving Tower of Hanoi, 
and you want to see it in action before your very eyes, now is your chance!

    python my_awesome_hanoi_solver.py | python hanoi.py -p

This program uses [pyglet](https://bitbucket.org/pyglet/pyglet/wiki/Home), which
you'll need to install (`pip install pyglet` in bash/powershell should do it)

Features may someday include:

 * Less Multithreading (I didn't know what I was doing)
 * Animation

Features do not include:

 * A program that solves Tower of Hanoi for you

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
