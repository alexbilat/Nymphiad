from settings import *

class Transition:
    """Fade-to-black then fade-in overlay.
    Call transition.start(next_state) to begin.
    Call transition.update(screen) every frame AFTER drawing the scene.
    Read transition.pending_state (non-None for one frame) to know when to swap.
    """
    FADE_SPEED = 30  # alpha change per frame - lower = slower fade

    def __init__(self):
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.overlay.fill((0, 0, 0))  # solid black rectangle we fade in/out
        self.alpha = 0                # starts fully transparent
        self.active = False           # True while a fade is happening
        self._fading_out = False      # True = getting darker, False = getting lighter
        self._next_state = None       # the state to switch to at the darkest point
        self.pending_state = None     # main loop reads this to know when to swap states

    def start(self, next_state):
        """Kick off a fade-out -> swap -> fade-in sequence."""
        if self.active:
            return  # never interrupt a fade that's already in progress
        self._next_state = next_state
        self._fading_out = True
        self.alpha = 0        # start transparent and fade to black
        self.active = True
        self.pending_state = None

    def update(self, screen):
        """Advance the fade and draw the overlay. Call after the scene is drawn."""
        self.pending_state = None  # reset every frame so it only fires once
        if not self.active:
            return

        if self._fading_out:
            self.alpha = min(255, self.alpha + self.FADE_SPEED)  # get darker
            if self.alpha >= 255:
                # Fully black - this is the moment we swap states
                self.pending_state = self._next_state
                self._fading_out = False  # now start fading back in
        else:
            self.alpha = max(0, self.alpha - self.FADE_SPEED)  # get lighter
            if self.alpha <= 0:
                self.active = False  # fully transparent again, we're done

        self.overlay.set_alpha(self.alpha)
        screen.blit(self.overlay, (0, 0))  # draw the black overlay on top of the scene