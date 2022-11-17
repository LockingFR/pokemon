import pygame
import pytmx
import pyscroll
from pygame import mixer

from personnage import Player
from map import MapManager
mixer.pre_init(44160, -16, 1, 512)
pygame.mixer.init()

world_theme_song = mixer.Sound("assets\sounds\world_theme.mp3")
world_theme_song.set_volume(0.3)
house_song = mixer.Sound("assets\sounds\way101.mp3")
house_song.set_volume(0.1)
prof_song = mixer.Sound("assets\sounds\prof_theme.mp3")
prof_song.set_volume(0.3)



#récupérer le nom d'un objet définie dans tiled
def get_tile_by_name(tmx_data, name):

    for group in tmx_data.objectgroups: #Pour tous les objets de la carte.tmx, cela cherche un objet donné.
            for obj in group:
                if obj.name == name:
                    return obj


class Jeu:
    def __init__(self):
        # Créer la fenêtre
        icon = pygame.image.load("assets\images\icon\poke.png")
        pygame.display.set_icon(icon)
        self.screen = pygame.display.set_mode((1000, 720)) 
       
        
        #self.icon = pygame.icon
        pygame.display.set_caption("Pokémon - Table")        

        # generer un joueur
        self.player = Player(0, 0)
        self.map_manager = MapManager(self.screen, self.player)

        #definir le rect de collision pour entrer dans la maison

        self.current_song = None
        
       

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.player.move_up()       #input des flèches du clavier, liées à des fonctions dans personnage.py (qui s'occupe de la direction)
        elif pressed [pygame.K_DOWN]:
            self.player.move_down()
        elif pressed [pygame.K_LEFT]:
            self.player.move_left()
        elif pressed [pygame.K_RIGHT]:
            self.player.move_right()

    
    
    def play_sounds(self):
    
    # joue un son donné si il n'est pas déjà lancé
        
        if self.map_manager.current_map == "world" and self.current_song != "world theme":
            self.current_song = "world theme"

            house_song.stop()
            prof_song.stop()

            world_theme_song.play(loops=-1) #boucle infinie
            
        elif self.map_manager.current_map == "route1" and self.current_song != "route1 theme":

            self.current_song = "route1 theme"

            world_theme_song.stop()
            prof_song.stop()
            
            house_song.play(loops=-1)

        elif self.map_manager.current_map == "prof_house" and self.current_song != "prof theme":

            self.current_song = "prof theme"
            
            world_theme_song.stop()
            house_song.stop()
            
            prof_song.play(loops=-1)
        
    


    def update(self):
        self.map_manager.update() #mets à jour


    def run(self):
        
        clock = pygame.time.Clock()
        
        # Boucle du jeu
        running = True 
        

        while running:

            self.player.save_location()
            self.handle_input()         #initialisation des fonctions
            self.update()
            self.map_manager.draw()
            self.play_sounds()
            
            pygame.display.flip()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60) #nombre d'ips
    
        pygame.quit()

