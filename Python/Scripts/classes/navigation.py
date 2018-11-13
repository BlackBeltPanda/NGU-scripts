"""Navigation class handles navigation through the menus."""
from classes.inputs import Inputs
import ngucon as ncon
import time


class Navigation(Inputs):
    """Navigate through menus."""

    menus = ncon.MENUITEMS
    equipment = ncon.EQUIPMENTSLOTS
    current_menu = ""

    def menu(self, target):
        """Navigate through main menu."""
        if Navigation.current_menu == "target":
            return
        y = ncon.MENUOFFSETY + ((self.menus.index(target) + 1) *
                                ncon.MENUDISTANCEY)
        self.click(ncon.MENUOFFSETX, y)
        time.sleep(ncon.LONG_SLEEP)
        Navigation.current_menu = target

    def input_box(self):
        """Click input box."""
        self.click(ncon.NUMBERINPUTBOXX, ncon.NUMBERINPUTBOXY)
        time.sleep(ncon.SHORT_SLEEP)

    def rebirth(self):
        """Click rebirth menu."""
        if Navigation.current_menu == "rebirth":
            return
        self.click(ncon.REBIRTHX, ncon.REBIRTHY)
        time.sleep(ncon.SHORT_SLEEP)
        Navigation.current_menu = "rebirth"

    def confirm(self):
        """Click yes in confirm window."""
        self.click(ncon.CONFIRMX, ncon.CONFIRMY)
        time.sleep(ncon.SHORT_SLEEP)

    def ngu_magic(self):
        """Navigate to NGU magic."""
        if Navigation.current_menu == "ngu_magic":
            return
        self.menu("ngu")
        self.click(ncon.NGUMAGICX, ncon.NGUMAGICY)
        time.sleep(ncon.SHORT_SLEEP)
        Navigation.current_menu = "ngu_magic"

    def exp(self):
        """Navigate to EXP Menu."""
        if Navigation.current_menu == "exp":
            return
        self.click(ncon.EXPX, ncon.EXPY)
        time.sleep(ncon.SHORT_SLEEP)
        Navigation.current_menu = "exp"

    def exp_magic(self):
        """Navigate to the magic menu within the EXP menu."""
        if Navigation.current_menu == "exp_magic":
            return
        self.exp()
        self.click(ncon.MMENUX, ncon.MMENUY)
        time.sleep(ncon.SHORT_SLEEP)
        Navigation.current_menu = "exp_magic"

    def info(self):
        """Click info 'n stuff."""
        if Navigation.current_menu == "info":
            return
        self.click(ncon.INFOX, ncon.INFOY)
        time.sleep(ncon.SHORT_SLEEP)
        Navigation.current_menu = "info"

    def misc(self):
        """Navigate to Misc stats."""
        if Navigation.current_menu == "misc":
            return
        self.info()
        self.click(ncon.MISCX, ncon.MISCY)
        time.sleep(ncon.SHORT_SLEEP)
        Navigation.current_menu = "misc"