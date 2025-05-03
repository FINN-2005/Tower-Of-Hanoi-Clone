from classses import *

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(RES, pygame.SRCALPHA)
        self.clock = pygame.Clock()
                
        self.towerA, self.towerB, self.towerC = [Tower(pos=(HW - W/3,HH), no_of_discs=6),Tower(pos=(HW ,HH), no_of_discs=0),Tower(pos=(HW + W/3 ,HH), no_of_discs=0)]
        
    def update(self):
        TOWER_GROUP.update()
        TOWER_GROUP.draw(self.screen)
        DISC_GROUP.update()
        DISC_GROUP.draw(self.screen)
        
        
    def run(self):
        self.running = True
        while self.running:
            self.dt = self.clock.tick(FPS)/1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False
                    
            self.screen.fill('bisque')
            
            self.update()
            
            pygame.display.set_caption(f'FPS: {self.clock.get_fps()}')
            
            pygame.display.flip()
            
            
Game().run()
            