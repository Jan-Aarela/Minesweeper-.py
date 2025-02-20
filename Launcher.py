import os                           #font digital
import time
from libs import ascii_graphics as ascii_g
from libs import sweepergame as sw_game
from libs import soundlib
import platform


theme = {
    "theme" : None,        # This is useless tgb
    "themepath" : None,    # This is the filepath where all sprites and sounds are taken from.
    "cmdcolor"     : None  # Color of the cmd/terminal. Only works with Windons though :/
}


def cls():
    """
    Clears the text based menu with a simple command,
    depending on platform. Eg. Windows or Linux.
    """
    if platform.system() == "Windows":
        os.system("cls")
        
    if platform.system() == "Linux":
        os.system("clear")


def switch_theme():
    """
    Switches the games's theme depending on what player chooses. Then grabs resources 
    from corresponding path and uses those resources for the game. 
    Also changes the terminal/cmd color if on Windows trough reading color.txt file.
    """
    os.system('mode con: cols=32 lines=24')   
    themes = os.listdir("themes")
    
    listedthemes = []       
    
    while True:
        try:
            listedthemes = []
            print()
            for i, pack in enumerate(os.listdir("themes"), start = 1):
                listedthemes.append(i) 
                print(f"  {i} - {pack}")
            print("""
  Ps. The only theme that works
  is Minecraft, Rest of the 
  themes are missing assets.
""") 
            x = int(input("  Selection: ") or 4 )
            
        except ValueError:
            print()
            input("  Selection must a number")
            cls()
            
        else:
            if x in listedthemes:
                break    
                
            else:
                print()
                input(f"  Your options are 0-{len(listedthemes)}...")
                cls()
        
    theme["theme"] = themes[x-1]
    theme["themepath"] = f'themes/{theme["theme"]}'

    with open(f'{theme["themepath"]}/color.txt') as color_file:
        stuff = color_file.read().splitlines()
        theme["cmdcolor"] = stuff[0]
        textcolor = (int(stuff[1]),int(stuff[2]),int(stuff[3]),int(stuff[4]))

    if platform.system() == "Windows":
        os.system(theme["cmdcolor"])
               
    soundlib.states["themepath"] = theme["themepath"]
    sw_game.theme["themepath"] = theme["themepath"]
    sw_game.theme["color"] = textcolor
        
    
       
def menu():
    """
    This is the main menu of the misweeper game.
    Prompts the user with options to explore features.
    Eg. Play, credits, scoreboard etc.
    """
    while True:
        soundlib.sfx("interract")
        os.system('mode con: cols=32 lines=24')
        print(ascii_g.menu)
        try: 
            x = (input("  Selection: ")).lower() or "p"
        except KeyboardInterrupt:
            cls()
            break
            
        else:
            if x == "p" or x == "play":
                cls()
                game_setup()
                         
            elif x == "s" or x == "scoreboard":
                cls()
                show_scoreboard()
                
            elif x == "m" or x == "mute":
                soundlib.mute()
                
                
            elif x == "c" or x == "credits":
                cls()
                show_credits()
                
                
            elif x == "q" or x == "quit":
                cls()
                quit_game()
                break
                
            else:
                soundlib.sfx("error")
                input(ascii_g.choises)
                

def show_scoreboard():
    """
    Shows scoreboard/history data from scoreboard.txt file
    and reorganizes it into desending order.
    """
    os.system('mode con: cols=72 lines=44')
    soundlib.sfx("interract")
    
    scores = []
    with open("Scoreboard.txt") as file:
        for line in file:
            linestripped = line.strip("\n")
            scores.append(linestripped)
    
    scores.sort(reverse=True) 
    pages = int(len(scores)/ 32)+1
    
    
    for i in range(pages):
        print(ascii_g.scoreboard)
        print()
        print("  Date              Outcome  Time     Size   Turns  Mines  Player name   ")
        print()
        if len(scores) == 0:
            continue
        
        for j in range(32):
            if len(scores) != 0:
                print(f"  {scores[0]}")
                scores.remove(scores[0])
        
        if len(scores) != 0:
            print()
            input(f"  {i+1}. page.    Press enter to show next Page")
            soundlib.sfx("interract")
            cls()
        if len(scores) == 0:
            break
    
    print()
    input(f"  {i+1}. page.    Press ENTER to return ")
    
 
def show_credits():
    """
    Shows credits.
    """
    soundlib.sfx("interract")
    print(ascii_g.cred2)
    input("  Press ENTER to return ")


def game_setup():
    """
    Sets the parametres for the minesweeper game.
    Eg. field's dimensions, amt. of mines and the player name.
    """
     
    while True:
        cls()
        print(ascii_g.setuph)
        try:
            soundlib.sfx("interract")
            h_tiles = int(input("  Horizontal tiles amt. : ") or 12)
            soundlib.sfx("interract")
            v_tiles = int(input("    Vertical tiles amt. : ") or 12)
            soundlib.sfx("interract")
            n_mines = int(input("            Mines in %  : ") or 15)
            soundlib.sfx("interract")
            print()
            playername = (input("  Player name : ")).strip()
            soundlib.sfx("interract")
            
        except ValueError:
            input("  Must be an integrer.")
            
        else:
            if (h_tiles < 8 or h_tiles > 32
                or v_tiles < 8 or v_tiles > 32):
                input("""  
  Amt. of tiles must 
  be within 8 - 32.
  Press ENTER to retry.""")
                continue
            
            if n_mines < 10 or n_mines > 50:
                input("""
                
  % of mines must be
  within 10-50%
  Press ENTER to retry.""")
                continue
                         
            if len(playername) > 12:
                input("""
                
  Name must be less than
  12 letters long.""")
                continue
            
            if playername == "":
                playername = "Guest"
                
                
            break
                
    sw_game.stats["h_tiles"] = h_tiles
    sw_game.stats["v_tiles"] = v_tiles
    sw_game.stats["n_mines"] = int(h_tiles * v_tiles * 0.01 * n_mines)
    sw_game.gamedata["playername"] = playername
    
    cls()
    soundlib.sfx("interract")
    print(ascii_g.running)
    sw_game.load()
    

def quit_game():
    """
    Quits the game while turning off music for more
    dramatic effect.
    """
    soundlib.b_music(-1)
    soundlib.sfx("interract")
    print("""


             Bruh""")
  
    time.sleep(1)
    cls()
    



"""
Following lines set the theme of the game by grabbing files from a specific file path.
Then initializes soundlibrary and after that, runs the main menu.

If running though terminal/cmd etc.,
Clears the terminal window.
"""

os.system('cmd /c "cls"')

switch_theme()

soundlib.b_music(1) 

menu() 
