from Aktionen import ist_rechts_frei, ist_links_frei, ist_unten_frei, ist_oben_frei
from Aktionen import inhalt_rechts, inhalt_links, inhalt_unten, inhalt_oben
from Aktionen import bewege_links, bewege_oben, bewege_rechts, bewege_unten
from Aktionen import inhalt, init_gridworld, zeigen, wenn_dann

init_gridworld(random_player=False, random_mines=False, maze=False)

wenn_dann(ist_unten_frei, bewege_unten)
wenn_dann(ist_unten_frei, bewege_unten)
wenn_dann(ist_unten_frei, bewege_unten)
wenn_dann(ist_unten_frei, bewege_unten)
wenn_dann(ist_unten_frei, bewege_unten)
wenn_dann(ist_unten_frei, bewege_unten)
wenn_dann(ist_unten_frei, bewege_unten)
wenn_dann(ist_unten_frei, bewege_unten)
wenn_dann(ist_unten_frei, bewege_unten)
wenn_dann(ist_unten_frei, bewege_unten)
wenn_dann(ist_unten_frei, bewege_unten)

'''
Beispiel fuer eigene Kondition: 
- wenn rechts frei ist, dann bewege Spieler nach rechts, 
- ansonsten wenn links frei ist, dann bewege Spieler nach links
- ansonsten wenn oben frei ist, dann bewege Spieler nach oben
- ansonsten bewege Spieler nach unten
'''
if ist_rechts_frei():
    bewege_rechts()
elif ist_links_frei():
    bewege_links()
elif ist_oben_frei():
    bewege_oben()
else:
    bewege_unten()


zeigen()
