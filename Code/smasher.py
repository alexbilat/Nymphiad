from settings import *

class Smasher(pygame.sprite.Sprite):
    """
    Ceiling-mounted crusher that drops on the player when they pass beneath it.
    Five states: idle -> falling -> impact -> returning -> recharge -> idle
    It acts as a rideable platform on the way back up — but get caught under it and you're done.
    """

    BODY_W = 64
    BODY_H = 32

    FALL_SPEED   = 4   # pixels per tick on the way down — fast and scary
    RETURN_SPEED = 1   # pixels per tick on the way back up — slow and taunting

    IMPACT_HOLD   = 90   # ticks to sit at the bottom before returning (1.5 seconds at 60fps)
    RECHARGE_HOLD = 15   # ticks to wait at the top before becoming active again

    TRIGGER_MARGIN = 4   # how many pixels below the smasher the player needs to be to trigger it
    CRUSH_SKIN = 4       # overlap tolerance for the crush check — so it doesn't fire on a pixel

    def __init__(self, x, y, floor_y):
        super().__init__()

        body_sheet = pygame.image.load('Images/Smasher/smasher-sheet0.png').convert_alpha()
        self.chain_img = pygame.image.load('Images/Smasher/smasher_chain.png').convert_alpha()

        bw, bh = self.BODY_W, self.BODY_H
        self.idle_frame   = body_sheet.subsurface((1,  1, bw, bh))   # normal hanging look
        self.impact_frame = body_sheet.subsurface((1, 35, bw, bh))   # squished face after hitting the floor

        self.image = self.idle_frame
        self.rect  = self.image.get_rect(topleft=(x, y))

        self.top_y   = y          # rest position at the top (where it returns to)
        self.floor_y = floor_y    # world Y the bottom of the head slams down to

        # Chain anchor is above the smasher — used for drawing the chain links
        self.anchor_x = self.rect.centerx
        self.anchor_y = self.top_y - self.chain_img.get_height()

        self._state = 'idle'
        self._timer = 0

        self.just_impacted = False  # True for one frame right when it hits the floor

    def _set_state(self, new_state):
        """Switch to a new state and reset the timer"""
        self._state = new_state
        self._timer = 0

    def _within_column(self, player_hitbox):
        """True if the player is horizontally under this smasher"""
        return (player_hitbox.right > self.rect.left and
                player_hitbox.left < self.rect.right)

    def _player_below(self, player_hitbox, wall_tiles=None):
        """True if the player is in the column below the smasher with no tiles in the way."""
        below = player_hitbox.top >= self.rect.bottom - self.TRIGGER_MARGIN
        if not (self._within_column(player_hitbox) and below):
            return False

        # Check for blocking tiles between the smasher and the player
        if wall_tiles:
            gap_top    = self.rect.bottom
            gap_bottom = player_hitbox.top
            for tile in wall_tiles:
                if tile.right <= self.rect.left or tile.left >= self.rect.right:
                    continue  # tile isn't in our column
                if tile.top >= gap_bottom or tile.bottom <= gap_top:
                    continue  # tile isn't between us and the player
                return False  # there's a wall in the way, can't see the player

        return True

    def _vertical_overlap(self, player_hitbox):
        """How many pixels the smasher and player overlap vertically"""
        return (min(player_hitbox.bottom, self.rect.bottom) -
                max(player_hitbox.top, self.rect.top))

    def _effective_floor(self, boxes):
        """Find the floor Y, adjusted down if a box is sitting in our column above it."""
        floor = self.floor_y
        if boxes is not None:
            for box in boxes.sprites():
                if box.rect.right <= self.rect.left or box.rect.left >= self.rect.right:
                    continue  # box isn't in our column
                if box.rect.top <= self.rect.top:
                    continue  # box is above us, ignore it
                if box.rect.top < floor:
                    floor = box.rect.top  # box is lower than our floor, land on the box instead
        return floor

    def update(self, player_hitbox, player=None, wall_tiles=None, boxes=None):
        self.just_impacted = False  # reset every frame, only True the instant we hit the floor

        effective_floor = self._effective_floor(boxes)  # recalculate in case a box moved

        if self._state == 'idle':
            self.image = self.idle_frame
            if self._player_below(player_hitbox, wall_tiles):
                play('smasher_fall', CH_HAZARD)  # ominous whoosh as it starts to fall
                self._set_state('falling')

        elif self._state == 'falling':
            self.image = self.idle_frame
            self.rect.y += self.FALL_SPEED
            if self.rect.bottom >= effective_floor:
                self.rect.bottom = effective_floor  # snap to the floor exactly
                self.just_impacted = True
                play('smasher_impact', CH_HAZARD)  # satisfying thud
                self._set_state('impact')
            self._crush_from_below(player_hitbox, player)  # kill anyone in the way on the way down

        elif self._state == 'impact':
            self.image = self.impact_frame  # squished face while it sits at the bottom
            self._crush_from_below(player_hitbox, player)  # still deadly at the bottom
            self._timer += 1
            if self._timer >= self.IMPACT_HOLD:
                play('smasher_return', CH_HAZARD)  # creaking as it goes back up
                self._set_state('returning')

        elif self._state == 'returning':
            self.image = self.idle_frame
            self.rect.y -= self.RETURN_SPEED  # slowly creep back to the ceiling
            self._crush_from_above(player_hitbox, player, wall_tiles)  # kill anyone riding it into the ceiling
            if self.rect.top <= self.top_y:
                self.rect.top = self.top_y  # snap back to rest position
                self._set_state('recharge')

        elif self._state == 'recharge':
            self.image = self.idle_frame
            self._timer += 1
            if self._timer >= self.RECHARGE_HOLD:
                self._set_state('idle')  # ready to drop again, sucker

    def _crush_from_below(self, player_hitbox, player):
        """Kill the player if the smasher is descending onto them from above."""
        if player is None:
            return
        if not self._within_column(player_hitbox):
            return
        if not player_hitbox.colliderect(self.rect):
            return
        # Only crush if the smasher is genuinely pushing down on the player's top
        crushing = (self.rect.bottom > player_hitbox.top + self.CRUSH_SKIN and
                    self.rect.top <= player_hitbox.top and
                    player_hitbox.centery > self.rect.top)
        if crushing:
            player.trigger_spike_death()

    def _crush_from_above(self, player_hitbox, player, wall_tiles):
        """Kill the player if they're riding the smasher and it squishes them into the ceiling."""
        if player is None:
            return
        if not self._within_column(player_hitbox):
            return

        # Player is riding if their feet are near the top of the smasher
        riding_on_top = (player_hitbox.bottom > self.rect.top - self.CRUSH_SKIN and
                         player_hitbox.bottom <= self.rect.bottom and
                         player_hitbox.centery < self.rect.centery)
        if not riding_on_top:
            return

        # If the smasher has returned all the way to the top, crush immediately
        if self.rect.top <= self.top_y + self.RETURN_SPEED:
            player.trigger_spike_death()
            return

        # Also crush if the player's head is bumping into a ceiling tile
        if wall_tiles is not None:
            head_probe = player_hitbox.copy()
            head_probe.height = self.CRUSH_SKIN + 1
            head_probe.bottom = player_hitbox.top + 1
            for tile in wall_tiles:
                if head_probe.colliderect(tile):
                    player.trigger_spike_death()
                    return

    def draw_extras(self, screen, camera):
        """Draw the chain links above the smasher body. Called separately from the sprite group."""
        cam_x, cam_y = camera
        chain_w = self.chain_img.get_width()
        chain_h = self.chain_img.get_height()

        # Stack chain images from just above the body up to the anchor point
        chain_x = self.rect.centerx - chain_w // 2 - cam_x
        top = self.anchor_y
        y = self.rect.top - chain_h
        while y + chain_h > top:
            screen.blit(self.chain_img, (chain_x, y - cam_y))
            y -= chain_h  # step upward one chain link at a time