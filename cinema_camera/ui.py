from __future__ import annotations

import ba
import _ba
#from bastd.ui.popup import PopupMenuWindow, PopupWindow
#from bastd.ui.confirm import ConfirmWindow
#from bastd.ui.colorpicker import ColorPickerExact
#from bastd.ui.mainmenu import MainMenuWindow
#from typing import List, Tuple, Sequence, Optional, Dict, Any, Union, TYPE_CHECKING, cast
#from bastd.ui.playlist.editcontroller import PlaylistEditController
#import bastd.ui.party


class SettingsWindow:
    """Window for answering simple yes/no questions."""

    def __init__(self):
        uiscale = ba.app.ui.uiscale
        height = (300 if uiscale is ba.UIScale.SMALL else
                   350 if uiscale is ba.UIScale.MEDIUM else 400)
        width = (500 if uiscale is ba.UIScale.SMALL else
                   600 if uiscale is ba.UIScale.MEDIUM else 650)
        scroll_h = (200 if uiscale is ba.UIScale.SMALL else
                   250 if uiscale is ba.UIScale.MEDIUM else 270)
        scroll_w = (450 if uiscale is ba.UIScale.SMALL else
                   550 if uiscale is ba.UIScale.MEDIUM else 600)
        self._transition_out: Optional[str]
        scale_origin: Optional[Tuple[float, float]]
        self._transition_out = 'out_scale'
        scale_origin = 10
        transition = 'in_scale'
        scale_origin = None
        cancel_is_selected = False
        cfg = ba.app.config
        bg_color = cfg.get('PartyWindow Main Color', (0.5,0.5,0.5))

        self.root_widget = ba.containerwidget(
            size=(width, height),
            color = bg_color,
            transition=transition,
            toolbar_visibility='menu_minimal_no_back',
            parent=_ba.get_special_widget('overlay_stack'),
            on_outside_click_call=self._cancel,
            scale=(2.1 if uiscale is ba.UIScale.SMALL else
                   1.5 if uiscale is ba.UIScale.MEDIUM else 1.0),
            scale_origin_stack_offset=scale_origin)
        ba.textwidget(parent=self.root_widget,
                      position=(width * 0.5, height - 45),
                      size=(20, 20),
                      h_align='center',
                      v_align='center',
                      text="Custom Settings",
                      scale=0.9,
                      color=(5,5,5))
        cbtn = btn = ba.buttonwidget(parent=self.root_widget,
                                     autoselect=True,
                                     position=(30, height - 60),
                                     size=(30, 30),
                                     label=ba.charstr(ba.SpecialChar.BACK),
                                     button_type='backSmall',
                                     on_activate_call=self._cancel)
        scroll_position = (30 if uiscale is ba.UIScale.SMALL else
                           40 if uiscale is ba.UIScale.MEDIUM else 50)
        self._scrollwidget = ba.scrollwidget(parent=self.root_widget,
                                             position=(30, scroll_position),
                                             simple_culling_v=20.0,
                                             highlight=False,
                                             size=(scroll_w, scroll_h),
                                             selection_loops_to_parent=True)
        ba.widget(edit=self._scrollwidget, right_widget=self._scrollwidget)
        self._subcontainer = ba.columnwidget(parent=self._scrollwidget,
                                             selection_loops_to_parent=True)
        ip_button = ba.checkboxwidget(
                    parent=self._subcontainer,
                    position=(20, height - 100),
                    size=(300, 30),
                    maxwidth=300,
                    textcolor = ((0,1,0) if cfg['IP button'] else (0.95,0.65,0)),
                    scale=1,
                    value=cfg['IP button'],
                    autoselect=True,
                    text="IP Button",
                    on_value_change_call=self.ip_button)
        ping_button = ba.checkboxwidget(
                    parent=self._subcontainer,
                    position=(20, height - 150),
                    size=(300, 30),
                    maxwidth=300,
                    textcolor = ((0,1,0) if cfg['ping button'] else (0.95,0.65,0)),
                    scale=1,
                    value=cfg['ping button'],
                    autoselect=True,
                    text="Ping Button",
                    on_value_change_call=self.ping_button)
        copy_button = ba.checkboxwidget(
                    parent=self._subcontainer,
                    position=(20, height - 200),
                    size=(300, 30),
                    maxwidth=300,
                    textcolor = ((0,1,0) if cfg['copy button'] else (0.95,0.65,0)),
                    scale=1,
                    value=cfg['copy button'],
                    autoselect=True,
                    text="Copy Text Button",
                    on_value_change_call=self.copy_button)
        direct_send = ba.checkboxwidget(
                    parent=self._subcontainer,
                    position=(20, height - 250),
                    size=(300, 30),
                    maxwidth=300,
                    textcolor = ((0,1,0) if cfg['Direct Send'] else (0.95,0.65,0)),
                    scale=1,
                    value=cfg['Direct Send'],
                    autoselect=True,
                    text="Directly Send Custom Commands",
                    on_value_change_call=self.direct_send)
        custom_cmd = ba.checkboxwidget(
                    parent=self._subcontainer,
                    position=(20, height - 250),
                    size=(300, 30),
                    maxwidth=300,
                    textcolor = ((0,1,0) if cfg['my cmd'] else (0.95,0.65,0)),
                    scale=1,
                    value=cfg['my cmd'],
                    autoselect=True,
                    text="Custom Command Choice",
                    on_value_change_call=self.my_cmd)            
        ba.containerwidget(edit=self.root_widget, cancel_button=btn)
        ba.containerwidget(edit=self.root_widget,
                           selected_child=(cbtn if cbtn is not None
                                           and cancel_is_selected else None),
                           start_button=None)

    def ip_button(self, value: bool):
        cfg = ba.app.config
        cfg['IP button'] = value
        cfg.apply_and_commit()
        if cfg['IP button']:
            ba.screenmessage("IP Button is now enabled", color = (0,1,0))
        else:
            ba.screenmessage("IP Button is now disabled", color = (1,0.7,0))
    def ping_button(self, value: bool):
        cfg = ba.app.config
        cfg['ping button'] = value
        cfg.apply_and_commit()
        if cfg['ping button']:
            ba.screenmessage("Ping Button is now enabled", color = (0,1,0))
        else:
            ba.screenmessage("Ping Button is now disabled", color = (1,0.7,0)) 
    def copy_button(self, value: bool):
        cfg = ba.app.config
        cfg['copy button'] = value
        cfg.apply_and_commit()
        if cfg['copy button']:
            ba.screenmessage("Copy Text Button is now enabled", color = (0,1,0))
        else:
            ba.screenmessage("Copy Text Button is now disabled", color = (1,0.7,0))
    def direct_send(self, value: bool):
        cfg = ba.app.config
        cfg['Direct Send'] = value
        cfg.apply_and_commit()
        if cfg['copy button']:
            ba.screenmessage("Custom Commands will be send directly.", color = (0,1,0))
        else:
            ba.screenmessage("Text Box will be replaced by Custom Command.", color = (1,0.7,0))
    def my_cmd(self, value: bool):
        cfg = ba.app.config
        cfg['my cmd'] = value
        cfg.apply_and_commit() 
        if cfg['my cmd']:
            ba.screenmessage("Custom Command Choice will now appear.", color = (0,1,0))
        else:
            ba.screenmessage("Custom Command Choice will not appear", color = (1,0.7,0))  
    def _cancel(self) -> None:
        ba.containerwidget(
            edit=self.root_widget,
            transition=('out_right' if self._transition_out is None else
                        self._transition_out))
