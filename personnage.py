import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        
        # création du joueur, défini son rect de collision, la couleur du rect, la position initiale ...
        self.sprite_sheet = pygame.image.load('assets\images\personnages\Player1.png')
        self.small_sprite_sheet = pygame.transform.scale(self.sprite_sheet, (self.sprite_sheet.get_width()//1.5,self.sprite_sheet.get_height()//1.5))
        #utilisé dans des cas spéciaux, si le personnage parait trop grand
        self.current_map = "world"
        self.image = self.get_image(0, 0, self.sprite_sheet)
        self.image.set_colorkey([0,0,0])
        self.rect = self.image.get_rect()
        self.position = [x,y]
        self.moving = False
        self.direction = 'down'

        self.frame = 0 #premiere frame
        self.frame_timer = 0 # "vitesse" entre chaque frame

        self.animations = {
            'down': [self.get_image(48*i,0, self.sprite_sheet) for i in range(4)], #créé des listes avec les sprites de directions
            'left': [self.get_image(48*i,48, self.sprite_sheet) for i in range(4)],
            'right': [self.get_image(48*i,96, self.sprite_sheet) for i in range(4)],
            'up': [self.get_image(48*i,144,self.sprite_sheet) for i in range(4)]
        }

        self.small_animations = {
            'down': [self.get_image(32*i,0, self.small_sprite_sheet) for i in range(4)], #créé des listes avec les sprites de directions pour le personnage plus petit
            'left': [self.get_image(32*i,32, self.small_sprite_sheet) for i in range(4)],
            'right': [self.get_image(32*i,64, self.small_sprite_sheet) for i in range(4)],
            'up': [self.get_image(32*i,96, self.small_sprite_sheet) for i in range(4)]
        }
                    
        self.old_position = self.position.copy()
        self.feet= pygame.Rect(0, 0, self.rect.width * 0.5, 12) #"rétrécie" le rect autour du personnage pour améliorer le rendu lors d'une collision
        self.speed = 3 #vitesse du personnage 

    def save_location (self):
        self.old_position = self.position.copy()

    def change_animation(self): 

        #if self.current_map == "world" or self.current_map == "house" or self.current_map =='prof_house' :
        self.image = self.animations[self.direction][self.frame] #permet de changer les animations par rapport à la direction ainsi qu'à la bonne frame
        self.image.set_colorkey((0,0,0))

        #elif self.current_map == "house" or self.current_map =='prof_house':
            #self.image = self.small_animations[self.direction][self.frame]
            #self.image.set_colorkey((0,0,0))

    def move_right(self) : 
        if self.direction != 'right':
            self.direction = 'right' 
            self.frame = 0

        self.moving = True                      #les move_"direction" permettent de bouger dans telles directions par rapport aux input donnés
        self.frame_timer += 1
        
        self.position[0] += self.speed
    
    def move_left(self) :

        if self.direction != 'left':
            self.direction = 'left' 
            self.frame = 0

        self.moving = True        
        self.frame_timer += 1
        
        self.position[0] -= self.speed
    
    def move_up(self) : 

        if self.direction != 'up':
            self.direction = 'up' 
            self.frame = 0

        self.moving = True        
        self.frame_timer += 1

        self.position[1] -= self.speed
    
    def move_down(self) :

        if self.direction != 'down':
            self.direction = 'down' 
            self.frame = 0

        self.moving = True
        self.frame_timer += 1

        self.position[1] += self.speed


    def update(self):
        self.rect.center = self.position
        self.feet.midbottom = self.rect.midbottom


        if self.moving:
           
                if self.frame_timer == 20:
                    self.frame_timer = 0

                if self.frame_timer % 5 == 0 and self.frame_timer != 0: 
                    self.frame += 1

                if self.frame == 4:             # permet au personnage de changer d'animation de frame (boucle pour répéter)
                    self.frame = 0
        else:
            self.frame = 0

        self.moving = False

        self.change_animation()


    def move_back(self):
        self.position = self.old_position
        self.rect.center = self.position
        self.feet.midbottom = self.rect.midbottom


    def get_image(self, x, y, sheet):

        if sheet == self.sprite_sheet:
            image = pygame.Surface([48, 48])
            image.blit(self.sprite_sheet, (0, 0), (x, y, 48, 48))
            self.rect = image.get_rect()
            self.speed = 3
        elif sheet == self.small_sprite_sheet:
            image = pygame.Surface([32, 32])
            image.blit(self.small_sprite_sheet, (0, 0), (x, y, 32, 32))
            self.rect = image.get_rect()
            self.speed = 1
        return image

    #utilisé pour récupérer la taille des images du personnage, en pixels, défini la vitesse qu'aura telle sprite de personnage