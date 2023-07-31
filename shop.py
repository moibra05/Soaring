import pygame
from configs import *
 
class Shop:
    def __init__(self, cash, plane, upgrades: list[int]):
        self.screen = pygame.display.get_surface()
        self.shop = pygame.image.load(f"{CWD}/assets/gameImages/shop.png")
        self.cont_arrow = pygame.transform.scale(
            pygame.image.load(f"{CWD}/assets/gameImages/continueArrow.png"), (162, 123)
            ).convert_alpha()
        self.cont_arrow_rect = self.cont_arrow.get_rect(topleft = (775, 570))
        self.cont_arrow_pos = self.cont_arrow_rect
        self.drop_down = pygame.transform.scale(
            pygame.image.load(f"{CWD}/assets/gameImages/drop_down.png"), (155, 224)
            )
        self.upgrades = upgrades
        self.upgrade_costs = [] # Star Spawn, Max Speed, Wind Power, Aerodynamics
        self.max_upgrades = [12, 12, 8, 6]
        for upgrade in self.upgrades:
            self.upgrade_costs.append(25 + (25 * upgrade))
        self.buyfx = pygame.mixer.Sound(f"{CWD}/assets/soundEffects/buy_sound.mp3")
        self.errorfx = pygame.mixer.Sound(f"{CWD}/assets/soundEffects/purchase_error.mp3")
        self.cash = cash
        self.plane = plane

    def draw_upgrade(self, title, cost, description, index):
        mouse_pos = pygame.mouse.get_pos()
        drop_down_pos = (mouse_pos[0] + 10, mouse_pos[1] + 10)
        upgrade_title_pos = (mouse_pos[0] + 20, mouse_pos[1] + 20)
        upgrade_cost_pos = (mouse_pos[0] + 20, mouse_pos[1] + 37)
        upgrade_number_pos = (mouse_pos[0] + 20, mouse_pos[1] + 200)

        upgrade_title = upgrade_font.render(title, True, "black")
        upgrade_cost = upgrade_font.render(f"${cost}", True, "black")

        if self.upgrades[index] < self.max_upgrades[index]:
            upgrade_number = upgrade_font.render(f"Owned: {self.upgrades[index]}", True, "black")
        else:
            upgrade_number = upgrade_font.render("MAX", True, "black")

        self.screen.blit(self.drop_down, drop_down_pos)
        self.screen.blit(upgrade_title, upgrade_title_pos)
        self.screen.blit(upgrade_cost, upgrade_cost_pos)
        self.screen.blit(upgrade_number, upgrade_number_pos)

        description_text = description.split("/")

        for i in range(len(description_text)):
            upgrade_desc = description_font.render(description_text[i], True, "black")
            upgrade_desc_pos = (mouse_pos[0] + 20, mouse_pos[1] + 65 + (17 * i))
            self.screen.blit(upgrade_desc, upgrade_desc_pos)

    def upgrade_select(self):
        mouse_pos = pygame.mouse.get_pos()

        if 139 < mouse_pos[0] < 298 and 238 < mouse_pos[1] < 397:
            self.draw_upgrade("Star Spawn", self.upgrade_costs[0], 
            "Increases/the rate stars/spawn", 0)

        elif 401 < mouse_pos[0] < 560 and 179 < mouse_pos[1] < 337:
            self.draw_upgrade("Max Speed", self.upgrade_costs[1], 
            "Your plane/is able to/acheieve a/greater/maximum speed", 1)

        elif 401 < mouse_pos[0] < 560 and 378 < mouse_pos[1] < 537:
            self.draw_upgrade("Wind Power", self.upgrade_costs[2], 
            "Coming into/contact with/wind will give/you a greater/temporary/speed boost", 2)

        elif 667 < mouse_pos[0] < 826 and 238 < mouse_pos[1] < 397:
            self.draw_upgrade("Aerodynamic", self.upgrade_costs[3], 
            "Your plane/retains its/velocity for/longer", 3)

    def upgrade(self, index):
        self.upgrades[index] += 1
        self.upgrade_costs[index] += 25
        self.buyfx.play()

    def update(self, cash):
        mouse_pos = pygame.mouse.get_pos()
        self.cash = cash
        if 775 < mouse_pos[0] < 937 and 570 < mouse_pos[1] < 693:
            self.cont_arrow = pygame.transform.scale(self.cont_arrow, (178, 135))
            self.cont_arrow_pos = pygame.Vector2(765, 560)
        else:
            self.cont_arrow = pygame.transform.scale(
                pygame.image.load(f"{CWD}/assets/gameImages/continueArrow.png"), (162, 123)
                )
            self.cont_arrow_pos = pygame.Vector2(775, 570)

        self.upgrade_select()

    def draw(self):
        cash_text = default_font.render(f"${self.cash:.2f}", True, "green")
        rect = cash_text.get_rect(center = (WIDTH/2, 665))
        self.screen.blit(self.shop, (0,0))
        self.screen.blit(self.cont_arrow, self.cont_arrow_pos)
        self.screen.blit(cash_text, rect)

        
