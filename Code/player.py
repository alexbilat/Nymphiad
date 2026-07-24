from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.player_standing_sheet = pygame.image.load('Images/Player/player-sheet0.png').convert_alpha()
        self.player_main_sheet = pygame.image.load('Images/Player/player-sheet1.png').convert_alpha()

        self.SPRITE_W = 32
        self.SPRITE_H = 32

        self.stand_frames = [
            self.player_standing_sheet.subsurface((103, 133, 32, 32)),
            self.player_standing_sheet.subsurface((137, 133, 32, 32)),
            self.player_standing_sheet.subsurface((103, 133, 32, 32)),
            self.player_standing_sheet.subsurface((137, 133, 32, 32)),
            self.player_standing_sheet.subsurface((171, 133, 32, 32)),
            self.player_standing_sheet.subsurface((205, 133, 32, 32)),
        ]
        self.stand_frames_flipped = [pygame.transform.flip(f, True, False) for f in self.stand_frames]

        self.smile_frames = [
            self.player_standing_sheet.subsurface((103, 167, 32, 32)),
            self.player_standing_sheet.subsurface((137, 167, 32, 32)),
            self.player_standing_sheet.subsurface((171, 167, 32, 32)),
            self.player_standing_sheet.subsurface((205, 167, 32, 32)),
            self.player_standing_sheet.subsurface((171, 167, 32, 32)),
        ]
        self.smile_frames_flipped = [pygame.transform.flip(f, True, False) for f in self.smile_frames]

        self.running_frames = [
            self.player_main_sheet.subsurface((35,  1,  32, 32)),
            self.player_main_sheet.subsurface((69,  1,  32, 32)),
            self.player_main_sheet.subsurface((103, 1,  32, 32)),
            self.player_main_sheet.subsurface((137, 1,  32, 32)),
            self.player_main_sheet.subsurface((171, 1,  32, 32)),
            self.player_main_sheet.subsurface((205, 1,  32, 32)),
            self.player_main_sheet.subsurface((1,   35, 32, 32)),
            self.player_main_sheet.subsurface((35,  35, 32, 32)),
        ]
        self.running_frames_flipped = [pygame.transform.flip(f, True, False) for f in self.running_frames]

        self.jump_frames = [
            self.player_main_sheet.subsurface((69,  35, 32, 32)),
            self.player_main_sheet.subsurface((103, 35, 32, 32)),
        ]
        self.jump_frames_flipped = [pygame.transform.flip(f, True, False) for f in self.jump_frames]

        self.fall_frames = [
            self.player_main_sheet.subsurface((137, 35, 32, 32)),
        ]
        self.fall_frames_flipped = [pygame.transform.flip(f, True, False) for f in self.fall_frames]

        self.land_frames = [
            self.player_main_sheet.subsurface((171, 35, 32, 32)),
            self.player_main_sheet.subsurface((205, 35, 32, 32)),
        ]
        self.land_frames_flipped = [pygame.transform.flip(f, True, False) for f in self.land_frames]

        self.dancing_frames = [
            self.player_main_sheet.subsurface((69,  103, 32, 32)),
            self.player_main_sheet.subsurface((103, 103, 32, 32)),
            self.player_main_sheet.subsurface((137, 103, 32, 32)),
            self.player_main_sheet.subsurface((171, 103, 32, 32)),
            self.player_main_sheet.subsurface((69,  103, 32, 32)),
            self.player_main_sheet.subsurface((103, 103, 32, 32)),
            self.player_main_sheet.subsurface((137, 103, 32, 32)),
            self.player_main_sheet.subsurface((171, 103, 32, 32)),
        ]

        self.pushing_frames = [
            self.player_main_sheet.subsurface((35,  69, 32, 32)),
            self.player_main_sheet.subsurface((69,  69, 32, 32)),
            self.player_main_sheet.subsurface((103, 69, 32, 32)),
            self.player_main_sheet.subsurface((137, 69, 32, 32)),
            self.player_main_sheet.subsurface((137, 69, 32, 32)),
            self.player_main_sheet.subsurface((171, 69, 32, 32)),
            self.player_main_sheet.subsurface((205, 69, 32, 32)),
            self.player_main_sheet.subsurface((1,  103, 32, 32)),
            self.player_main_sheet.subsurface((35, 103, 32, 32)),
        ]
        self.pushing_frames_flipped = [pygame.transform.flip(f, True, False) for f in self.pushing_frames]

        self.hold_frames = [
            self.player_main_sheet.subsurface((1, 69, 32, 32)),
        ]
        self.hold_frames_flipped = [pygame.transform.flip(f, True, False) for f in self.hold_frames]

        self.death_by_spike_frames = [
            self.player_main_sheet.subsurface((1, 205, 32, 32)),
            self.player_standing_sheet.subsurface((1,   1,  64, 64)),
            self.player_standing_sheet.subsurface((67,  1,  64, 64)),
            self.player_standing_sheet.subsurface((133, 1, 64, 64)),
            self.player_standing_sheet.subsurface((1,   67, 64, 64)),
            self.player_standing_sheet.subsurface((67, 67, 64, 64))
        ]
        self.death_by_spike_frames_flipped = [pygame.transform.flip(f, True, False) for f in self.death_by_spike_frames]

        # Animation state
        self.frame_index = 0
        self.frame_timer = 0
        self.FRAME_DELAY_STANDING = 15
        self.RUNNING_DELAY = 5
        self.AIRBORNE_DELAY = 4
        self.SPIKE_DEATH_DELAY = 4
        self.stand_cycle_count = 0
        self.SMILE_EVERY = 5
        self.playing_smile = False
        self._last_anim_state = None

        # Spike death
        self.dying_by_spike = False
        self.death_animation_finished = False
        self._spike_death_origin_y = 0
        self._spike_death_origin_x = 0
        self._spike_death_rise     = 0

        # Movement freeze (e.g., after touching a switch)
        self.movement_freeze_timer = 0

        # Movement state
        self.alive = True
        self.standing = True
        self.running = False
        self.jumping = False
        self.direction = 'right'
        self.landing = False
        self.dancing = False
        self.dance_done = False
        self.DANCE_DELAY = 8
        self.level_complete = False

        # Physics
        self.dx = 0
        self.dy = 0
        self.running_SPEED = 3.6
        self.JUMP_SPEED = -8.5
        self.GRAVITY = 0.5
        self.MAX_GRAVITY = 20
        self.falling = False

        # Box interaction
        self.BOX_SPEED = 1.5
        self.grabbed_box = None
        self.grab_offset = 0
        self.GRAB_RANGE = 10
        self.GRAB_CONTACT_TOL = 3

        # ── Audio state ──────────────────────────────────────────────────
        # Track previous states so we only fire sounds on transitions.
        self._was_running   = False   # run footstep loop
        self._was_jumping   = False   # jump sfx (fired once per jump)
        self._was_landing   = False   # land sfx
        self._was_dying     = False   # death_pop sfx
        self._was_dancing   = False   # coin_get sfx

        # Sprite rect (visual) and hitbox (collision)
        self.image = self.stand_frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = pygame.Rect(0, 0, 16, 24)
        self.hitbox.midbottom = self.rect.midbottom

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _sync_rect(self):
        self.rect.midbottom = self.hitbox.midbottom

    CORNER_SKIN = 3

    def _resolve_h(self, rect, dx, tiles):
        for tile in tiles:
            if rect.colliderect(tile):
                vertical_overlap = min(rect.bottom, tile.bottom) - max(rect.top, tile.top)
                if vertical_overlap <= self.CORNER_SKIN:
                    continue
                if dx > 0:
                    rect.right = tile.left
                elif dx < 0:
                    rect.left = tile.right
        return rect

    def _resolve_v(self, rect, dy, tiles):
        landed = False
        for tile in tiles:
            if rect.colliderect(tile):
                if dy >= 0 and rect.bottom > tile.top and rect.top < tile.top:
                    rect.bottom = tile.top
                    dy = 0
                    landed = True
                elif dy < 0 and rect.top < tile.bottom and rect.bottom > tile.bottom:
                    rect.top = tile.bottom
                    dy = 0
        return rect, dy, landed

    # ------------------------------------------------------------------
    # Screen wrapping
    # ------------------------------------------------------------------

    def wrap_position(self, grabbed_box=None, axis='both', camera=(0, 0), wall_tiles=None):
        cam_x, cam_y = camera
        wrapped_x = False
        wrapped_y = False
        offset_x = 0
        offset_y = 0

        left_edge   = cam_x
        right_edge  = cam_x + SCREEN_WIDTH
        top_edge    = cam_y
        bottom_edge = cam_y + SCREEN_HEIGHT

        if axis in ('x', 'both'):
            if self.hitbox.right < left_edge:
                offset_x = right_edge - self.hitbox.left
                self.hitbox.left = right_edge
                wrapped_x = True
            elif self.hitbox.left > right_edge:
                offset_x = left_edge - self.hitbox.right
                self.hitbox.right = left_edge
                wrapped_x = True

        if axis in ('y', 'both'):
            if self.hitbox.bottom < top_edge:
                offset_y = bottom_edge - self.hitbox.top
                self.hitbox.top = bottom_edge
                wrapped_y = True
            elif self.hitbox.top > bottom_edge:
                offset_y = top_edge - self.hitbox.bottom
                self.hitbox.bottom = top_edge
                wrapped_y = True

        self._sync_rect()
        return wrapped_x

    def _repin_grabbed_box(self, camera, wall_tiles=None):
        box = self.grabbed_box
        if box is None:
            return

        target_x = self.hitbox.x + self.grab_offset
        while target_x - self.hitbox.x > SCREEN_WIDTH / 2:
            target_x -= SCREEN_WIDTH
        while target_x - self.hitbox.x < -SCREEN_WIDTH / 2:
            target_x += SCREEN_WIDTH

        box.rect.x = target_x
        box.float_y = float(box.rect.y)
        box.just_wrapped = True
        if wall_tiles is not None:
            box.settle_onto_floor(wall_tiles)

    DEBUG_BOX = False

    def _debug_box_state(self, camera, tag=''):
        if not self.DEBUG_BOX:
            return
        cam_x, cam_y = camera
        left_edge  = cam_x
        right_edge = cam_x + SCREEN_WIDTH
        hb = self.hitbox
        gb = self.grabbed_box
        msg = (f"[{tag:10s}] cam_x={cam_x:7.1f} win=[{left_edge:.0f},{right_edge:.0f}] "
               f"player.x={hb.x:5d} L={hb.left:5d} R={hb.right:5d} dir={self.direction} "
               f"grab={'Y' if gb else 'N'}")
        if gb:
            on_screen = right_edge > gb.rect.left and left_edge < gb.rect.right
            pair_left  = min(hb.left, gb.rect.left)
            pair_right = max(hb.right, gb.rect.right)
            msg += (f" | box.x={gb.rect.x:5d} L={gb.rect.left:5d} R={gb.rect.right:5d} "
                    f"box.bottom={gb.rect.bottom:5d} box.dy={gb.dy:.1f} "
                    f"wrapped={'Y' if gb.just_wrapped else 'N'} on_screen={'Y' if on_screen else 'N'} "
                    f"pair=[{pair_left},{pair_right}]")
        print(msg)

    # ------------------------------------------------------------------
    # Animation
    # ------------------------------------------------------------------

    def animation(self):
        if self.dying_by_spike:
            anim_state = 'dying_by_spike'
        elif self.dancing:
            anim_state = 'dancing'
        elif self.jumping:
            anim_state = 'jumping'
        elif self.falling:
            anim_state = 'falling'
        elif self.landing:
            anim_state = 'landing'
        elif self.grabbed_box is not None and self.running:
            anim_state = 'pushing'
        elif self.grabbed_box is not None:
            anim_state = 'holding'
        elif self.running:
            anim_state = 'running'
        elif self.playing_smile and self.standing:
            anim_state = 'smile'
        else:
            anim_state = 'standing'

        if anim_state != self._last_anim_state:
            if anim_state not in ('jumping', 'landing', 'dancing'):
                self.frame_index = 0
                self.frame_timer = 0
            self._last_anim_state = anim_state

        self.frame_timer += 1

        if anim_state == 'dying_by_spike':
            if self.frame_timer >= self.SPIKE_DEATH_DELAY:
                self.frame_timer = 0
                if self.frame_index < len(self.death_by_spike_frames) - 1:
                    self.frame_index += 1
                else:
                    self.death_animation_finished = True

        elif anim_state == 'running':
            if self.frame_timer >= self.RUNNING_DELAY:
                self.frame_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.running_frames)

        elif anim_state == 'jumping':
            if self.frame_timer >= self.AIRBORNE_DELAY:
                self.frame_timer = 0
                if self.frame_index < len(self.jump_frames) - 1:
                    self.frame_index += 1

        elif anim_state == 'falling':
            if self.frame_timer >= self.AIRBORNE_DELAY:
                self.frame_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.fall_frames)

        elif anim_state == 'landing':
            if self.frame_timer >= self.AIRBORNE_DELAY:
                self.frame_timer = 0
                self.frame_index += 1
            if self.frame_index >= len(self.land_frames):
                self.landing = False
                self.frame_index = 0

        elif anim_state == 'dancing':
            if self.frame_timer >= self.DANCE_DELAY:
                self.frame_timer = 0
                self.frame_index += 1
            if self.frame_index >= len(self.dancing_frames):
                self.dancing = False
                self.dance_done = True
                self.level_complete = True
                self.frame_index = 0

        elif anim_state == 'pushing':
            if self.frame_timer >= self.RUNNING_DELAY:
                self.frame_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.pushing_frames)

        elif anim_state == 'holding':
            self.frame_index = 0

        elif anim_state in ('standing', 'smile'):
            if self.frame_timer >= self.FRAME_DELAY_STANDING:
                self.frame_timer = 0
                self.frame_index += 1
                if self.playing_smile:
                    if self.frame_index >= len(self.smile_frames):
                        self.playing_smile = False
                        self.frame_index = 0
                else:
                    if self.frame_index >= len(self.stand_frames):
                        self.frame_index = 0
                        self.stand_cycle_count += 1
                        if self.stand_cycle_count >= self.SMILE_EVERY:
                            self.stand_cycle_count = 0
                            self.playing_smile = True
                            self.frame_index = 0

        def pick(right_frames, left_frames):
            idx = self.frame_index % len(right_frames)
            self.image = right_frames[idx] if self.direction == 'right' else left_frames[idx]

        if anim_state == 'dying_by_spike':
            pick(self.death_by_spike_frames, self.death_by_spike_frames_flipped)
        elif anim_state == 'dancing':
            self.image = self.dancing_frames[self.frame_index % len(self.dancing_frames)]
        elif anim_state == 'jumping':
            pick(self.jump_frames, self.jump_frames_flipped)
        elif anim_state == 'falling':
            pick(self.fall_frames, self.fall_frames_flipped)
        elif anim_state == 'landing':
            pick(self.land_frames, self.land_frames_flipped)
        elif anim_state == 'pushing':
            pick(self.pushing_frames, self.pushing_frames_flipped)
        elif anim_state == 'holding':
            pick(self.hold_frames, self.hold_frames_flipped)
        elif anim_state == 'running':
            pick(self.running_frames, self.running_frames_flipped)
        elif anim_state == 'smile':
            pick(self.smile_frames, self.smile_frames_flipped)
        else:
            pick(self.stand_frames, self.stand_frames_flipped)

    # ------------------------------------------------------------------
    # Audio helpers  (called from update() at the end of each frame)
    # ------------------------------------------------------------------

    def _update_audio(self):
        """Fire one-shot sounds on state transitions; loop run sound."""

        # ── jump ─────────────────────────────────────────────────────────
        if self.jumping and not self._was_jumping:
            play('jump', CH_PLAYER)
        self._was_jumping = self.jumping

        # ── land ─────────────────────────────────────────────────────────
        if self.landing and not self._was_landing:
            play('land', CH_PLAYER)
        self._was_landing = self.landing

        # ── run footstep loop ─────────────────────────────────────────────
        # Use the 'run' sound looped on CH_PLAYER while on the ground and
        # moving.  Stop it as soon as the player is airborne or still.
        is_running_grounded = self.running and self.standing
        if is_running_grounded and not self._was_running:
            play('run', CH_PLAYER, loops=-1, volume=0.2)
        elif not is_running_grounded and self._was_running:
            # Only stop if the channel is playing the run sound
            # (jump sound may have started on the same channel - let it play).
            if not self.jumping:
                CH_PLAYER.stop()
        self._was_running = is_running_grounded

        # ── death pop ────────────────────────────────────────────────────
        if self.dying_by_spike and not self._was_dying:
            play('death_pop', CH_PLAYER)
        self._was_dying = self.dying_by_spike

        # ── coin get / dancing ───────────────────────────────────────────
        if self.dancing and not self._was_dancing:
            play('coin_get', CH_UI)
        self._was_dancing = self.dancing

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    def check_coin(self, coin_sprite):
        if coin_sprite and not self.dancing and not self.level_complete:
            if self.hitbox.colliderect(coin_sprite.rect):
                self.start_dance()
                return False
        if self.level_complete:
            self.level_complete = False
            return True
        return False

    def start_dance(self):
        self.dancing = True
        self.dance_done = False
        self.frame_index = 0
        self.frame_timer = 0
        self.running = False
        self.jumping = False
        self.falling = False
        self.landing = False
        self.dy = 0

    def trigger_spike_death(self):
        """Begin the death_by_spike animation."""
        if self.dying_by_spike:
            return
        self.dying_by_spike = True
        self.death_animation_finished = False
        self._spike_death_origin_x = self.rect.centerx
        self._spike_death_origin_y = self.rect.bottom
        self._spike_death_rise     = 0
        self.frame_index = 0
        self.frame_timer = 0
        self.running = False
        self.jumping = False
        self.falling = False
        self.landing = False
        self.dancing = False
        self.dy = 0

    def freeze_movement(self, duration_ticks=15):
        self.movement_freeze_timer = duration_ticks
        self.dx = 0
        self.dy = 0
        self.running = False
        self.jumping = False
        self.falling = False
        self.landing = False

    # ------------------------------------------------------------------
    # Main update
    # ------------------------------------------------------------------

    def update(self, wall_tiles, boxes=None, camera=(0, 0), smashers=None):
        if self.movement_freeze_timer > 0:
            self.movement_freeze_timer -= 1

        if self.dying_by_spike:
            self._spike_death_rise += 1
            self.animation()
            old_midbottom = (self._spike_death_origin_x, self._spike_death_origin_y - self._spike_death_rise)
            self.rect.size = self.image.get_size()
            self.rect.midbottom = old_midbottom
            self._update_audio()
            return

        box_list = boxes.sprites() if boxes else []
        smasher_list = smashers.sprites() if smashers else []
        self._update_grab(box_list, camera)
        self._read_input()
        if self.movement_freeze_timer == 0:
            self._move_horizontal(wall_tiles, box_list)
            self._debug_box_state(camera, 'pre-wrap')
            box_wrapped = self.grabbed_box.just_wrapped if self.grabbed_box else False
            player_wrapped = self.wrap_position(self.grabbed_box, axis='x', camera=camera, wall_tiles=wall_tiles)
            if self.grabbed_box is not None:
                if player_wrapped or box_wrapped:
                    self._repin_grabbed_box(camera, wall_tiles)
                else:
                    self.grab_offset = self.grabbed_box.rect.x - self.hitbox.x
            self._debug_box_state(camera, 'post-wrap')
            self._move_vertical(wall_tiles, box_list, smasher_list)
        self.animation()
        self._sync_rect()
        self.wrap_position(self.grabbed_box, axis='y', camera=camera, wall_tiles=wall_tiles)
        self._update_audio()

    # ------------------------------------------------------------------
    # Grab / release
    # ------------------------------------------------------------------

    def _update_grab(self, box_list, camera=(0, 0)):
        if self.dancing:
            if self.grabbed_box:
                self.grabbed_box.being_grabbed = False
            self.grabbed_box = None
            return

        keys = pygame.key.get_pressed()
        if not keys[pygame.K_x]:
            if self.grabbed_box:
                self.grabbed_box.being_grabbed = False
            self.grabbed_box = None
            return

        if self.grabbed_box and self.grabbed_box in box_list:
            hb = self.hitbox
            bx = self.grabbed_box.rect
            cam_x = camera[0]
            pc = (hb.centerx - cam_x) % SCREEN_WIDTH
            bc = (bx.centerx - cam_x) % SCREEN_WIDTH
            d = abs(pc - bc)
            center_dist = min(d, SCREEN_WIDTH - d)
            adjacency = (hb.width + bx.width) / 2 + self.GRAB_RANGE
            if center_dist > adjacency:
                self.grabbed_box.being_grabbed = False
                self.grabbed_box = None
            else:
                raw = (bc - pc)
                if raw > SCREEN_WIDTH / 2:
                    raw -= SCREEN_WIDTH
                elif raw < -SCREEN_WIDTH / 2:
                    raw += SCREEN_WIDTH
                self.direction = 'right' if raw >= 0 else 'left'
        else:
            if self.grabbed_box:
                self.grabbed_box.being_grabbed = False
            self.grabbed_box = None
            probe = self.hitbox.inflate(self.GRAB_CONTACT_TOL * 2, 0)
            for box in box_list:
                if not probe.colliderect(box.rect):
                    continue
                vertical_overlap = min(self.hitbox.bottom, box.rect.bottom) - max(self.hitbox.top, box.rect.top)
                if vertical_overlap <= self.CORNER_SKIN:
                    continue
                self.grabbed_box = box
                self.grabbed_box.being_grabbed = True
                self.grab_offset = box.rect.x - self.hitbox.x
                break

    # ------------------------------------------------------------------
    # Read input
    # ------------------------------------------------------------------

    def _read_input(self):
        self.dx = 0
        if self.dancing or self.movement_freeze_timer > 0:
            return

        keys = pygame.key.get_pressed()

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.dx = self.running_SPEED
            self.running = True
            if self.grabbed_box is None:
                self.direction = 'right'
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.dx = -self.running_SPEED
            self.running = True
            if self.grabbed_box is None:
                self.direction = 'left'
        else:
            self.running = False

        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.standing and self.grabbed_box is None:
            self.dy = self.JUMP_SPEED
            self.jumping = True
            self.standing = False
            self.falling = False
            self.landing = False
            self.frame_index = 0
            self.frame_timer = 0

        if self.jumping and self.dy >= 0:
            self.jumping = False
            self.falling = True

        if self.grabbed_box is not None and self.dx != 0:
            self.dx = self.BOX_SPEED if self.dx > 0 else -self.BOX_SPEED

    # ------------------------------------------------------------------
    # Horizontal movement
    # ------------------------------------------------------------------

    def _move_horizontal(self, wall_tiles, box_list):
        if self.dx == 0:
            return

        player_x_before = self.hitbox.x
        self.hitbox.x += int(self.dx)
        self._resolve_h(self.hitbox, self.dx, wall_tiles)

        for box in box_list:
            if box is self.grabbed_box:
                continue
            if self.hitbox.colliderect(box.rect):
                vertical_overlap = min(self.hitbox.bottom, box.rect.bottom) - max(self.hitbox.top, box.rect.top)
                if vertical_overlap <= self.CORNER_SKIN:
                    continue
                if self.dx > 0:
                    self.hitbox.right = box.rect.left
                elif self.dx < 0:
                    self.hitbox.left = box.rect.right

        actual_player_dx = self.hitbox.x - player_x_before

        if actual_player_dx == 0:
            self.running = False

        if self.grabbed_box is None or actual_player_dx == 0:
            return

        box = self.grabbed_box
        box_dx = self.BOX_SPEED if actual_player_dx > 0 else -self.BOX_SPEED
        box.rect.x += int(box_dx)

        for tile in wall_tiles:
            if box.rect.colliderect(tile):
                vertical_overlap = min(box.rect.bottom, tile.bottom) - max(box.rect.top, tile.top)
                if vertical_overlap <= self.CORNER_SKIN:
                    continue
                if box_dx > 0:
                    overlap = box.rect.right - tile.left
                    box.rect.right = tile.left
                    self.hitbox.x -= overlap
                    self._resolve_h(self.hitbox, self.dx, wall_tiles)
                elif box_dx < 0:
                    overlap = tile.right - box.rect.left
                    box.rect.left = tile.right
                    self.hitbox.x += overlap
                    self._resolve_h(self.hitbox, self.dx, wall_tiles)

        for other in box_list:
            if other is box:
                continue
            if box.rect.colliderect(other.rect):
                vertical_overlap = min(box.rect.bottom, other.rect.bottom) - max(box.rect.top, other.rect.top)
                if vertical_overlap <= self.CORNER_SKIN:
                    continue
                if box_dx > 0:
                    overlap = box.rect.right - other.rect.left
                    box.rect.right = other.rect.left
                    self.hitbox.x -= overlap
                    self._resolve_h(self.hitbox, self.dx, wall_tiles)
                elif box_dx < 0:
                    overlap = other.rect.right - box.rect.left
                    box.rect.left = other.rect.right
                    self.hitbox.x += overlap
                    self._resolve_h(self.hitbox, self.dx, wall_tiles)

        box.float_y = float(box.rect.y)

    # ------------------------------------------------------------------
    # Vertical movement
    # ------------------------------------------------------------------

    def _move_vertical(self, wall_tiles, box_list, smasher_list=None):
        if smasher_list is None:
            smasher_list = []

        was_standing = self.standing

        carried = getattr(self, '_riding_smasher', None)
        if carried is not None and carried in smasher_list:
            dy_platform = carried.rect.y - getattr(self, '_riding_smasher_prev_y', carried.rect.y)
            if dy_platform != 0:
                self.hitbox.y += dy_platform

        self.standing = False
        self.dy = 1 if was_standing else min(self.dy + self.GRAVITY, self.MAX_GRAVITY)

        all_solid = list(wall_tiles) + [b.rect for b in box_list] + [s.rect for s in smasher_list]
        was_falling = self.falling

        remaining = int(self.dy)
        step_sign = 1 if remaining > 0 else -1
        landed = False
        while remaining != 0:
            step = step_sign * min(abs(remaining), TILE_SIZE)
            self.hitbox.y += step
            self.hitbox, self.dy, step_landed = self._resolve_v(self.hitbox, self.dy, all_solid)
            if step_landed:
                landed = True
            if step_landed or self.dy == 0:
                break
            remaining -= step

        if landed:
            self.standing = True
            self.jumping = False
            if was_falling and not self.landing:
                self.landing = True
                self.frame_index = 0
                self.frame_timer = 0
            self.falling = False
        elif self.dy > 0 and not self.jumping:
            self.falling = True

        self._riding_smasher = None
        if self.standing:
            for s in smasher_list:
                if (self.hitbox.right > s.rect.left and self.hitbox.left < s.rect.right
                        and abs(self.hitbox.bottom - s.rect.top) <= 2):
                    self._riding_smasher = s
                    self._riding_smasher_prev_y = s.rect.y
                    break