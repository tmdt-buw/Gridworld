from Aktionen import ist_rechts_frei, ist_links_frei, ist_unten_frei, ist_oben_frei
from Aktionen import inhalt_rechts, inhalt_links, inhalt_unten, inhalt_oben
from Aktionen import bewege_links, bewege_oben, bewege_rechts, bewege_unten
from Aktionen import inhalt, init_gridworld, zeigen, wenn_dann, spieler_position


init_gridworld(random_player=False, random_mines=False, maze=False)

'''' 
Hier kommt euer Code
'''


for i in range(10):
    wenn_dann(ist_rechts_frei, bewege_rechts)


''' 
Code Ende
'''


zeigen()




