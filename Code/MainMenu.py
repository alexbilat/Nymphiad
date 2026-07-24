# Header
_author_ = "Alex Bilat"
_date_ = "2025/12/04"
_version_ = "1.0"
_filename_ = "settings.py"
_description_ = "Main Menu Class"

from settings import *

class MainMenu():
    def __init__(self):
        """Initialize the main menu"""
        super().__init__()

        # Background
        self.sheet_background_surf = pygame.image.load('Images/Main Menu/menu_bg-sheet1.png').convert_alpha()
        self.background_clouds = self.sheet_background_surf.subsurface((0, 0, SCREEN_WIDTH, 232))
        self.background_hill = self.sheet_background_surf.subsurface((0, 506, SCREEN_WIDTH, 218))
        self.sheet_wallpaper_surf = pygame.image.load('Images/Main Menu/menu_bg-sheet0.png').convert_alpha()
        self.background_grass = pygame.image.load('Images/Main Menu/grass.png')
        self.background_sky = self.sheet_wallpaper_surf.subsurface((0, 644, SCREEN_WIDTH, 362))
        
        # Darken the screen
        self.bg = pygame.image.load('Images/Main Menu/overlay_bg.png').convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.bg.set_alpha(128) 

        # Title of the game
        self.title_surf = pygame.image.load('Images/Main Menu/logo_game_text-sheet0.png').convert_alpha()
        self.bar = pygame.image.load('Images/Main Menu/logo_game_bar-sheet0.png').convert_alpha()
        
        # Buttons with font
        self.font = pygame.font.Font('font/Greek-Freak.ttf', 24)
        self.play_surf = self.font.render('Play', True, (255, 255, 255))
        self.play_rect = self.play_surf.get_rect(center=(SCREEN_WIDTH // 2, 200))


        self.quit_surf = self.font.render('Quit', True, (255, 255, 255))
        self.quit_rect = self.quit_surf.get_rect(center=(SCREEN_WIDTH // 2, 240))

        # Side bubble things
        self.selector_sheet = pygame.image.load('Images/Main Menu/menu_selector-sheet0.png').convert_alpha()
        self.frameWidth = 173
        self.frameHeight = 15
        self.selector_frames = [
            self.get_frame_selector(39),
            self.get_frame_selector(56)
        ]

        # Find subframes
        self.play_selector_rect = self.selector_frames[0].get_rect(center=self.play_rect.center)
        self.quit_selector_rect = self.selector_frames[0].get_rect(center=self.quit_rect.center)

        self.selector_index = 0
        self.selector_index_speed = 0.025
        self.hover_target = None
        self.overPlay = False
        self.overOptions = False
        self.overQuit = False

        # Level changing
        self.state = 'start'

        # Audio: start menu music and track hover to fire select sound once per entry
        play_music('menu')
        self._last_hover = None

    def get_frame_selector(self, y_offset):
        """Get's the frame for the selector"""
        return self.selector_sheet.subsurface((0,y_offset, self.frameWidth, self.frameHeight))
    
    def side_animation(self, mouse_pos):

        # Updates the animation index
        self.selector_index += self.selector_index_speed
        if self.selector_index >= len(self.selector_frames):
            self.selector_index = 0
        
        # Reset hover target and flags every frame
        self.hover_target = None
        self.overPlay = False
        self.overQuit = False
        
        # Main logic
        if self.play_rect.collidepoint(mouse_pos):
            self.hover_target = self.play_rect
            self.overPlay = True
        elif self.quit_rect.collidepoint(mouse_pos):
            self.hover_target = self.quit_rect
            self.overQuit = True

        # Play select sound once each time the cursor enters a new button
        current_hover = (self.overPlay, self.overQuit)
        if any(current_hover) and current_hover != self._last_hover:
            play('select', CH_UI)
        self._last_hover = current_hover
        

    def clicked(self, mouse_pos, event):
        """Check for clicks"""
        if self.play_rect.collidepoint(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN:
            self.state = 'level_1'
        elif self.quit_rect.collidepoint(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN:
            pygame.quit()
            exit()


    def draw(self, screen, mouse_pos):
        """Draws Background and buttons"""
        # Back ground
        screen.blit(self.background_sky, (0, 0))
        screen.blit(self.background_clouds, (0, 0))
        screen.blit(self.background_hill, (0, 150))
        screen.blit(self.background_grass, (0, 290))
        screen.blit(self.bg, (0,0))

        # Title Elements and buttons
        screen.blit(self.title_surf, (100, 40))
        screen.blit(self.bar, (116, 14))
        screen.blit(self.bar, (116, 126))
        screen.blit(self.play_surf, self.play_rect)
        screen.blit(self.quit_surf, self.quit_rect)

        if self.hover_target:
            frame = self.selector_frames[int(self.selector_index)]
            if self.overPlay:
                screen.blit(frame, self.play_selector_rect)
            elif self.overQuit:
                screen.blit(frame, self.quit_selector_rect)

    def update(self, screen, mouse_pos, event):
        """Update this class with information"""
        self.draw(screen, mouse_pos)
        self.clicked(mouse_pos, event)
        self.side_animation(mouse_pos)

        return self.state