import pygame
pygame.init() 

#global variables
gui_font = pygame.font.Font(None, 30)
clicked = False

class Button:
    def __init__(self, text, height, width, pos, elevation) :    
        #core attribut
            self.pressed = False
            self.original_y_pos = pos[1]
            self.elevation = elevation 
            self.dynamic_elevation = elevation
        #bottom rec 
            self.bottom_rect = pygame.Rect(pos, (width, elevation))
            self.bottom_color = (128,128,128)
        #top rec
            self.top_rect = pygame.Rect(pos, (width, height))
            self.top_color = (0,0,0)
        #text 
            self.text_surf = gui_font.render(text, True, (255,255,255))
            self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
    def draw(self,screen, mouse_pos):
        #elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation
        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius= 15)
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius = 15 )
        screen.blit(self.text_surf, self.text_rect)  
        self.check_click(mouse_pos)
    def check_click(self, mouse_pos):
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = (128,128,128)
            if pygame.mouse.get_pressed()[0] :
                self.dynamic_elevation = 0 
                self.pressed = True 
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed == True:  
                    self.pressed = False  
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = (0,0,0)


