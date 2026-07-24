from settings import *

class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.box_sheet = pygame.image.load('Images/Box/box-sheet0.png').convert_alpha()
        self.image = self.box_sheet.subsurface((0, 0, 32, 32))
        self.rect = self.image.get_rect(topleft=(x, y))

        # Physics
        self.dy = 0                 # current vertical velocity
        self.float_y = float(y)    # sub-pixel Y position so gravity accumulates cleanly
        self.GRAVITY = 0.5
        self.MAX_GRAVITY = 20
        self.being_grabbed = False  # True while the player is holding X near this box
        self.just_wrapped = False   # set for one frame after wrapping so we skip gravity that tick

        # Audio - only play an impact sound if the box was actually falling fast enough to matter
        self._prev_dy = 0
        self._IMPACT_THRESHOLD = 3  # minimum falling speed to count as an impact

    def move_x(self, dx, wall_tiles):
        """Move horizontally and push back out of any wall tiles we entered."""
        if dx == 0:
            return 0
        self.rect.x += int(dx)
        actual_dx = dx
        for tile in wall_tiles:
            if self.rect.colliderect(tile):
                if dx > 0:
                    actual_dx -= (self.rect.right - tile.left)
                    self.rect.right = tile.left  # hit a wall going right
                elif dx < 0:
                    actual_dx += (tile.right - self.rect.left)
                    self.rect.left = tile.right  # hit a wall going left
        return actual_dx

    def apply_gravity(self, wall_tiles, boxes=None):
        """Pull the box down each frame and resolve collisions against tiles and other boxes."""
        if self.just_wrapped:
            self.just_wrapped = False  # skip gravity the frame we wrapped so we don't tunnel
            return

        falling_speed_before = self.dy
        self.dy = min(self.dy + self.GRAVITY, self.MAX_GRAVITY)

        # Other boxes count as solid ground - a box can sit on top of another box
        sibling_rects = [b.rect for b in boxes.sprites() if b is not self] if boxes else []
        all_solid = list(wall_tiles) + sibling_rects

        # Sub-step the movement so fast-falling boxes don't tunnel through thin floors
        remaining = self.dy
        step_sign = 1 if remaining > 0 else -1
        landed = False
        while remaining != 0:
            step = step_sign * min(abs(remaining), TILE_SIZE)
            self.float_y += step
            self.rect.y = int(self.float_y)
            remaining -= step

            stopped = False
            for tile in all_solid:
                if self.rect.colliderect(tile):
                    if self.dy >= 0 and self.rect.bottom > tile.top and self.rect.top < tile.top:
                        self.rect.bottom = tile.top  # land on top of the tile
                        self.float_y = float(self.rect.y)
                        self.dy = 0
                        stopped = True
                        landed = True
            if stopped or self.dy == 0:
                break

        # Only play the thud if the box was falling with some real speed
        if landed and falling_speed_before >= self._IMPACT_THRESHOLD:
            play('box_impact', CH_BOX)

        self._prev_dy = self.dy

    def settle_onto_floor(self, wall_tiles):
        """Snap the box down onto whatever tile is directly below it. Used after wrapping."""
        for tile in wall_tiles:
            if self.rect.colliderect(tile):
                if self.rect.bottom > tile.top and self.rect.top < tile.top:
                    self.rect.bottom = tile.top
                    self.float_y = float(self.rect.y)
                    self.dy = 0

    def wrap_position(self, camera=(0, 0), wall_tiles=None):
        """Teleport the box to the opposite side of the screen if it goes out of bounds."""
        cam_x, cam_y = camera
        left_edge   = cam_x
        right_edge  = cam_x + SCREEN_WIDTH
        top_edge    = cam_y
        bottom_edge = cam_y + SCREEN_HEIGHT

        wrapped = False

        # Vertical wrapping - always active
        if self.rect.top > bottom_edge:
            self.rect.bottom = top_edge  # fell off the bottom, appear at the top
            self.float_y = float(self.rect.y)
            wrapped = True
        elif self.rect.bottom < top_edge:
            self.rect.top = bottom_edge  # went off the top, appear at the bottom
            self.float_y = float(self.rect.y)
            wrapped = True

        # Horizontal wrapping - only while being carried (so unattended boxes don't slide off screen)
        if self.being_grabbed:
            if self.rect.left > right_edge:
                self.rect.right = left_edge
                wrapped = True
            elif self.rect.right < left_edge:
                self.rect.left = right_edge
                wrapped = True

        if wrapped:
            self.just_wrapped = True  # skip gravity this frame so we don't fall through the new floor
            if wall_tiles is not None:
                self.settle_onto_floor(wall_tiles)  # snap to ground at the new position

    def notify_wrapped_by_player(self, wall_tiles):
        """Called by the player when it wraps so the box can sync up without applying gravity."""
        self.just_wrapped = True
        self.settle_onto_floor(wall_tiles)

    def update(self, wall_tiles, camera=(0, 0), boxes=None):
        """Does what title says"""
        self.apply_gravity(wall_tiles, boxes)
        self.wrap_position(camera, wall_tiles)