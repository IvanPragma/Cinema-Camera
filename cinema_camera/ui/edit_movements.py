from __future__ import annotations

import bauiv1 as bui
import bascenev1 as bs
from bascenev1 import app
from cinema_camera.ui.movement import MovementWidget

from typing import Optional

from cinema_camera.movement import Movement
from cinema_camera.ui.settings import SettingsWidget


class EditMovementsWindow:
    """Window for edit movements and their attributes."""

    def __init__(self, root) -> None:
        self.movement_widgets = []
        self._selected_movement = None
        self.root = root
        uiscale = bui.app.ui_v1.uiscale
        self.height = (420 if uiscale is bui.UIScale.SMALL else
                       470 if uiscale is bui.UIScale.MEDIUM else 520)
        self.width = (500 if uiscale is bui.UIScale.SMALL else
                      600 if uiscale is bui.UIScale.MEDIUM else 650)
        scroll_h = (250 if uiscale is bui.UIScale.SMALL else
                    300 if uiscale is bui.UIScale.MEDIUM else 320)
        scroll_w = (450 if uiscale is bui.UIScale.SMALL else
                    550 if uiscale is bui.UIScale.MEDIUM else 600)

        self._transition_out: Optional[str] = 'out_scale'
        scale_origin: Optional[tuple[float, float]] = 10

        transition: str = 'in_scale'
        scale_origin = None  # HM
        cancel_is_selected = False
        cfg = bui.app.config

        bg_color = cfg.get('PartyWindow Main Color', (0.5, 0.5, 0.5))

        self.root_widget = bui.containerwidget(  # Our widget (window)
            size=(self.width, self.height),
            color=bg_color,
            transition=transition,
            toolbar_visibility='menu_minimal_no_back',
            parent=bui.get_special_widget('overlay_stack'),  # HM
            on_outside_click_call=self._cancel,
            scale=(2.1 if uiscale is bui.UIScale.SMALL else
                   1.5 if uiscale is bui.UIScale.MEDIUM else 1.0),
            scale_origin_stack_offset=scale_origin)

        bui.textwidget(parent=self.root_widget,  # Window title
                       position=(self.width * 0.5, self.height - 45),
                       size=(20, 20),
                       h_align='center',
                       v_align='center',
                       text="Edit Movements",
                       scale=0.9,
                       color=(1, 1, 1))

        cbtn = btn = bui.buttonwidget(parent=self.root_widget,  # Back button
                                      autoselect=True,
                                      position=(30, self.height - 60),
                                      size=(30, 30),
                                      label=bui.charstr(bui.SpecialChar.BACK),
                                      button_type='backSmall',
                                      on_activate_call=self._cancel)

        add_new_movement_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(self.width - 170, self.height - 130),
            size=(125, 30),
            label='Add movement',
            button_type='square',
            color=bg_color,
            on_activate_call=self._on_add_movement_press
        )

        delete_movement_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(self.width - 170, self.height - 85),
            size=(125, 30),
            label='Delete movement',
            button_type='square',
            color=bg_color,
            on_activate_call=self._on_delete_movement_press
        )

        bui.buttonwidget(parent=self.root_widget,
                         position=(self.width - 210, self.height - 85),
                         size=(25, 25),
                         icon=bui.gettexture('settingsIcon'),
                         button_type='square',
                         color=bg_color,
                         on_activate_call=self._on_settings_press)

        bui.buttonwidget(parent=self.root_widget,
                         autoselect=True,
                         position=(50, self.height - 130),
                         size=(125, 30),
                         color=(0.1, 0.8, 0.1),
                         icon=bui.gettexture('startButton'),
                         label='Start',
                         on_activate_call=self._start)

        bui.buttonwidget(parent=self.root_widget,
                         autoselect=True,
                         position=(50, self.height - 85),
                         size=(125, 30),
                         color=(0.1, 0.8, 0.8),
                         icon=bui.gettexture('achievementCrossHair'),
                         label='Add current point',
                         on_activate_call=self._add_current_camera_point)

        scroll_position = (30 if uiscale is bui.UIScale.SMALL else
                           40 if uiscale is bui.UIScale.MEDIUM else 50)

        self._scrollwidget = bui.scrollwidget(parent=self.root_widget,
                                              position=(30, scroll_position),
                                              simple_culling_v=20.0,
                                              highlight=False,
                                              size=(scroll_w, scroll_h),
                                              selection_loops_to_parent=True)

        bui.widget(edit=self._scrollwidget, right_widget=self._scrollwidget)

        self._subcontainer = bui.columnwidget(parent=self._scrollwidget,
                                              border=15,
                                              selection_loops_to_parent=True)

        self._update_movements()

        bui.containerwidget(edit=self.root_widget, cancel_button=btn)
        bui.containerwidget(edit=self.root_widget,
                            selected_child=(cbtn if cbtn is not None
                                            and cancel_is_selected else None),
                            start_button=None)

    def _update_movements(self) -> None:

        for child in self._subcontainer.get_children():
            child.delete()

        cur_h = 0.0
        self.movement_widgets = []
        for i, mvm in enumerate(app.cinema_camera.camera.movements):
            self.movement_widgets.append(
                bui.buttonwidget(
                    parent=self._subcontainer,
                    position=(20, self.height - cur_h),
                    size=(300, 30),
                    label=f'Movement #{mvm.num}',
                    on_select_call=bui.Call(self._on_movement_select, mvm.num),
                    color=(.75, .75, .75),
                    on_activate_call=bui.Call(self._on_edit_movement_press, mvm)
                )
            )
            cur_h += 75.0

    def _get_new_movement_num(self) -> int:
        new_num = 1
        if len(app.cinema_camera.camera.movements) > 0:
            new_num = app.cinema_camera.camera.movements[-1].num + 1
        return new_num

    def _on_add_movement_press(self) -> None:
        new_num = self._get_new_movement_num()
        MovementWidget(self, new_num)

    def _on_movement_select(self, num) -> None:
        self._selected_movement = num

    def _on_settings_press(self) -> None:
        settings_widget = SettingsWidget(self,
                                         app.cinema_camera.camera.settings)

    def _on_edit_movement_press(self, mvm: Movement) -> None:
        if mvm not in app.cinema_camera.camera.movements:
            raise RuntimeError('Movement are not found')

        num = app.cinema_camera.camera.movements.index(mvm) + 1
        mvm_widget = MovementWidget(self, num, mvm=mvm)
        mvm_widget.position = mvm.position
        mvm_widget.target = mvm.target
        mvm_widget.during_time = mvm.during_time
        mvm_widget.speed_graph_cf = mvm.speed_graph_cf
        mvm_widget.smooth_move_graph_cf = mvm.speed_move_cf

    def _on_delete_movement_press(self) -> None:
        if not self._selected_movement:
            bui.screenmessage("Movement are not selected",
                              color=(0.8, 0.1, 0.1))
            return
        for mvm in app.cinema_camera.camera.movements:
            if mvm.num == self._selected_movement:
                app.cinema_camera.camera.movements.remove(mvm)
                break
        self._update_movements()

    def _add_current_camera_point(self) -> None:

        new_num = self._get_new_movement_num()

        app.cinema_camera.camera.movements.append(
            Movement(
                new_num,
                app.cinema_camera.camera.position,
                app.cinema_camera.camera.target,
                1.0, 1.0, bs.Vec3(1.0, 1.0, 1.0),
                apply_previous_velocity=True))
        self._update_movements()

        bui.screenmessage(f"Successfully add movement #{new_num}",
                          color=(0.4, 0.3, 0.9))

    def _start(self) -> None:
        self.root_widget.delete()
        self.root.get_root_widget().delete()
        app.cinema_camera.camera.start_move()

    def _cancel(self) -> None:
        bui.containerwidget(
            edit=self.root_widget,
            transition=('out_right' if self._transition_out is None else
                        self._transition_out)
        )
