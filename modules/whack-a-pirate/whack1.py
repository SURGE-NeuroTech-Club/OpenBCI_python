import pygame



class Pirate(pygame.sprite.Sprite):
    def __init__(self, image, sil, skull_image, location, duration):
        super().__init__()
        self.image = image
        self.sil = sil
        self.skull_image = skull_image
        self.rect = self.image.get_rect()
        self.duration = duration
        self.location = location
        self.visible = False
        self.clicked = False

    def update(self):
        if self.location is not None:
            self.rect.x = self.location[0] - self.rect.width / 2
            self.rect.y = self.location[1] - self.rect.height / 2

    def draw(self, surface):
        if self.visible:
            if self.clicked:
                surface.blit(self.skull_image, self.rect)
            else:
                surface.blit(self.image, self.rect)

    def draw_silhouette(self, surface):
            surface.blit(self.sil, self.rect)


