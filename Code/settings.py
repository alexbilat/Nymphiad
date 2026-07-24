# Header
_author_ = "Alex Bilat"
_date_ = "2025/12/04"
_version_ = "1.0"
_filename_ = "settings.py"
_description_ = "Settings folder for game"

# Importing
import pygame  # Must run pip install pygame-ce
import math
import pytmx # type:ignore


# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 360
TILE_SIZE = 16

# AUDIO
# Initialise the mixer before loading any sounds.  All other modules import
# settings so this runs exactly once, before any Sound object is created.

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init() # init pygame music

def _load(name):
    """Load Audio/<name>.ogg, return None silently if the file is missing."""
    try:
        return pygame.mixer.Sound(f'Audio/{name}.ogg')
    except Exception:
        return None

# All sounds keyed by name. Access via sounds['jump'].play() etc.
sounds = {
    'box_impact'      : _load('box_impact'),
    'bullet_impact'   : _load('bullet_impact'),
    'coin_get'        : _load('coin_get'),
    'coin_give'       : _load('coin_give'),
    'death_burn'      : _load('death_burn'),
    'death_electro'   : _load('death_electro'),
    'death_pop'       : _load('death_pop'),
    'dive'            : _load('dive'),
    'final'           : _load('final'),
    'game'            : _load('game'),
    'jump'            : _load('jump'),
    'land'            : _load('land'),
    'logo_impact'     : _load('logo_impact'),
    'logo_launch'     : _load('logo_launch'),
    'menu'            : _load('menu'),
    'run'             : _load('run'),
    'select'          : _load('select'),
    'shoot'           : _load('shoot'),
    'smasher_fall'    : _load('smasher_fall'),
    'smasher_impact'  : _load('smasher_impact'),
    'smasher_return'  : _load('smasher_return'),
    'spikes_click'    : _load('spikes_click'),
    'spikes_in'       : _load('spikes_in'),
    'spikes_out'      : _load('spikes_out'),
    'switch'          : _load('switch'),
    'type'            : _load('type'),
    'push'            : _load('push')
}

# Dedicated mixer channels so sounds never cut each other off unexpectedly. 
CH_MUSIC   = pygame.mixer.Channel(0)   # looping background music
CH_PLAYER  = pygame.mixer.Channel(1)   # jump / land / run
CH_HAZARD  = pygame.mixer.Channel(2)   # spikes / smasher
CH_UI      = pygame.mixer.Channel(3)   # menu / select / coin
CH_BOX     = pygame.mixer.Channel(4)   # box impacts
CH_SWITCH  = pygame.mixer.Channel(5)   # switch flip
# This took a long time to format, but it makes it easy to read ^^^

def play(name, channel=None, loops=0, volume=1.0):
    """Play a sound by name. Silently skips missing sounds.

    channel  - one of the CH_* constants above, or None to use find_channel().
    loops    - pygame loops arg (0 = once, -1 = forever).
    volume   - 0.0 - 1.0.
    """
    snd = sounds.get(name)
    if snd is None:
        return  # file probably missing, no crash
    snd.set_volume(volume)
    if channel is not None:
        channel.play(snd, loops=loops)
    else:
        snd.play(loops=loops)  # let pygame pick a free channel

def play_music(name, loops=-1, volume=0.5):
    """Start looping background music on CH_MUSIC, replacing any current track."""
    snd = sounds.get(name)
    if snd is None:
        return
    if CH_MUSIC.get_sound() is snd and CH_MUSIC.get_busy():
        return  # already playing this track, don't restart it
    snd.set_volume(volume)
    CH_MUSIC.play(snd, loops=loops)

def stop_music():
    CH_MUSIC.stop()