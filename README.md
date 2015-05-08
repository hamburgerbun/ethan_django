# ethan_django
Ethan written in django so people can play Ethan in a web browser

the rules of Ethan are as follows
- some N number of players begin with 5 points a piece
- players take turns in some arbitrary order of unwillingness rolling a two die
- if a player rolls a total of anything other than a four (1+3, 3+1, 2+2), add a chip to Ethan's pile
- if a player rolls a four, take all of the chips from Ethan's pile
- once a player is out of chips, he or she is out
- the game is over once all players are out of chips, or there is only one player remaining, and he or she just rolled the two die resulting in that player having more chips than Ethan's pile (namely, he or she rolled a 4 and got all of the chips, or he or she already had majority of the chips and rolled one more time).

Ethan eyes variant - same rules, except rolling a 2 (1+1) results in that player immediately losing all chips to Ethan. 

This small project will be written in 
Python 3.4
Django 1.7.5

My goal is to write Ethan completely in django with the following features:
- sqlite backend saves game information in their entirety
- games will store all information and history of actions
- games will be attached to random hex strings so ppl can continue off or whatever
- RESTful in a loose sense; there's not much going on so that shouldn't be hard
- 2 views, game setup, and the game itself
    - game setup will welcome user, ask for player count, ethan eyes option
    - game screen will show Ethan's score, the dice, player scores, move history, and win/lose conditions. 
    
I may never start or finish it but it'll happen one day. 
