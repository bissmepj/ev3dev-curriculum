#Create a program that plays the game "Plinko" with the EV3 robot.
#The robot will 'fall' down a series of white pieces of paper randomly.
#This will be accomplished by creating an array of left and right moves that EV3 can do,
#but the user will select n number of terms to determine which moves are called
#and guess where EV3 will end up.  If the value in the 'x' array is more or less than
#a certain 'if' value, then EV3 will turn left or right based on the condition.  This should
#create a truly 'random' experience for the user.  To further the randomization, the numbers will
#be shuffled before executing the "Plinko" game. If the user wins, then a display will
#tell them that they have won.  If they lose, then the display will tell them
#they have lost.  EV3 will joke during the game.

#Goals:
#   Create a truly 'random' experience if possible.
#   Create a fun atmosphere with Snatch3r's charm.
#   Create an aesthetically pleasing interface.

import random

#def plinko (x, ):
