from __future__ import annotations

import bauiv1 as bui
from bascenev1 import app, Plugin

from bauiv1lib.mainmenu import MainMenuWindow
from bauiv1lib.party import PartyWindow as OriginalPartyWindow

from cinema_camera.settings import load_settings
from cinema_camera.tools.redefine import redefine, redefine_class

from cinema_camera.camera import Camera
from cinema_camera.ui.party_window import PartyWindow


def _get_store_char_tex(self) -> str:
    bui.set_party_icon_always_visible(True)
    return self.cinema_camera_old()


def main(plugin: Plugin) -> None:
    print(f'CinemaCamera v{plugin.__version__}')
    app.cinema_camera = plugin
    redefine(MainMenuWindow, '_get_store_char_tex', _get_store_char_tex,
             'cinema_camera_old')
    redefine_class(OriginalPartyWindow, PartyWindow)


# ba_meta require api 8
# ba_meta export plugin
class CinemaCamera(Plugin):
    """Shoot beautiful videos together with cinema camera

    Author: Ivan Ms
    Owner: Ms Company - BombSquad
    Upgrade to api8: Era0S
    """

    __version__ = '1.3.api8'

    camera: Camera = None

    def on_app_running(self) -> None:
        """Plugin start point."""

        self.camera = Camera(load_settings())

        return main(self)
