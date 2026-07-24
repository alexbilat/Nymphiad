# Header
_author_ = "Alex Bilat"
_date_ = "2025/12/04"
_version_ = "1.0"
_filename_ = "main.py"
_description_ = "Main executable to run the game"

# Importing 
from settings import *
from MainMenu import *
from player import * 
from coin import *
from transition import *
from box import *
from spike import *
from switch import *
from smasher import *

# Initiate pygame stuff
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SHOWN)
pygame.display.set_caption('Nymphiad')
clock = pygame.time.Clock()

# Classes
main_menu = MainMenu()
player  = pygame.sprite.GroupSingle()
coin    = pygame.sprite.GroupSingle()
boxes   = pygame.sprite.Group()
spikes  = pygame.sprite.Group()
switches = pygame.sprite.Group()
smashers = pygame.sprite.Group()
current_level = None

# Spawn positions per level
player_spawns = {
    'level_1': (50, 50),
    'level_2': (40, 180),
    'level_3': (50, 60),
    'level_4': (76, 246),
    'level_5': (50, 270),
    'level_6': (150, 290),
    'level_7': (50, 300),
    'level_8': (140, 110 + 16),
    'level_9': (50, 50),
    'level_10': (50, 50),
    'level_11': (50, 50),
    'level_12': (50, 50),
    'level_13': (50, 50),
    'level_14': (50, 50),
    'level_15': (50, 50),
}

coin_spawns = {
    'level_1': (535, 190),
    'level_2': (535, 170), 
    'level_3': (568, 75),
    'level_4': (535, 237),
    'level_5': (566, 270),
    'level_6': (726, 139),
    'level_7': (55, 170),
    'level_8': (470, 105 + 16),
    'level_9': (120, 80),
    'level_10': (120, 80),
    'level_11': (120, 80),
    'level_12': (120, 80),
    'level_13': (120, 80),
    'level_14': (120, 80),
    'level_15': (120, 80),
}

box_spawns = {
    'level_1': None,
    'level_2': None,
    'level_3': [(200, 300), (368, 177)],
    'level_4': [(17, 122)],
    'level_5': None,
    'level_6': [(25, 240)],
    'level_7': [(330, 100)],
    'level_8': [(78, 110 + 16), (43 * 16, 8 * 16)],
    'level_9': [(50, 50)],
    'level_10': [(50, 50)],
    'level_11': [(50, 50)],
    'level_12': [(50, 50)],
    'level_13': [(50, 50)],
    'level_14': [(50, 50)],
    'level_15': [(50, 50)],
}

spacing = 32
spike_spawns = {
    'level_1': None,
    'level_2': None,
    'level_3': None,
    'level_4': None,
    'level_5': [(140, 322), (140 + spacing, 322), (140 + 4 * spacing, 322 - 32), (140 + 5 * spacing, 322 - 32), (140 + 6 * spacing, 322 - 32)],
    'level_6': [(204, 290), (204 + spacing, 290), (204 + 2 * spacing, 290), (204 + 7 * spacing, 290), (204 + 8 * spacing, 290), (784, 290), (784 + spacing, 290), (784 + 2 * spacing, 290), (784 + 3 * spacing, 290)],
    'level_7': [(77, 418), (77 + spacing, 418), (237, 450), (237 + spacing, 450), (237 + 2 * spacing, 450), (77, 34), (77 + spacing, 34)],
    'level_8': [(45, 322 + 16), (45 + spacing, 322 + 16), (45 + 2 * spacing, 322 + 16), (461, 322 + 16), (461 + spacing, 322 + 16)],
    'level_9': None,
    'level_10': None,
    'level_11': None,
    'level_12': None,
    'level_13': None,
    'level_14': None,
    'level_15': None,
}

