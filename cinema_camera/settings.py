from __future__ import annotations

import ba


def get_default_settings() -> dict:
    return {
        'newton_polynomial': ba.BoolSetting('Сглаживание (полином Ньютона)', True),
    }


def load_settings() -> dict:
    if 'cc' not in ba.app.config:
        ba.app.config['cc'] = dict([(key, setting.default) for key, setting in get_default_settings().items()])
        ba.app.config.apply_and_commit()

    my_settings = ba.app.config['cc']
    settings = get_default_settings()
    for key, setting in settings.items():
        if key in my_settings:
            settings[key].default = my_settings[key]

    return settings


def save_settings(settings: dict) -> None:
    assert isinstance(settings, dict)
    ba.app.config['cc'] = settings
    ba.app.config.apply_and_commit()
    ba.app.cinema_camera.camera.settings = load_settings()
