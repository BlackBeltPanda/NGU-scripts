"""Contains functions for running a no equip challenge."""
from classes.features import Features
import coordinates as coords
import time

class Equipment(Features):
    """Contains functions for running a no equip challenge."""
    boss = 0

    def speedrun(self, duration):
        """Start a speedrun.

        Keyword arguments
        duration -- duration in minutes to run
        f -- feature object
        """
        diggers = [3, 2]
        self.nuke()
        time.sleep(2)
        self.fight()
        self.adventure(highest=True)
        time.sleep(2)
        rb_time = self.get_rebirth_time()
        while int(rb_time.timestamp.tm_min) < duration:
            self.wandoos(True)
            if not self.check_pixel_color(*coords.COLOR_BM_LOCKED) and not self.check_pixel_color(*coords.COLOR_BM_LOCKED_ALT):
                self.blood_magic(3)
            self.nuke()
            self.adventure(highest=True)
            """No point in wasting energy on augments or trying to cap diggers if we don't have the time machine unlocked"""
            if not self.check_pixel_color(*coords.COLOR_TM_LOCKED):
                self.time_machine(coords.INPUT_MAX, magic=True)
                self.gold_diggers(diggers)
                self.augments({"SS": 1}, coords.INPUT_MAX)
            rb_time = self.get_rebirth_time()
        self.pit()
        self.spin()
        boss = self.get_current_boss()
        return

    def start(self):
        """Challenge rebirth sequence.

        If you wish to edit the length or sequence of the rebirths; change the for-loop values
        and durations in the self.speedrun(duration) calls."""
        self.set_wandoos(0)  # wandoos 98, use 1 for meh
        self.toggle_auto_spells(number=True, drop=False, gold=True)

        for x in range(8):
            """Let's not waste too much time if we can't handle 3 minute rebirths"""
            if (x > 3 and boss < 30) or (x > 5 and boss < 37):
                break
            self.speedrun(3)
            if not self.check_challenge():
                return
            self.do_rebirth()
        for x in range(5):
            self.speedrun(7)
            if not self.check_challenge():
                return
            self.do_rebirth()
        for x in range(5):
            self.speedrun(12)
            if not self.check_challenge():
                return
            self.do_rebirth()
        for x in range(5):
            self.speedrun(60)
            if not self.check_challenge():
                return
            self.do_rebirth()
        return
