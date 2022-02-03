# Author: Mark McCarthy
# Date: 12-21-2021
# This program is an implementation of the classic game 
# Aggrivation for running statistical analysis of the 
# gameplay.#


import random as rd
from numpy import mod
import matplotlib

##########################################################

#####################GAME CLASSES#########################

#############################################################

class __Game_obj(object):
    
    #Game obj Variables 
    _game_board = []
    _win = False
    _colors = ['y','g','w','b','p','o']
    num_players = int(input('How many players: '))
    _player_list = []
    _num_turns = 0


    #Game obj constructor inits the board and a list of players 
    #depending on input from user for num of players.
    def __init__(self):
        self._player_list = make_players(self, self.num_players)

        #shortcut is at 8th index in each 14 space section
        for elt in range(len(self._colors)):
            temp = space(self._colors[elt])
            temp2 = space(self._colors[elt],True)
            counter = 0
            for i in range(14):
                if counter == 7:
                    self._game_board.append(temp2)
                else:
                    self._game_board.append(temp)
                counter += 1 
        super().__init__()



    #setter for all attributes
    def __setattr__(self, __name: str, __value) -> None:
        return super().__setattr__(__name, __value)

    #attribute getter
    def __getattribute__(self, name):
        return object.__getattribute__(self,name)


#make and return a list of the # of players needed.
def make_players(self, num_players):
    player_list = []
    for elt in range(num_players):
        temp_color = self._colors[elt]
        temp = __player(temp_color)
        player_list.append(temp)
    return player_list

#------------------------------------------------

class space(object):
    
    #variables
    _color = ''
    _occupied = ''
    _shortcut = False

    #base ctor
    def __init__(self,a):
        self._color = a

    #ctor for shortcut space
    def __init__(self,a,short = False):
        self._color = a
        self._shortcut = short

    #setter for all attributes
    def __setattr__(self, __name: str, __value) -> None:
        return super().__setattr__(__name, __value)

    #attribute getter
    def __getattribute__(self, name):
        return object.__getattribute__(self,name)

#------------------------------------------------

class super_short(object):
    
    #variables
    _occupied = False
    _color = ''

    #ctor
    def __init__(self,a):
        self._color = a
        super().__init__()

    #setter for all attributes
    def __setattr__(self, __name: str, __value) -> None:
        return super().__setattr__(__name, __value)

    #attribute getter
    def __getattribute__(self, name):
        return object.__getattribute__(self,name)

#------------------------------------------------

class __player(object):

    _color = ''
    _base = []
    _home = [0]*4
    _num_marbles_out = -1

    def __init__(self,a) -> None:
        self._color = a
        fill_base(self,a)
        super().__init__()

    #setter for all attributes
    def __setattr__(self, __name: str, __value) -> None:
        return super().__setattr__(__name, __value)

    #attribute getter
    def __getattribute__(self, name):
        return object.__getattribute__(self,name) 

    def describe(self):
        print("color = " + self._color)
        print_base(self)
        print("Home: ", self._home)
        print("num marbles out = ", self._num_marbles_out)

    def marbles_out(self):
        print("num marbles out for " + self._color + " = ", self._num_marbles_out + 1)

def print_base(player):
    for marble in player._base:
        print(marble._color + " marble at: ", marble._location)
        
#Method is passed a player obj and fills the base with marbles
def fill_base(player,a):
    player._base = [__marble(a)]*4


#------------------------------------------------

class __marble(object):

    #variables
    _color = ''
    _location = 0

    def __init__(self,a) -> None:
        self._color = a
        super().__init__()

       #setter for all attributes
    def __setattr__(self, __name: str, __value) -> None:
        return super().__setattr__(__name, __value)

    #attribute getter
    def __getattribute__(self, name):
        return object.__getattribute__(self,name) 
    
    #update location of the marble
    def update_loc(self, roll):
        self._location += (roll-1)


#############################################################

####################GAME BOARD METHODS#######################

#############################################################

#------------------------------------------
def roll_die():
    roll = rd.randint(1,6)
    return roll
#------------------------------------------


#------------------------------------------
def update_board(game,roll,player):

    #reassign player to reference the space in the player list 
    curr_player = player

    #check game condition variables
    ##function checks if new marble can be played 
    _new_marble_flag = check_new_marble(player)

    #udpdate the board with a new marble if available
    if (roll == 1 or roll == 6) and curr_player._num_marbles_out < 4 and _new_marble_flag:
        print("roll = ",roll)
        game._game_board[roll-1]._occupied = curr_player._color
        curr_player._num_marbles_out +=1



        #turn this update into a marble method to avoid updating the whole base list.
        #unsure why it updates the whole list.
        curr_player._base[curr_player._num_marbles_out].update_loc(roll)
        #curr_player._base[curr_player._num_marbles_out]._location = roll-1
        
        
        
        
        temp = curr_player._base[curr_player._num_marbles_out]
        print("index of marble just played: ", curr_player._base.index(temp))
        print_base(curr_player)
        print('new marble played for ' + curr_player._color)
        curr_player.marbles_out()

    #if not then move the front marble unless the front marble is stuck
    #if the front marble is stuck check if the next furthest along marble 
    #is able to move
    else:

        #print("non marble play for " + curr_player._color +  " roll = ", roll)
        ##find the front marble
        _front_marble = find_front(curr_player)

        ##check if front marble can circumnavigate the board with the
        # new roll 
        _wrap = check_wrap(_front_marble,roll,curr_player)
        
        #if wrap returns true the move is complete 
        if _wrap:
            return
        #if wrap is false then move to the second marble 
        else:
            _next_marble = find_next(_front_marble,curr_player,roll)

            return
