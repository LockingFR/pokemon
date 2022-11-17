from dataclasses import dataclass
import pygame, pytmx, pyscroll
from pygame import mixer



@dataclass
class Portal:
    from_world: str                     #classe de données servant à définir des variables comme str
    origin_point : str
    target_world: str
    teleport_point: str 


@dataclass
class Map:
    name:  str
    walls : list[pygame.Rect]
    group: pyscroll.PyscrollGroup          #classe de données servant à définir des variables par rapport à leurs utilités
    tmx_data: pytmx.TiledMap
    portals: list[Portal]
    #npcs : list[NPC]

class MapManager:
    
    def __init__(self,screen, player) -> None:
        self.maps = dict() # "house" -> Map("house", wall, group)
        self.screen = screen
        self.player = player
        self.current_map ="world"
        #prends une carte d'origine, un point d'origine, pour envoyer le joueur sur une autre carte, sur un point précis
        self.register_map("world", portals=[
            Portal(from_world="world", origin_point="enter_house", target_world="house", teleport_point="spawn_house"),
            Portal(from_world="world", origin_point="enter_house2", target_world="house2", teleport_point="spawn_house2"),
            Portal(from_world="world", origin_point="enter_house_prof", target_world="prof_house", teleport_point="spawn_prof"),
            Portal(from_world="world", origin_point="tp_route1", target_world="route1", teleport_point="tp_route1_down")

        ])
        #self.register_map("house", portals = [
        #    Portal(from_world="house", origin_point="exit_house", target_world="world", teleport_point="enter_house_exit")
        #])
        self.register_map("prof_house", portals = [
            Portal(from_world="prof_house", origin_point="exit_prof", target_world="world", teleport_point="enter_prof_exit")
        ])
        self.register_map("house2", portals = [
            Portal(from_world="house2", origin_point="exit_house2", target_world="world", teleport_point="enter_house_exit2")
        ])
        self.register_map("house", portals = [
            Portal(from_world="house", origin_point="exit_house", target_world="world", teleport_point="enter_house_exit"),
            Portal(from_world="house", origin_point="exit_house", target_world="world", teleport_point="enter_house_exit"),
            Portal(from_world="house", origin_point="exit_stage", target_world="etage_house1", teleport_point="exit_stage_house")
        ])
        self.register_map("etage_house1", portals = [
            Portal(from_world="etage_house1", origin_point="exit_house_stage", target_world="house", teleport_point="spawn_house_stage")
        ])

        self.register_map("house2", portals = [
            Portal(from_world="house2", origin_point="exit_house2", target_world="world2", teleport_point="enter_house_exit2"),
            Portal(from_world="house2", origin_point="exit_stage2", target_world="etage_house2", teleport_point="exit_stage_house2")
        ])
        self.register_map("etage_house2", portals = [
            Portal(from_world="etage_house2", origin_point="exit_house_stage2", target_world="house2", teleport_point="spawn_house_stage2")
        ])
        self.register_map("route1", portals = [
            Portal(from_world="route1", origin_point="exit_route1_1", target_world="world", teleport_point="route1_exit_world"),
            Portal(from_world="route1", origin_point="exit_route1_2", target_world="city1", teleport_point="tp_enter_city")
        ])

        self.register_map("city1", portals = [
            Portal(from_world="city1", origin_point="exit_city", target_world="route1", teleport_point="tp_route1_up"),
        ])
        
        

        self.teleport_player("player")

    def check_collisions(self):
        # portails
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)
            
            if self.player.feet.colliderect(rect):
                copy_portal = portal
                self.current_map = portal.target_world
                self.player.current_map = portal.target_world
                self.teleport_player(copy_portal.teleport_point)
                
                
        
    #collision avec les murs
        for sprite in self.get_group().sprites(): 
            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()
                    

    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x #position 0 = axe des X
        self.player.position[1] = point.y #position 1 = axe des y
        self.player.save_location()

    def register_map(self,name, portals = []):
        tmx_data = pytmx.util_pygame.load_pygame(f"assets\maps\{name}.tmx") #load les maps
        map_data = pyscroll.data.TiledMapData(tmx_data) #permet de faire défiler la map
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size()) #taille de la map
        
        
        map_layer.zoom = 1.5
       
      
        #definir une liste qui va stocker les rectangles de collision
        walls = []
        
       
        #"""for obj in tmx_data.objects:
         #   if obj.type == "collision":
         #       """"walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        for group in tmx_data.objectgroups:
            for obj in group:
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        

        # dessiner le grp de calques
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        group.add(self.player)

        #créer un objet map
        self.maps[name]= Map(name, walls, group, tmx_data, portals)
        

    def get_map(self) : return self.maps[self.current_map]

    def get_group(self): return self.get_map().group

    def get_walls(self): return  self.get_map().walls
    
    def get_object(self, name) : return self.get_map().tmx_data.get_object_by_name(name)
    

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)
        
    def update(self):
        self.get_group().update()
        self.check_collisions()

        