from settings import *

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.coin_sheet = pygame.image.load('Images/Coin/obol-sheet0.png').convert_alpha()

        # Spin frames parsed from data.js
        # Format per entry: (x, y, duration) - all frames are 16x16
        # The coin holds its wide face for 12 ticks and the thin edge for 6, just like the original
        self.spin_frames = []
        frame_data = [
            (1,  1,  12),  # frame 0 - held for 12 ticks (wide face, very shiny, very tempting)
            (19, 1,  1),   # frame 1
            (37, 1,  1),   # frame 2
            (1,  19, 1),   # frame 3
            (19, 19, 6),   # frame 4 - held for 6 ticks (narrow edge)
            (37, 19, 1),   # frame 5
            (1,  37, 1),   # frame 6
            (37, 19, 1),   # frame 7
        ]
        # Each entry expands into 'duration' copies of the frame so we can just step through the list
        for fx, fy, duration in frame_data:
            frame = self.coin_sheet.subsurface((fx, fy, 16, 16))
            for _ in range(duration):
                self.spin_frames.append(frame)

        self.frame_index = 0
        self.SPIN_DELAY = 2  # advance one frame every 2 game ticks
        self.frame_timer = 0

        # Float state - the coin bobs up and down using a sine wave
        self.spawn_y = y          # base Y to bob around, never changes
        self.float_offset = 0.0   # current vertical offset in pixels
        self.float_speed = 0.03   # how fast the sine wave advances (radians per tick)
        self.float_amplitude = 3  # how many pixels it floats up and down

        self.float_timer = 0.0    # angle into the sine wave

        self.image = self.spin_frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))

    def animation(self):
        """Advance the spin animation one step"""
        self.frame_timer += 1
        if self.frame_timer >= self.SPIN_DELAY:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.spin_frames) # Regular animation procedure
        self.image = self.spin_frames[self.frame_index]

    def float(self):
        """Slowly bob the coin up and down using sin - an actual use lol"""
        self.float_timer += self.float_speed
        self.float_offset = math.sin(self.float_timer) * self.float_amplitude
        self.rect.y = int(self.spawn_y + self.float_offset)

    def update(self):
        """Updates"""
        self.animation()
        self.float()