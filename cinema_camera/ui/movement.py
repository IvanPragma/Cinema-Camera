from __future__ import annotations

import ba
import _ba

from ba import app

from typing import Tuple, Optional, Union, Dict

from cinema_camera.movement import Movement
from cinema_camera.ui.edit import EditVector, EditNum


class MovementWidget:
    """Widget for edit movement."""

    def __init__(self, parent, num: int, mvm: Union[Movement, None] = None) -> None:
        self.parent = parent

        self.num: int = num

        if not mvm:
            self.movement: Movement = Movement(num=num,
                                               position=ba.Vec3(0, 0, 0),
                                               target=ba.Vec3(0, 0, 0),
                                               during_time=1.0,
                                               speed_graph_cf=1.0,
                                               speed_move_cf=ba.Vec3(1.0, 1.0, 1.0),
                                               apply_previous_velocity=True)
        else:
            self.movement: Movement = mvm

        uiscale = ba.app.ui.uiscale
        self.height = (520 if uiscale is ba.UIScale.SMALL else
                       570 if uiscale is ba.UIScale.MEDIUM else 620)
        self.width = (500 if uiscale is ba.UIScale.SMALL else
                      600 if uiscale is ba.UIScale.MEDIUM else 650)

        self._transition_out: Optional[str] = 'out_scale'
        scale_origin: Optional[Tuple[float, float]] = 10

        transition: str = 'in_scale'
        scale_origin = None  # HM
        self.cancel_is_selected = False
        cfg = ba.app.config

        self.bg_color = cfg.get('PartyWindow Main Color', (0.5, 0.5, 0.5))

        self.root_widget = ba.containerwidget(  # Our widget (window)
            size=(self.width, self.height),
            color=self.bg_color,
            transition=transition,
            toolbar_visibility='menu_minimal_no_back',
            parent=_ba.get_special_widget('overlay_stack'),  # HM
            on_outside_click_call=self._cancel,
            scale=(2.1 if uiscale is ba.UIScale.SMALL else
                   1.5 if uiscale is ba.UIScale.MEDIUM else 1.0),
            scale_origin_stack_offset=scale_origin)

        self._update()

    def _update(self):

        for child in self.root_widget.get_children():
            child.delete()

        ba.textwidget(parent=self.root_widget,  # Window title
                      position=(self.width * 0.5, self.height - 45),
                      size=(20, 20),
                      h_align='center',
                      v_align='center',
                      text=f"Movement #{self.num}",
                      scale=0.7,
                      color=(1, 1, 1))

        cbtn = btn = ba.buttonwidget(parent=self.root_widget,  # Back button
                                     autoselect=True,
                                     position=(30, self.height - 60),
                                     size=(30, 30),
                                     label=ba.charstr(ba.SpecialChar.BACK),
                                     button_type='backSmall',
                                     on_activate_call=self._cancel)

        self.position_text = ba.textwidget(
            parent=self.root_widget,
            position=(60, self.height - 103),
            size=(20, 20),
            h_align='center',
            v_align='center',
            text='Position:',
            scale=0.7,
            color=(1, 1, 1))

        pos = self.movement.position
        pos_txt = f'{(round(pos.x, 2), round(pos.y, 2), round(pos.z, 2))}'
        self.change_position_button = ba.buttonwidget(parent=self.root_widget,
                                                      position=(120, self.height - 110),
                                                      size=(125, 30),
                                                      label=pos_txt,
                                                      button_type='square',
                                                      color=self.bg_color,
                                                      on_activate_call=self._on_change_position_press)

        pos_graph = self.movement.speed_move_cf
        pos_graph_txt = f'{(round(pos_graph.x, 2), round(pos_graph.y, 2), round(pos_graph.z, 2))}'
        self.change_position_graph_button = ba.buttonwidget(parent=self.root_widget,
                                                            position=(250, self.height - 110),
                                                            size=(125, 30),
                                                            label=f'Graph: {pos_graph_txt}',
                                                            button_type='square',
                                                            color=self.bg_color,
                                                            on_activate_call=self._on_change_move_graph)  # FIXME

        self.target_text = ba.textwidget(
            parent=self.root_widget,
            position=(60, self.height - 147),
            size=(20, 20),
            h_align='center',
            v_align='center',
            text='Target:',
            scale=0.7,
            color=(1, 1, 1))

        trg = self.movement.target
        trg_txt = f'{(round(trg.x, 2), round(trg.y, 2), round(trg.z, 2))}'
        self.change_target_button = ba.buttonwidget(parent=self.root_widget,
                                                    position=(120, self.height - 155),
                                                    size=(125, 30),
                                                    label=trg_txt,
                                                    button_type='square',
                                                    color=self.bg_color,
                                                    on_activate_call=self._on_change_target_press)

        trg_graph = self.movement.speed_move_cf
        trg_graph_txt = f'{(round(trg_graph.x, 2), round(trg_graph.y, 2), round(trg_graph.z, 2))}'
        self.change_target_graph_button = ba.buttonwidget(parent=self.root_widget,
                                                          position=(250, self.height - 155),
                                                          size=(125, 30),
                                                          label=f'Graph: {trg_graph_txt}',
                                                          button_type='square',
                                                          color=self.bg_color,
                                                          on_activate_call=self._on_change_move_graph)

        self.time_text = ba.textwidget(
            parent=self.root_widget,
            position=(60, self.height - 192),
            size=(20, 20),
            h_align='center',
            v_align='center',
            text='Time:',
            scale=0.7,
            color=(1, 1, 1))

        self.change_time_button = ba.buttonwidget(parent=self.root_widget,
                                                  position=(120, self.height - 200),
                                                  size=(125, 30),
                                                  label=f'During time: {self.movement.during_time}',
                                                  button_type='square',
                                                  color=self.bg_color,
                                                  on_activate_call=self._on_change_time_press)

        self.change_time_graph_button = ba.buttonwidget(parent=self.root_widget,
                                                        position=(250, self.height - 200),
                                                        size=(125, 30),
                                                        label=f'Graph: ({self.movement.speed_graph_cf})',
                                                        button_type='square',
                                                        color=self.bg_color,
                                                        on_activate_call=self._on_change_speed_graph)

        self.settings_button = ba.buttonwidget(parent=self.root_widget,
                                               position=(self.width - 140, self.height - 60),
                                               size=(25, 25),
                                               icon=ba.gettexture('settingsIcon'),
                                               button_type='square',
                                               color=self.bg_color,
                                               on_activate_call=self._on_settings_press)

        self.save_button = ba.buttonwidget(parent=self.root_widget,
                                           position=(self.width - 140, self.height - 300),
                                           size=(125, 30),
                                           label='Save',
                                           button_type='square',
                                           on_activate_call=self._save)

        self.cancel_button = ba.buttonwidget(parent=self.root_widget,
                                             position=(30, self.height - 300),
                                             size=(125, 30),
                                             label='Cancel',
                                             button_type='square',
                                             color=(0.8, 0.3, 0.3),
                                             on_activate_call=self._cancel)

        ba.containerwidget(edit=self.root_widget, cancel_button=btn)  # setup cancel button
        ba.containerwidget(edit=self.root_widget,
                           selected_child=(cbtn if cbtn is not None
                                                   and self.cancel_is_selected else None),
                           start_button=None)  # select cancel button, if it need

    def _on_change_position_press(self):
        def set_value(value: ba.Vec3) -> None:
            self.movement.position = value
            self._update()

        EditVector(self.movement.position, set_value)

    def _on_change_target_press(self):
        def set_value(value: ba.Vec3) -> None:
            self.movement.target = value
            self._update()

        EditVector(self.movement.target, set_value)

    def _on_change_time_press(self):
        def set_value(value: float) -> None:
            self.movement.during_time = value
            self._update()

        EditNum(self.movement.during_time, set_value)

    def _on_change_speed_graph(self):
        def set_value(value: float) -> None:
            self.movement.speed_graph_cf = value
            self._update()

        EditNum(self.movement.speed_graph_cf, set_value, fields_title=['degree'])

    def _on_change_move_graph(self):
        def set_value(value: ba.Vec3) -> None:
            self.movement.speed_move_cf = value
            self._update()

        EditVector(self.movement.speed_move_cf, set_value, fields_title=['X degree', 'Y degree', 'Z degree'])

    def _on_settings_press(self):
        ba.screenmessage("Настройки", color=(0.1, 0.8, 0.5))

    def _save(self) -> None:
        ba.screenmessage(f"Successfully add movement #{self.num}", color=(0.4, 0.3, 0.9))

        # self.movement.during_time

        if self.movement not in app.cinema_camera.camera.movements:
            idx = len(app.cinema_camera.camera.movements)
            app.cinema_camera.camera.movements.append(None)
        else:
            idx = app.cinema_camera.camera.movements.index(self.movement)

        app.cinema_camera.camera.movements[idx] = self.movement
        self.parent._update_movements()
        self._cancel()

    def _cancel(self) -> None:
        ba.containerwidget(
            edit=self.root_widget,
            transition=('out_right' if self._transition_out is None else
                        self._transition_out))