# Switch spawn positions per level.
# Each entry is a list of (x, y, direction) tuples, or None for no switches.
# direction must be 'left' | 'right' | 'up' | 'down'.
switch_spawns = {
    'level_1': None,
    'level_2': None,
    'level_3': None,
    'level_4': None,
    'level_5': [(536, 110, 'right')],
    'level_6': [(237, 143, 'right')],
    'level_7': [(590, 304, 'up')],
    'level_8': [(170, 304 - 32 + 16, 'right')],
    'level_9': None,
    'level_10': None,
    'level_11': None,
    'level_12': None,
    'level_13': None,
    'level_14': None,
    'level_15': None,
}

# Smasher (crusher) spawn positions per level.
# Each entry is a list of (x, y, floor_y) tuples, or None for no smashers.
#   x, y     : world top-left of the head at rest (head is 64x32)
#   floor_y  : world Y the head's bottom slams down onto
smasher_spawns = {
    'level_1': None,
    'level_2': None,
    'level_3': None,
    'level_4': None,
    'level_5': None,
    'level_6': None,
    'level_7': [(398, 176, 336), (366, 16, 112)],
    'level_8': [(13 * 16 - 2, 16 + 16, (11 * 16) + 16), (23 * 16, (11 * 16) + 16, (19 * 16) + 16)],
    'level_9': None,
    'level_10': None,
    'level_11': None,
    'level_12': None,
    'level_13': None,
    'level_14': None,
    'level_15': None,
}

# How far the camera glides per switch press, per level.
# Levels not listed fall back to DEFAULT_SHIFT.
DEFAULT_SHIFT = 96
shift_amounts = {
    'level_6': 224,
    'level_7' : 128,
    'level_8' : 160
}

# Initial camera offset per level, in world pixels [x, y].
# Levels not listed start at [0, 0]. Positive y starts the view 128px lower.
DEFAULT_START_CAMERA = [0, 0]
start_cameras = {
    'level_7': [0, 128],
    'level_8' : [0, 16]
}

tile_size = 16
levels = {f'level_{i}': f'Tiled/level_{i}.tmx' for i in range(1, 16)} # Dict with every single level
loaded_maps = {}

level_order = [f'level_{i}' for i in range(1, 16)]
transition = Transition() # Init fading class


# CAMERA MODEL 
#
# Every entity (player, coin, boxes, spikes, switches) and every collision
# tile lives in WORLD coordinates — the full TMX map, which is much larger
# than the 640x360 window. The camera is the world-space position of the
# top-left corner of the visible window. We draw each thing at
# (world_pos - camera). When a switch fires, we glide the CAMERA to a new
# region of the world; the world itself never moves, so entities never need
# to be dragged along and there are no phantom-tile copies.


# Current camera (top-left of the visible window) per level, in world coords.
level_cameras = {f'level_{i}': [0, 0] for i in range(1, 16)}

# Smooth camera glide state per level.
level_cam_anim = {
    f'level_{i}': {
        'animating': False,
        'start_cam': [0, 0],
        'end_cam': [0, 0],
        'timer': 0,
        'duration': 15,  # 0.25s at 60fps
    }
    for i in range(1, 16)
}

def load_level(state):
    """Loads level and returns the map"""
    if state not in loaded_maps:
        loaded_maps[state] = pytmx.load_pygame(levels[state]) # Load
    return loaded_maps[state]

def draw_with_camera(screen, sprite, camera):
    """Blit a sprite at its world position minus the camera.

    Replaces group.draw(), which always blits at sprite.rect with no offset.
    Entities store world coords in .rect; we subtract the camera so they line
    up with the camera-offset tiles.
    """
    if sprite is None:
        return
    cam_x, cam_y = camera
    screen.blit(sprite.image, (sprite.rect.x - cam_x, sprite.rect.y - cam_y))

def draw_level(screen, tmx_data, tile_size, cam_x=0, cam_y=0):
    """Actually draw the level on the screen, using tiled tmx maps"""
    screen.fill((0, 0, 0))
    # The map (e.g. 80x60 tiles = 1280x960px) is much larger than the window
    # (640x360px). Tiles are stored in world coords; we draw each at its world
    # position minus the camera, so only the tiles inside the camera window are
    # visible. No wraparound copies — the camera just looks at a different part
    # of the single, real map.
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    screen.blit(tile, (x * tile_size - 2 - cam_x, y * tile_size - cam_y))

