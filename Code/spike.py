from settings import *

class Spike(pygame.sprite.Sprite):
    """
    Floor spikes that react to the player's proximity.
    They wait a moment, then shoot up - giving the player just enough time to regret their life choices.
    """

    FRAME_W = 32
    FRAME_H = 16

    TRIGGER_DELAY  = 16  # ticks the player must be nearby before spikes start extending
    EXTEND_DELAY   = 5   # ticks between frames during the extend animation
    EXTENDED_DELAY = 8   # not currently used but kept for reference
    RETRACT_DELAY  = 5   # ticks between frames during the retract animation

    def __init__(self, x, y):
        super().__init__()

        # Two sheets - sheet0 has extend/retract frames, sheet1 has the fully-extended frame
        sheet0 = pygame.image.load('Images/Spikes/spikes-sheet0.png').convert_alpha()
        sheet1 = pygame.image.load('Images/Spikes/spikes-sheet1.png').convert_alpha()

        fw, fh = self.FRAME_W, self.FRAME_H

        # Frames for popping up
        self.extend_frames = [
            sheet0.subsurface((0,  0, fw, fh)),
            sheet0.subsurface((0, 16, fw, fh)),
            sheet0.subsurface((0, 32, fw, fh)),
        ]
        # Single frame for when the spikes are fully out and being menacing
        self.extended_frames = [
            sheet1.subsurface((0,  0, fw, fh)),
        ]
        # Frames for going back down (roughly the extend animation in reverse)
        self.retract_frames = [
            sheet0.subsurface((0, 48, fw, fh)),
            sheet1.subsurface((0, 16, fw, fh)),
            sheet0.subsurface((0,  0, fw, fh)),
        ]

        self.image = self.extend_frames[0]  # start showing the flat (hidden) frame
        self.rect  = self.image.get_rect(topleft=(x, y))

        self._state         = 'idle'   # idle -> extending -> extended -> retracting -> idle
        self._frame_index   = 0
        self._frame_timer   = 0
        self._trigger_timer = 0        # counts how long the player has been nearby
        self._death_triggered = False  # so we only kill the player once per extend cycle

    def _set_state(self, new_state):
        """Switch states and reset all the timers and counters"""
        self._state         = new_state
        self._frame_index   = 0
        self._frame_timer   = 0
        self._trigger_timer = 0
        self._death_triggered = False

    def _player_nearby(self, player_hitbox):
        """True if the player is touching this spike's rect"""
        return player_hitbox.colliderect(self.rect)

    def update(self, player_hitbox, player=None):
        self._frame_timer += 1
        nearby = self._player_nearby(player_hitbox)

        if self._state == 'idle':
            self.image = self.extend_frames[0]  # show the flat/hidden frame while waiting
            if nearby:
                self._trigger_timer += 1
                if self._trigger_timer >= self.TRIGGER_DELAY:
                    play('spikes_click', CH_HAZARD)  # ominous click before they shoot up
                    self._set_state('extending')
            else:
                self._trigger_timer = 0  # player left, reset the countdown

        elif self._state == 'extending':
            if self._frame_index == 0 and self._frame_timer == 1:
                play('spikes_out', CH_HAZARD)  # woosh sound as they come out
            if not self._death_triggered and nearby:
                self._death_triggered = True  # only kill once, even if player stays on them
                if player is not None:
                    player.trigger_spike_death()
            delay = self.EXTEND_DELAY
            if self._frame_timer >= delay:
                self._frame_timer = 0
                self._frame_index += 1
                if self._frame_index >= len(self.extend_frames):
                    self._set_state('extended')  # done extending, now just sit there
                    return
            self.image = self.extend_frames[self._frame_index]

        elif self._state == 'extended':
            self.image = self.extended_frames[0]
            if nearby and player is not None:
                player.trigger_spike_death()  # still deadly while fully out
            if not nearby:
                self._set_state('retracting')  # player left, safe to go back down

        elif self._state == 'retracting':
            if self._frame_index == 0 and self._frame_timer == 1:
                play('spikes_in', CH_HAZARD)  # satisfying click as they retract
            delay = self.RETRACT_DELAY
            if self._frame_timer >= delay:
                self._frame_timer = 0
                self._frame_index += 1
                if self._frame_index >= len(self.retract_frames):
                    self._set_state('idle')  # fully retracted, ready to ruin someone's day again
                    return
            self.image = self.retract_frames[self._frame_index]
            if nearby:
                self._set_state('extending')  # player came back mid-retract, fire again