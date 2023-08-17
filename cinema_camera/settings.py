from __future__ import annotations

import bascenev1 as bs


def get_default_settings() -> dict:
    return {'newton_polynomial': bs.BoolSetting('Сглаживание (полином Ньютона)',
                                                True)}


def load_settings() -> dict:
    if 'cc' not in bs.app.config:
        bs.app.config['cc'] = dict([(key, setting.default) for key, setting
                                    in get_default_settings().items()])
        bs.app.config.apply_and_commit()

    my_settings = bs.app.config['cc']
    settings = get_default_settings()
    for key, setting in settings.items():
        if key in my_settings:
            settings[key].default = my_settings[key]

    return settings


def save_settings(settings: dict) -> None:
    assert isinstance(settings, dict)
    bs.app.config['cc'] = settings
    bs.app.config.apply_and_commit()
    bs.app.cinema_camera.camera.settings = load_settings()