def get_collision_rects(tmx_data, tile_size):
    """Return collision tiles in pure WORLD coordinates (no camera offset).

    Physics runs entirely in world space, so collision rects carry no offset. The rest is offset. Tiled is good but the offsets make it complicated
    The camera only affects *drawing*, never collision.
    """
    rects = []
    for layer in tmx_data.layers:
        if isinstance(layer, pytmx.TiledTileLayer) and layer.name == 'collisions':
            for x, y, gid in layer:
                if gid:
                    rects.append(pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size))
    return rects

def get_current_camera(level_name):
    """Return the camera position, interpolated if a glide is in progress."""
    anim = level_cam_anim[level_name]

    if not anim['animating']:
        return level_cameras[level_name]

    progress = min(1.0, anim['timer'] / anim['duration'])
    cam_x = anim['start_cam'][0] + (anim['end_cam'][0] - anim['start_cam'][0]) * progress # This took so long to figure out
    cam_y = anim['start_cam'][1] + (anim['end_cam'][1] - anim['start_cam'][1]) * progress
    return [cam_x, cam_y]

def update_camera_animation(level_name):
    """Advance the camera glide. Call once per frame.

    Unlike the stupid old system, this moves ONLY the camera
    """
    anim = level_cam_anim[level_name]
    if not anim['animating']:
        return

    anim['timer'] += 1
    if anim['timer'] >= anim['duration']:
        anim['animating'] = False
        level_cameras[level_name] = anim['end_cam'][:] # I kept trying to move all the objects and the screen instead of just movin the camera. :(

def shift_level(level_name, direction, shift_amount):
    """Start a gradual camera glide in the given direction.

    The camera moves TOWARD the region being revealed: pressing a 'right'
    switch slides the camera right to show what's to the right. 
    """
    anim = level_cam_anim[level_name]

    dx, dy = 0, 0
    if direction == 'right':
        dx = shift_amount
    elif direction == 'left':
        dx = -shift_amount
    elif direction == 'down':
        dy = shift_amount
    elif direction == 'up':
        dy = -shift_amount

    anim['start_cam'] = level_cameras[level_name][:]
    anim['end_cam'] = [level_cameras[level_name][0] + dx, level_cameras[level_name][1] + dy]
    anim['timer'] = 0
    anim['animating'] = True

def init_level_entities(level_name):
    # Reset
    player.empty()
    coin.empty()
    boxes.empty()
    spikes.empty()
    switches.empty()
    smashers.empty()
    
    # Reset camera and glide animation when initializing (for deaths/level start)
    start_cam = start_cameras.get(level_name, DEFAULT_START_CAMERA)
    level_cameras[level_name] = start_cam[:]
    anim = level_cam_anim[level_name]
    anim['animating'] = False
    anim['start_cam'] = start_cam[:]
    anim['end_cam'] = start_cam[:]
    anim['timer'] = 0
    
    # Add everything to groups and get positions for the super awesome dictionaries at the top of this file
    player.add(Player(*player_spawns.get(level_name, (50, 50))))
    coin.add(Coin(*coin_spawns.get(level_name, (120, 80))))
    for pos in (box_spawns.get(level_name) or []):
        boxes.add(Box(*pos))
    for pos in (spike_spawns.get(level_name) or []):
        spikes.add(Spike(*pos))
    for entry in (smasher_spawns.get(level_name) or []):
        smashers.add(Smasher(*entry))
    for entry in (switch_spawns.get(level_name) or []):
        x, y, direction = entry
        switches.add(Switch(x, y, direction))

state = 'start' # Hi Mr Mac! Please change this 'state' variable to whatever you would like to skip levels if they're too hard (but try to figure them out first! It's fun :D 

# Main
running = True 


