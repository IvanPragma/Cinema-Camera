from __future__ import annotations

import bauiv1 as bui
import bascenev1 as bs

from typing import Union


class EditVector:

    def __init__(self,
                 value: bs.Vec3,
                 callback: Union[callable, None] = None,
                 fields_title: Union[list, None] = None) -> None:

        if not fields_title:
            fields_title = ["X position:", "Y position:", "Z position:"]
        if len(fields_title) < 3:
            fields_title += ["Unknown"] * (3 - len(fields_title))

        self.value: bs.Vec3 = value

        self.uiscale = bui.app.ui_v1.uiscale
        self.width: float = 400
        self.height: float = 400
        self.bg_color: tuple = (0.5, 0.5, 0.5)
        self.scale_origin = None
        self._transition_out: str = 'out_scale'
        self.callback: Union[callable, None] = callback

        self.root_widget = bui.containerwidget(
            size=(self.width, self.height),
            color=self.bg_color,
            toolbar_visibility='menu_minimal_no_back',
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self._cancel,
            scale=(2.1 if self.uiscale is bui.UIScale.SMALL else
                   1.5 if self.uiscale is bui.UIScale.MEDIUM else 1.0),
            scale_origin_stack_offset=self.scale_origin)

        self.x_text = bui.textwidget(
            parent=self.root_widget,
            position=(75, self.height - 115),
            size=(20, 20),
            h_align='center',
            v_align='center',
            text=fields_title[0],
            scale=0.7,
            color=(1, 1, 1))

        self.x_edit = bui.textwidget(
            parent=self.root_widget,
            editable=True,
            size=(120, 40),
            position=(135, self.height - 120),
            text=str(value.x),
            maxwidth=494,
            shadow=0.3,
            flatness=1.0,
            autoselect=True,
            v_align='center',
            corner_scale=0.7)

        self.y_text = bui.textwidget(
            parent=self.root_widget,
            position=(75, self.height - 165),
            size=(20, 20),
            h_align='center',
            v_align='center',
            text=fields_title[1],
            scale=0.7,
            color=(1, 1, 1))

        self.y_edit = bui.textwidget(
            parent=self.root_widget,
            editable=True,
            size=(120, 40),
            position=(135, self.height - 170),
            text=str(value.y),
            maxwidth=494,
            shadow=0.3,
            flatness=1.0,
            autoselect=True,
            v_align='center',
            corner_scale=0.7)

        self.z_text = bui.textwidget(
            parent=self.root_widget,
            position=(75, self.height - 215),
            size=(20, 20),
            h_align='center',
            v_align='center',
            text=fields_title[2],
            scale=0.7,
            color=(1, 1, 1))

        self.z_edit = bui.textwidget(
            parent=self.root_widget,
            editable=True,
            size=(120, 40),
            position=(135, self.height - 220),
            text=str(value.z),
            maxwidth=494,
            shadow=0.3,
            flatness=1.0,
            autoselect=True,
            v_align='center',
            corner_scale=0.7)

        self.save_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(self.width - 140, self.height - 350),
            size=(80, 30),
            label='Save',
            button_type='square',
            on_activate_call=self._save
        )

        btn = bui.buttonwidget(parent=self.root_widget,
                               autoselect=True,
                               position=(30, self.height - 60),
                               size=(30, 30),
                               label=bui.charstr(bui.SpecialChar.BACK),
                               button_type='backSmall',
                               on_activate_call=self._cancel)
        bui.containerwidget(edit=self.root_widget, cancel_button=btn)

    def _save(self) -> None:
        try:
            x = float(bui.textwidget(query=self.x_edit))
            y = float(bui.textwidget(query=self.y_edit))
            z = float(bui.textwidget(query=self.z_edit))
        except ValueError:
            bui.screenmessage("Неверно заполнены поля", color=(0.8, 0.1, 0.1))
            return
        self.value = bs.Vec3(x, y, z)
        if self.callback:
            self.callback(self.value)
        self._cancel()

    def _cancel(self) -> None:
        bui.containerwidget(
            edit=self.root_widget,
            transition=('out_right' if self._transition_out is None else
                        self._transition_out)
        )


class EditNum:

    def __init__(self,
                 value: Union[float, int],
                 callback: Union[callable, None] = None,
                 fields_title: Union[list, None] = None) -> None:

        if not fields_title:
            fields_title = ["Value"]
        if len(fields_title) < 1:
            fields_title += ["Unknown"] * (1 - len(fields_title))

        self.value: Union[float, int] = value

        self.uiscale = bui.app.ui_v1.uiscale
        self.width: float = 400
        self.height: float = 290
        self.bg_color: tuple = (0.5, 0.5, 0.5)
        self.scale_origin = None
        self._transition_out: str = 'out_scale'
        self.callback: Union[callable, None] = callback

        self.root_widget = bui.containerwidget(
            size=(self.width, self.height),
            color=self.bg_color,
            toolbar_visibility='menu_minimal_no_back',
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self._cancel,
            scale=(2.1 if self.uiscale is bui.UIScale.SMALL else
                   1.5 if self.uiscale is bui.UIScale.MEDIUM else 1.0),
            scale_origin_stack_offset=self.scale_origin)

        self.x_text = bui.textwidget(
            parent=self.root_widget,
            position=(75, self.height - 115),
            size=(20, 20),
            h_align='center',
            v_align='center',
            text=fields_title[0],
            scale=0.7,
            color=(1, 1, 1))

        self.x_edit = bui.textwidget(
            parent=self.root_widget,
            editable=True,
            size=(120, 40),
            position=(135, self.height - 120),
            text=str(self.value),
            maxwidth=494,
            shadow=0.3,
            flatness=1.0,
            autoselect=True,
            v_align='center',
            corner_scale=0.7)

        self.save_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(self.width - 140, self.height - 250),
            size=(80, 30),
            label='Save',
            button_type='square',
            on_activate_call=self._save)

        btn = bui.buttonwidget(parent=self.root_widget,
                               autoselect=True,
                               position=(30, self.height - 60),
                               size=(30, 30),
                               label=bui.charstr(bui.SpecialChar.BACK),
                               button_type='backSmall',
                               on_activate_call=self._cancel)
        bui.containerwidget(edit=self.root_widget, cancel_button=btn)

    def _save(self) -> None:
        try:
            x = float(bui.textwidget(query=self.x_edit))
        except ValueError:
            bui.screenmessage("Неверно заполнено поле", color=(0.8, 0.1, 0.1))
            return
        self.value = x
        if self.callback:
            self.callback(self.value)
        self._cancel()

    def _cancel(self) -> None:
        bui.containerwidget(
            edit=self.root_widget,
            transition=('out_right' if self._transition_out is None else
                        self._transition_out)
        )