#------------------------------------------


#------------------------------------------
#if any of the marbles on the board have a 
#location within board spaces 0-5
#return false to not play a new marble
def check_new_marble(player):

    counter = 0
    
    #if the marbels are far enough on the board or in base counter++
    for marble in range(len(player._base)):
        if player._base[marble]._location >= 6 or player._base[marble]._location == 0:
            counter += 1
    #if the marbles are all outside the first move spaces
    # play a new one         
    if counter == 4:
        return True
    else:
        return False
#------------------------------------------------


#------------------------------------------------
#function returns the index of the marble
#in the player._base list at the front of play on 
#the board.
def find_front(player):
    curr = player._base[0]
    for marble in player._base:
        if curr._location < marble._location:
            curr = marble
    return player._base.index(curr) 
#------------------------------------------------


#------------------------------------------------
#return the index of the marble with the second 
#highest location that allows for the addition of the 
#roll. 
def find_next(front,player,roll):

    #current front marble
    curr = player._base[front]

    #any marble other than front
    temp = player._base[front-1]

    #flag indicating a viable next marble
    good_marble = False

    #since curr is the highest just skip it
    for marble in player._base:
        if marble == curr:
            continue
        if temp._location < marble._location:
            
            #if marble is found with further(greater) location
            #check if it will stay behind the front marble 
            #after the roll is added.
            if marble._location + roll < curr._location:
                temp = marble
                good_marble = True

    #if a vialble marble was found return its index else return negative 
    if good_marble:
        return player._base.index(temp)
    else:
        return -999
#------------------------------------------------


#------------------------------------------------
#function checks if the front marble has traveld the 
#whole board and updates the marble location. If the 
#marble has landed on a home space the update is made
#in this function.
def check_wrap(_front_marble,roll,player):

    updated_move = player._base[_front_marble]._location + roll
    
    #if the marble has completed the board
    if updated_move > 83:

        updated_move = (updated_move-83)
        
        #put the marble in home if available
        if updated_move in [0,1,2,3] and check_home(player,updated_move):
            print(player._color + " marble is home")
            player._home[updated_move] = 1
            return True
        #if there is no spot in home check if there is room 
        # at the start of the board for the marble 
        else:
            back = check_back(player)
            #if the back marble is farther along than the 
            #front marble plus the roll will be update the 
            #front marble location. (front has now become the back)
            if player._base[back]._location > (updated_move-83):
                player._base[_front_marble]._location = (updated_move-83)
                return True
            #if the marble cant go home and cant start the board
            #again then it is stuck
            else:
                return False
    else:
        return False

#------------------------------------------------


#------------------------------------------------
#check if the spot in home is open to place a marble
def check_home(player,move):
    if player._home[move] == 0:
        player._home[move] = 1
        return True
    else:
        return False
#------------------------------------------------


#------------------------------------------------
#return the index in player._base of the marble
#with the lowest location (the back marble)
def check_back(player):
    curr = player._base[0]
    for marble in player._base:
        if curr._location > marble._location and marble._location > 0:
            curr = marble
    return player._base.index(curr) 

#------------------------------------------------


#------------------------------------------------
#find all the marbles that are out
#return list of indices in player._base
def find_out(player):
    _out = []
    for elt in player._base:
        curr = elt._location
        if curr > 0:
            _out.append(player._base.index(elt))
    return _out
#------------------------------------------------


#------------------------------------------------
def check_win(game):
    for elt in game._player_list:
        if sum(elt._home) == 4:
            game._win = True
            print(elt._color)

    if game._num_turns == 120:
        game._win = True
        print('times up')
#-------------------------------------------------

############################################################

##################GAME STATS METHODS########################

#############################################################





############################################################

##################### MAIN #################################

#############################################################

def main():
    game = __Game_obj()

    #statistics to be gathered
    _avg_aggravations = 0
    _avg_shortcut_success = 0
    _avg_turns_list = []
    game._num_turns = 1
    _avg_super = 0

    #game variables
    _curr_player = game._player_list[0]
    
    #while loop to drive the game based on _win attrib being  
    #changed.
    while game._win == False:
        
        #get current turns roll
        _curr_roll = roll_die()
        
        #update board
        update_board(game,_curr_roll,_curr_player)

        #update whos turn it is
        if _curr_player == game._player_list[-1]:
            _curr_player = game._player_list[0]
        else:
            _curr_player = game._player_list[game._player_list.index(_curr_player)+1]
            

        #update turn count
        game._num_turns += 1

        #check if there is a win
        check_win(game)

if __name__ == '__main__':
    main()
