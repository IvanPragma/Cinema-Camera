import ba

from cinema_camera.ui.edit_movements import EditMovementsWindow


class PartyWindow(ba.Window):
    _redefine_methods = ['__init__', '_on_edit_movements_button_press']

    def __init__(self, *args, **kwargs):

        getattr(self, '__init___old')(*args, **kwargs)

        self.bg_color = (.5, .5, .5)

        self._edit_movements_button = ba.buttonwidget(
            parent=self._root_widget,
            scale=0.7,
            position=(80, self._height - 47),  # (self._width - 80, self._height - 47)
            size=(50, 50),
            label='CC',
            autoselect=True,
            button_type='square',
            on_activate_call=ba.WeakCall(self._on_edit_movements_button_press),
            color=self.bg_color,
            iconscale=1.2)

    def _on_edit_movements_button_press(self):
        EditMovementsWindow(self)
