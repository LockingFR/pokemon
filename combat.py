import pygame
import pytmx
import pyscroll

from personnage import Player
from map import MapManager

class combat:
    def __init__(self):
        self.vie_pokemon_allie =
        self.vie_pokemon_enemie = 
        self.attaques_pokemon_allie =
        self.attaques_pokemon_allie = 
        self.choix_joueur_menu = 0
        self.statu_pokemon_allie =
        self.statu_pokemon_enemie =



    def menu_general(self):
         pressed = pygame.key.get_pressed()
        elif pressed [pygame.K_LEFT]:
            self.choix_joueur_menu =- 1 #les differentes options seront sur une meme ligne , ça facilitera le truc
        elif pressed [pygame.K_RIGHT]:
            self.choix_joueur_menu =+ 1
        if self.choix_joueur_menu == 5:
            self.choix_joueur_menu = 0

            hsahgrgylgi