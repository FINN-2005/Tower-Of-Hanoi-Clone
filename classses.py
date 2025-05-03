from settings import *
    
    
class Disc(pygame.sprite.Sprite):
    Active_Box = None
    def __init__(self, pos=[HW, HH], level=Disc_stuff.MAX_DISC_LEVEL, tower=None):
        super().__init__(DISC_GROUP)
        self.level = level
        self.pos = pos
        
        self.tower = tower

        self.color = getattr(Disc_stuff.cols, f"level_{level}", Disc_stuff.cols.default)
        self.size = (level * Disc_stuff.W / Disc_stuff.MAX_DISC_LEVEL + Disc_stuff.H, Disc_stuff.H)

        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.image.get_frect(midbottom=pos)

        pygame.draw.rect(self.image, self.color, self.image.get_rect(), border_radius=self.size[1] // 2)
        pygame.draw.rect(self.image, "black", self.image.get_rect(), 2, border_radius=self.size[1] // 2)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def _move_if_code(self):
        m_pos = V2(pygame.mouse.get_pos())
        if disc_group.ACTIVE_DISC is self:
            if self.rect.collidepoint(m_pos) or not self.offset_set:
                if self.offset_set:
                    self.offset = self.pos - m_pos
                    self.offset_set = False
                else:
                    if self.offset.magnitude_squared():
                        self.pos = m_pos + self.offset
        elif disc_group.ACTIVE_DISC is None:
            if self.rect.collidepoint(m_pos):
                disc_group.ACTIVE_DISC = self
    

    def _move_else_code(self):
        self.offset = V2()             
        self.offset_set = True
        disc_group.ACTIVE_DISC = None

    def drag_n_drop(self):
        condition = pygame.mouse.get_pressed()[0]
        if self.tower.top_disc is self:
            if condition: self._move_if_code()
            else: 
                if disc_group.ACTIVE_DISC is self:
                    self.tower.snap_to_tower(self)
                self._move_else_code()

    def update(self):
        self.drag_n_drop()
        self.rect.midbottom = self.pos

class Tower(pygame.sprite.Sprite):
    def __init__(self, pos=(HW,HH), no_of_discs=Disc_stuff.MAX_DISC_LEVEL):
        super().__init__(TOWER_GROUP)
        
        self.size = (max(Tower_stuff.base_w, Tower_stuff.stick_w),max(Tower_stuff.base_h, Tower_stuff.stick_h))
        self.pos = pos
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.image.get_frect(center=self.pos)
    
        w,h = self.size
        blx, bly = 0, h     # bottom left coords
        pygame.draw.rect(self.image, Tower_stuff.cols.stick, (w/2 - Tower_stuff.stick_w/2, 0, Tower_stuff.stick_w, Tower_stuff.stick_h), 0, int(Tower_stuff.stick_w/2 + 2))
        pygame.draw.rect(self.image, 'black', (w/2 - Tower_stuff.stick_w/2, 0, Tower_stuff.stick_w, Tower_stuff.stick_h), 2, int(Tower_stuff.stick_w/2 + 2))
        pygame.draw.rect(self.image, Tower_stuff.cols.base, (blx, bly-Tower_stuff.base_h, w, Tower_stuff.base_h), 0, -1, int(Tower_stuff.base_h/2 + 2), int(Tower_stuff.base_h/2 + 2), int(Tower_stuff.base_h/2 -2), int(Tower_stuff.base_h/2 -2))       
        pygame.draw.rect(self.image, 'black', (blx, bly-Tower_stuff.base_h, w, Tower_stuff.base_h), 2, -1, int(Tower_stuff.base_h/2 + 2), int(Tower_stuff.base_h/2 + 2), int(Tower_stuff.base_h/2 -2), int(Tower_stuff.base_h/2 -2))       
        
        self.no_of_discs = no_of_discs
        self.discs:list[Disc] = []
        for i in range(self.no_of_discs):
            x = self.rect.centerx
            y = self.rect.bottom - Tower_stuff.base_h - Disc_stuff.H*i
            self.discs.append(Disc((x,y), no_of_discs-i, self))
            
        self.top_disc = self.discs[-1] if self.discs else None

    def snap_to_tower(self, disc):
        disc_is_set = False
        for tower in TOWER_GROUP.sprites():
            if tower == self: continue
            if tower.rect.collidepoint(disc.rect.midbottom):
                if not tower.top_disc or (tower.top_disc.level > disc.level):
                    self.discs.remove(disc)
                    tower.discs.append(disc)
                    tower.top_disc = disc  
                    disc.pos = V2(tower.rect.centerx, tower.rect.bottom - (len(tower.discs)-1) * Disc_stuff.H - Tower_stuff.base_h)
                    disc.tower = tower
                    disc_is_set = True
                    break  
        if not disc_is_set: disc.pos = V2(self.rect.centerx, self.rect.bottom - (len(self.discs)-1) * Disc_stuff.H - Tower_stuff.base_h)
    
    def update(self):
        self.discs = sorted(self.discs, key= lambda a: a.level, reverse=True)
        self.top_disc = self.discs[-1] if self.discs else None
    
    