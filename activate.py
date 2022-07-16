from __future__ import annotations

import ba
import _ba

from ba import app, Plugin

from bastd.ui.mainmenu import MainMenuWindow
from bastd.ui.party import PartyWindow as OriginalPartyWindow

from cinema_camera.settings import load_settings
from cinema_camera.tools.redefine import redefine, redefine_class

from cinema_camera.camera import Camera
from cinema_camera.ui.party_window import PartyWindow


def _get_store_char_tex(self) -> str:
    _ba.set_party_icon_always_visible(True)
    return self.cinema_camera_old()


def main(plugin: Plugin) -> None:
    print(f'CinemaCamera v{plugin.__version__}')
    app.cinema_camera = plugin
    redefine(MainMenuWindow, '_get_store_char_tex', _get_store_char_tex, 'cinema_camera_old')
    redefine_class(OriginalPartyWindow, PartyWindow)


# ba_meta require api 7
# ba_meta export plugin
class CinemaCamera(Plugin):
    """Shoot beautiful videos together with cinema camera

    Author: Ivan Ms
    Owner: Ms Company - BombSquad
    """

    __version__ = '1.2'

    camera: Camera = None

    def on_app_running(self) -> None:
        """Plugin start point."""

        if app.build_number < 20427:
            ba.screenmessage('Cinema Camera не может работать на версии ниже 1.6.7.\nПожалуйста, обновите игру.',
                             color=(.8, .1, .1))
            raise RuntimeError('Cinema Camera can\'t work on a BombSquad whose version is lower than 1.6.7')

        self.camera = Camera(load_settings())

        return main(self)
