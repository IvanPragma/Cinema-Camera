from __future__ import annotations

from typing import Union, cast

import ba
import _ba

from cinema_camera.settings import save_settings


class SettingsWidget:

    def __init__(self, root, settings: dict) -> None:

        self.root = root
        self.settings: dict = settings
        self.raw_settings: dict = dict([(key, setting.default) for key, setting in settings.items()])
        self._choice_selections: dict = {}

        uiscale = ba.app.ui.uiscale
        self.height = (420 if uiscale is ba.UIScale.SMALL else
                       470 if uiscale is ba.UIScale.MEDIUM else 520)
        self.width = (500 if uiscale is ba.UIScale.SMALL else
                      600 if uiscale is ba.UIScale.MEDIUM else 650)

        cfg = ba.app.config
        bg_color = cfg.get('PartyWindow Main Color', (0.5, 0.5, 0.5))

        self.root_widget = ba.containerwidget(  # Our widget (window)
            size=(self.width, self.height),
            color=bg_color,
            transition='in_scale',
            toolbar_visibility='menu_minimal_no_back',
            parent=_ba.get_special_widget('overlay_stack'),  # HM
            on_outside_click_call=self._cancel,
            scale=(2.1 if uiscale is ba.UIScale.SMALL else
                   1.5 if uiscale is ba.UIScale.MEDIUM else 1.0),
            scale_origin_stack_offset=None)

        ba.textwidget(parent=self.root_widget,  # Window title
                      position=(self.width * 0.5, self.height - 45),
                      size=(20, 20),
                      h_align='center',
                      v_align='center',
                      text="Settings",
                      scale=0.9,
                      color=(1, 1, 1))

        cbtn = ba.buttonwidget(parent=self.root_widget,  # Back button
                               autoselect=True,
                               position=(30, self.height - 60),
                               size=(30, 30),
                               label=ba.charstr(ba.SpecialChar.BACK),
                               button_type='backSmall',
                               on_activate_call=self._cancel)

        add_button = ba.buttonwidget(
            parent=self.root_widget,
            position=(self.width - 170, self.height - 60),
            size=(200, 65),
            scale=0.75,
            text_scale=1.3,
            label='Сохранить',
            on_activate_call=self._save)

        self.update_settings()

    def update_settings(self) -> None:
        uiscale = ba.app.ui.uiscale
        x_inset = 50 if uiscale is ba.UIScale.SMALL else 0
        spacing = 52
        y_extra = 15
        scroll_height = 350 + 10
        scroll_width = self.width - (86 + 2 * x_inset)

        # Calc our total height we'll need
        scroll_height += spacing * len(self.settings)

        v = scroll_height - 5
        h = -40
        widget_column = []

        self._scrollwidget = ba.scrollwidget(parent=self.root_widget,
                                             position=(44 + x_inset,
                                                       35 + y_extra),
                                             size=(scroll_width, self.height - 116),
                                             highlight=False,
                                             claims_left_right=True,
                                             claims_tab=True,
                                             selection_loops_to_parent=True)

        self._subcontainer = ba.containerwidget(parent=self._scrollwidget,
                                                size=(scroll_width,
                                                      scroll_height),
                                                background=False,
                                                claims_left_right=True,
                                                claims_tab=True,
                                                selection_loops_to_parent=True)

        for key, setting in self.settings.items():
            value = setting.default
            value_type = type(value)

            # Shove the starting value in there to start.
            # self._settings[setting.name] = value

            name_translated = setting.name

            mw1 = 280
            mw2 = 70

            # Handle types with choices specially:
            if isinstance(setting, ba.ChoiceSetting):
                for choice in setting.choices:
                    if len(choice) != 2:
                        raise ValueError(
                            "Expected 2-member tuples for 'choices'; got: " +
                            repr(choice))
                    if not isinstance(choice[0], str):
                        raise TypeError(
                            'First value for choice tuple must be a str; got: '
                            + repr(choice))
                    if not isinstance(choice[1], value_type):
                        raise TypeError(
                            'Choice type does not match default value; choice:'
                            + repr(choice) + '; setting:' + repr(setting))
                if value_type not in (int, float):
                    raise TypeError(
                        'Choice type setting must have int or float default; '
                        'got: ' + repr(setting))

                # Start at the choice corresponding to the default if possible.
                self._choice_selections[setting.name] = 0
                for index, choice in enumerate(setting.choices):
                    if choice[1] == value:
                        self._choice_selections[setting.name] = index
                        break

                v -= spacing
                ba.textwidget(parent=self._subcontainer,
                              position=(h + 50, v),
                              size=(100, 30),
                              maxwidth=mw1,
                              text=name_translated,
                              h_align='left',
                              color=(0.8, 0.8, 0.8, 1.0),
                              v_align='center')
                txt = ba.textwidget(
                    parent=self._subcontainer,
                    position=(h + 509 - 95, v),
                    size=(0, 28),
                    text=setting.choices[self._choice_selections[setting.name]][0],
                    editable=False,
                    color=(0.6, 1.0, 0.6, 1.0),
                    maxwidth=mw2,
                    h_align='right',
                    v_align='center',
                    padding=2)
                btn1 = ba.buttonwidget(parent=self._subcontainer,
                                       position=(h + 509 - 50 - 1, v),
                                       size=(28, 28),
                                       label='<',
                                       autoselect=True,
                                       on_activate_call=ba.Call(
                                           self._choice_inc, key, txt,
                                           setting, -1),
                                       repeat=True)
                btn2 = ba.buttonwidget(parent=self._subcontainer,
                                       position=(h + 509 + 5, v),
                                       size=(28, 28),
                                       label='>',
                                       autoselect=True,
                                       on_activate_call=ba.Call(
                                           self._choice_inc, key, txt,
                                           setting, 1),
                                       repeat=True)
                widget_column.append([btn1, btn2])

            elif isinstance(setting, (ba.IntSetting, ba.FloatSetting)):
                v -= spacing
                min_value = setting.min_value
                max_value = setting.max_value
                increment = setting.increment
                ba.textwidget(parent=self._subcontainer,
                              position=(h + 50, v),
                              size=(100, 30),
                              text=name_translated,
                              h_align='left',
                              color=(0.8, 0.8, 0.8, 1.0),
                              v_align='center',
                              maxwidth=mw1)
                txt = ba.textwidget(parent=self._subcontainer,
                                    position=(h + 509 - 95, v),
                                    size=(0, 28),
                                    text=str(value),
                                    editable=False,
                                    color=(0.6, 1.0, 0.6, 1.0),
                                    maxwidth=mw2,
                                    h_align='right',
                                    v_align='center',
                                    padding=2)
                btn1 = ba.buttonwidget(parent=self._subcontainer,
                                       position=(h + 509 - 50 - 1, v),
                                       size=(28, 28),
                                       label='-',
                                       autoselect=True,
                                       on_activate_call=ba.Call(
                                           self._inc, txt, min_value,
                                           max_value, -increment, value_type,
                                           key),
                                       repeat=True)
                btn2 = ba.buttonwidget(parent=self._subcontainer,
                                       position=(h + 509 + 5, v),
                                       size=(28, 28),
                                       label='+',
                                       autoselect=True,
                                       on_activate_call=ba.Call(
                                           self._inc, txt, min_value,
                                           max_value, increment, value_type,
                                           key),
                                       repeat=True)
                widget_column.append([btn1, btn2])

            elif value_type == bool:
                v -= spacing
                ba.textwidget(parent=self._subcontainer,
                              position=(h + 50, v),
                              size=(100, 30),
                              text=name_translated,
                              h_align='left',
                              color=(0.8, 0.8, 0.8, 1.0),
                              v_align='center',
                              maxwidth=mw1)
                txt = ba.textwidget(
                    parent=self._subcontainer,
                    position=(h + 509 - 95, v),
                    size=(0, 28),
                    text=ba.Lstr(resource='onText') if value else ba.Lstr(
                        resource='offText'),
                    editable=False,
                    color=(0.6, 1.0, 0.6, 1.0),
                    maxwidth=mw2,
                    h_align='right',
                    v_align='center',
                    padding=2)
                cbw = ba.checkboxwidget(parent=self._subcontainer,
                                        text='',
                                        position=(h + 505 - 50 - 5, v - 2),
                                        size=(200, 30),
                                        autoselect=True,
                                        textcolor=(0.8, 0.8, 0.8),
                                        value=value,
                                        on_value_change_call=ba.Call(
                                            self._check_value_change,
                                            key, txt))
                widget_column.append([cbw])

            else:
                raise Exception()

    def _choice_inc(self, setting_name: str, widget: ba.Widget,
                    setting: ba.ChoiceSetting, increment: int) -> None:
        choices = setting.choices
        if increment > 0:
            self._choice_selections[setting_name] = min(
                len(choices) - 1, self._choice_selections[setting_name] + 1)
        else:
            self._choice_selections[setting_name] = max(
                0, self._choice_selections[setting_name] - 1)
        ba.textwidget(edit=widget,
                      text=choices[self._choice_selections[setting_name]][0])
        self.raw_settings[setting_name] = choices[
            self._choice_selections[setting_name]][1]

    def _check_value_change(self, setting_name: str, widget: ba.Widget,
                            value: int) -> None:
        ba.textwidget(edit=widget,
                      text=ba.Lstr(resource='onText') if value else ba.Lstr(
                          resource='offText'))
        self.raw_settings[setting_name] = value

    def _inc(self, ctrl: ba.Widget, min_val: Union[int, float],
             max_val: Union[int, float], increment: Union[int, float],
             setting_type: type, setting_name: str) -> None:
        if setting_type == float:
            val = float(cast(str, ba.textwidget(query=ctrl)))
        else:
            val = int(cast(str, ba.textwidget(query=ctrl)))
        val += increment
        val = max(min_val, min(val, max_val))
        if setting_type == float:
            ba.textwidget(edit=ctrl, text=str(round(val, 2)))
        elif setting_type == int:
            ba.textwidget(edit=ctrl, text=str(int(val)))
        else:
            raise TypeError('invalid vartype: ' + str(setting_type))
        self.raw_settings[setting_name] = val

    def _cancel(self) -> None:
        ba.containerwidget(
            edit=self.root_widget,
            transition='out_right')

    def _save(self) -> None:
        save_settings(self.raw_settings)
        print(self.raw_settings)
        self._cancel()
