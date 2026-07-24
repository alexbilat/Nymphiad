from settings import *

class Switch(pygame.sprite.Sprite):
    GLINT_INTERVAL    = 60 * 5       # how many ticks between idle glint animations (every 5 seconds)
    GLINT_FRAME_DELAY = 6            # ticks per frame of the glint

    # Maps each direction to its opposite for when the switch is flipped
    OPPOSITES = {
        'right': 'left',
        'left': 'right',
        'up': 'down',
        'down': 'up',
    }

    def __init__(self, x, y, direction='right'):
        super().__init__()

        # Three sprite sheets cover all four arrow directions
        s0 = pygame.image.load('Images/Switch/switch-sheet0.png').convert_alpha()
        s1 = pygame.image.load('Images/Switch/switch-sheet1.png').convert_alpha()
        s2 = pygame.image.load('Images/Switch/switch-sheet2.png').convert_alpha()

        # Each direction has 4 frames: frame 0 is the idle pose, frames 1-3 are the glint animation
        self._frames = {
            'left': [
                s0.subsurface((35, 35, 32, 32)),
                s0.subsurface((69, 35, 32, 32)),
                s0.subsurface(( 1, 69, 32, 32)),
                s0.subsurface((35, 69, 32, 32)),
            ],
            'right': [
                s0.subsurface((69, 69, 32, 32)),
                s1.subsurface(( 1,  1, 32, 32)),
                s1.subsurface((35,  1, 32, 32)),
                s1.subsurface((69,  1, 32, 32)),
            ],
            'up': [
                s1.subsurface(( 1, 35, 32, 32)),
                s1.subsurface((35, 35, 32, 32)),
                s1.subsurface((69, 35, 32, 32)),
                s1.subsurface(( 1, 69, 32, 32)),
            ],
            'down': [
                s1.subsurface((35, 69, 32, 32)),
                s1.subsurface((69, 69, 32, 32)),
                s2.subsurface(( 1,  1, 32, 32)),
                s2.subsurface((35,  1, 32, 32)),
            ],
        }

        if direction not in self._frames:
            raise ValueError("Switch direction must be 'left', 'right', 'up', or 'down'")

        self._player_touching = False  # tracks whether the player was touching last frame

        self.direction    = direction
        self._frame_index = 0   # 0 = idle frame, 1-3 = glint frames
        self._frame_timer = 0   # counts ticks within the current frame
        self._idle_timer  = 0   # counts ticks since the last glint, to trigger the next one

        self.image = self._frames[direction][0]
        self.rect  = self.image.get_rect(topleft=(x, y))

    def flip_direction(self):
        """Flip the arrow to the opposite direction and play the switch sound."""
        self.direction = self.OPPOSITES[self.direction]
        self._frame_index = 0
        self._frame_timer = 0
        self._idle_timer = 0
        self.image = self._frames[self.direction][0]
        play('switch', CH_SWITCH)

    def check_collision(self, player_hitbox):
        """Return True only on the FIRST frame of a new player touch, not every frame they overlap."""
        touching_now = self.rect.colliderect(player_hitbox)

        if touching_now and not self._player_touching:
            self._player_touching = True
            return True  # rising edge - player just entered

        if not touching_now:
            self._player_touching = False  # player left, reset so it can fire again next time

        return False

    def update(self):
        frames = self._frames[self.direction]

        if self._frame_index > 0:
            # Currently playing the glint animation - advance it
            self._frame_timer += 1
            if self._frame_timer >= self.GLINT_FRAME_DELAY:
                self._frame_timer = 0
                self._frame_index += 1
                if self._frame_index >= len(frames):
                    self._frame_index = 0  # glint done, return to idle
                    self._idle_timer  = 0
            self.image = frames[self._frame_index]

        else:
            # Idle - show the base frame and wait for the glint interval
            self.image = frames[0]
            self._idle_timer += 1
            if self._idle_timer >= self.GLINT_INTERVAL:
                self._frame_index = 1  # kick off the glint animation
                self._frame_timer = 0
                self._idle_timer  = 0