LAST_LEVEL     = 'level_8'         
HIGHSCORE_FILE = 'highscores.txt'

score_seconds  = 0.0   # Accumulated seconds
score_running  = False # True while we should tick the clock this frame

# Font init
score_font_large = pygame.font.Font('font/Greek-Freak.ttf', 20) 
score_font_small = pygame.font.Font('font/Greek-Freak.ttf', 14)

def draw_score(surface, seconds):
    """Render the timer in the bottom-right corner."""
    text = f'Time: {seconds:.1f}s'
    surf = score_font_large.render(text, True, (255, 255, 255))
    shadow = score_font_large.render(text, True, (0, 0, 0))
    x = SCREEN_WIDTH - surf.get_width() - 8
    y = SCREEN_HEIGHT - surf.get_height() - 8
    surface.blit(shadow, (x + 1, y + 1))
    surface.blit(surf,   (x,     y))

def save_highscore(name, seconds):
    """Append name + time to highscores.txt."""
    with open(HIGHSCORE_FILE, 'a') as f:
        f.write(f'{name},{seconds:.2f}\n')

def load_highscores():
    """Return list of (name, seconds) sorted best (lowest) first."""
    entries = []
    try:
        with open(HIGHSCORE_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if ',' in line:
                    parts = line.rsplit(',', 1)
                    try:
                        entries.append((parts[0], float(parts[1])))
                    except ValueError:
                        pass
    except FileNotFoundError:
        pass
    return sorted(entries, key=lambda e: e[1])


# To disable stuff when typing etc
name_entry_active  = False  # True while the name-entry overlay is shown
name_entry_text    = '' # what the player has typed so far
name_entry_done    = False # set True for one frame when Enter is pressed
name_entry_blink   = 0  # cursor blink timer
final_score_saved  = 0.0  # snapshot of score_seconds at beat time


# Main
while running:
    dt = clock.tick(60) / 1000.0   # 60 FPS but using dt so that it runs consistently on all computers
    mouse_pos = pygame.mouse.get_pos() # Self explanatory 

    # Allow the user to quit
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            break

        # To type high scores
        if name_entry_active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and name_entry_text.strip(): # When done
                name_entry_done = True
            elif event.key == pygame.K_BACKSPACE: # Delete character
                name_entry_text = name_entry_text[:-1]
            elif len(name_entry_text) < 16 and event.unicode.isprintable(): # Normal typing
                name_entry_text += event.unicode

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and state in levels and not name_entry_active: # Restart
            if not transition.active:
                transition.start(state)

    if name_entry_done: # Save high scores
        save_highscore(name_entry_text.strip(), final_score_saved)
        name_entry_active = False
        name_entry_done   = False
        name_entry_text   = ''
        score_seconds     = 0.0
        score_running     = False
        if not transition.active:
            play('final', CH_UI) # Music yay
            transition.start('start')

    if state == 'start' and running:
        # Reset score when returning to main menu
        score_seconds = 0.0
        score_running = False
        state = main_menu.update(screen, mouse_pos, event)

    elif state in levels and running:
        if current_level != state:
            current_level = state
            init_level_entities(state)
            play_music('game')
            # Start the clock on level_1 entry, keep it running on other levels
            if state == 'level_1':
                score_seconds = 0.0
            score_running = True
        
        # Set up levels and cam
        tmx_data = load_level(state)
        update_camera_animation(state)
        camera = get_current_camera(state)
        cam = (camera[0], camera[1])

        # Tick the score clock unless a transition or death is in progress
        p_sprite = player.sprite
        dying_now = p_sprite is not None and p_sprite.dying_by_spike
        if score_running and not transition.active and not dying_now and not name_entry_active:
            score_seconds += dt

        collision_tiles = get_collision_rects(tmx_data, tile_size) # Get tiles for physics
        draw_level(screen, tmx_data, tile_size, camera[0], camera[1]) # Let there be a map to play on

        # This part just draws every sprite and item
        for b in boxes.sprites():
            b.update(collision_tiles, cam, boxes)

        p = player.sprite
        for smasher in smashers.sprites():
            smasher.update(p.hitbox, p, collision_tiles, boxes)

        player.update(collision_tiles, boxes, cam, smashers)

        for b in boxes.sprites():
            draw_with_camera(screen, b, cam)
        draw_with_camera(screen, p, cam)

        for spike in spikes.sprites():
            spike.update(p.hitbox, p)
        for spike in spikes.sprites():
            draw_with_camera(screen, spike, cam)

        for smasher in smashers.sprites():
            draw_with_camera(screen, smasher, cam)
            smasher.draw_extras(screen, cam)

        switches.update()

        for switch in switches.sprites():
            if switch.check_collision(p.hitbox):
                p.freeze_movement()
                shift_level(state, switch.direction, shift_amounts.get(state, DEFAULT_SHIFT))
                switch.flip_direction()

        for switch in switches.sprites():
            draw_with_camera(screen, switch, cam)

        if p.death_animation_finished and not transition.active:
            transition.start(state)
            p.death_animation_finished = False

        if coin.sprite:
            coin.update()
            draw_with_camera(screen, coin.sprite, cam)

        if p.check_coin(coin.sprite):
            coin.empty()
            if state in level_order and not transition.active:
                next_idx   = level_order.index(state) + 1
                next_state = level_order[next_idx] if next_idx < len(level_order) else 'start'
                if state == LAST_LEVEL:
                    # Freeze the clock and show the name-entry overlay
                    score_running     = False
                    final_score_saved = score_seconds
                    name_entry_active = True
                    name_entry_text   = ''
                else:
                    play('coin_give', CH_UI)
                    transition.start(next_state)
        elif p.dancing and coin.sprite:
            coin.empty()

        draw_score(screen, score_seconds)

        if name_entry_active:
            name_entry_blink = (name_entry_blink + 1) % 60 # I like 60%, it looks good

            # Semi-transparent dark panel
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            # Heading
            heading = score_font_large.render('You beat the game!', True, (255, 220, 80))
            screen.blit(heading, heading.get_rect(center=(SCREEN_WIDTH // 2, 100)))

            time_line = score_font_large.render(f'Your time: {final_score_saved:.1f}s', True, (255, 255, 255))
            screen.blit(time_line, time_line.get_rect(center=(SCREEN_WIDTH // 2, 130)))

            prompt = score_font_small.render('Enter your name and press Enter:', True, (200, 200, 200))
            screen.blit(prompt, prompt.get_rect(center=(SCREEN_WIDTH // 2, 165)))

            # Input box
            cursor = '|' if name_entry_blink < 30 else ' '
            input_surf = score_font_large.render(name_entry_text + cursor, True, (255, 255, 255))
            box_rect = input_surf.get_rect(center=(SCREEN_WIDTH // 2, 200))
            pygame.draw.rect(screen, (60, 60, 80), box_rect.inflate(16, 8))
            pygame.draw.rect(screen, (180, 180, 220), box_rect.inflate(16, 8), 2)
            screen.blit(input_surf, box_rect)

            # Top scores
            scores = load_highscores()[:5]
            if scores:
                hs_title = score_font_small.render('Best times:', True, (180, 180, 180))
                screen.blit(hs_title, hs_title.get_rect(center=(SCREEN_WIDTH // 2, 240)))
                for i, (hs_name, hs_secs) in enumerate(scores):
                    col = (255, 215, 0) if i == 0 else (200, 200, 200)
                    line = score_font_small.render(f'{i+1}. {hs_name}  {hs_secs:.1f}s', True, col)
                    screen.blit(line, line.get_rect(center=(SCREEN_WIDTH // 2, 260 + i * 20)))

        transition.update(screen) # Transitions

        if transition.pending_state:
            state = transition.pending_state
            current_level = None
            if state == 'start':
                main_menu.state = 'start'

    pygame.display.update() # Update the display

pygame.quit()
exit()