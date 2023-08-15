from __future__ import annotations

from typing import Optional, Union

import _babase
import _bascenev1
import bauiv1 as bui
import bascenev1 as bs

from cinema_camera.movement import Movement
from cinema_camera.tools.calculate import newton_polynomial


class Camera:
    """Camera class.

    Main class of CC

    Automatically receives/changes the attributes of the game camera,
    when receiving/changing the relevant attributes of this class.
    """

    @property
    def position(self) -> bs.Vec3:
        return bs.Vec3(_babase.get_camera_position())

    @position.setter
    def position(self, value: Optional[bs.Vec3]) -> bs.Vec3:
        assert isinstance(value, bs.Vec3)
        _babase.set_camera_position(value.x, value.y, value.z)

    @property
    def target(self) -> bs.Vec3:
        return bs.Vec3(_babase.get_camera_target())

    @target.setter
    def target(self, value: Optional[bs.Vec3]) -> bs.Vec3:
        assert isinstance(value, bs.Vec3)
        _babase.set_camera_target(value.x, value.y, value.z)

    def __init__(self, settings: dict):
        self.settings: dict = settings
        self.movements: list[Movement] = []
        self.position_at_time: callable = lambda x: x
        self.target_at_time: callable = lambda x: x

        self.current_time: float = -9999
        self.end_time: float = -9999
        self.active: bool = False

    def add_movement(self, movement: Movement) -> None:
        self.movements.append(movement)

    def start_move(self) -> None:
        """Starts moving.

        Preparing a data for moving.

        Forms a lists of movement's data and times list,
        then uses it for calculating moving functions.

        And if all right calling self._move() or just ba.animate_array().
        """

        assert not self.active, RuntimeError('Camera already moving, wait')
        self.active = True

        self.current_time = 0
        self.end_time = 0

        # form times list
        times = []
        for mv in self.movements:
            times.append(mv.during_time + self.end_time)
            self.end_time = times[-1]

        # form moving functions
        if self.settings['newton_polynomial'].default:
            self.position_at_time = newton_polynomial(
                times,
                [mv.position[0] for mv in self.movements],
                [mv.position[1] for mv in self.movements],
                [mv.position[2] for mv in self.movements]
            )
            self.target_at_time = newton_polynomial(
                times,
                [mv.target[0] for mv in self.movements],
                [mv.target[1] for mv in self.movements],
                [mv.target[2] for mv in self.movements]
            )

            self._move()
        else:
            time = 0
            prev_mv = None
            prev_trg = (0, 0, 0)
            prev_pos = (0, 0, 0)
            with _bascenev1.get_foreground_host_activity().context:
                for i, mv in enumerate(self.movements):
                    bs.timer(time, bui.Call(self.animate, prev_mv, mv,
                                            'position', prev_pos, mv.position,
                                            mv.during_time))
                    bs.timer(time, bui.Call(self.animate, prev_mv, mv, 'target',
                                            prev_trg, mv.target,
                                            mv.during_time))
                    prev_mv = mv
                    prev_trg = mv.target
                    prev_pos = mv.position
                    time += mv.during_time

    def animate(self,
                prev_movement: Union[Movement, None],
                movement: Movement,
                attribute: str,
                start_position: tuple,
                end_position: tuple,
                total_time: float):

        if prev_movement:
            if prev_movement.active:
                with _bascenev1.get_foreground_host_activity().context:
                    return bs.timer(0.01, bs.Call(self.animate,
                                                  prev_movement,
                                                  movement,
                                                  attribute,
                                                  start_position,
                                                  end_position,
                                                  total_time))
        movement.active = True

        if total_time <= 0:
            return setattr(self, attribute, end_position)

        time = 0.0
        difference = bs.Vec3(end_position) - bs.Vec3(start_position)

        def _update():
            nonlocal time

            array = getattr(self, attribute)
            for i in range(3):
                array[i] = (start_position[i] + difference[i]
                            * (time / total_time))
            setattr(self, attribute, array)

            if time / total_time < 1.0:
                time += 0.01
                with _bascenev1.get_foreground_host_activity().context:
                    bs.timer(0.01, _update)
            else:
                movement.active = False

        with _bascenev1.get_foreground_host_activity().context:
            bs.timer(0.01, _update)

    def _move(self) -> None:
        """Move camera process.

        Every 0.01 seconds update camera attrs and check time.
        """

        def _update() -> None:
            self.current_time += 0.01

            self.position = self.position_at_time(self.current_time)
            self.target = self.target_at_time(self.current_time)

            if self.current_time >= self.end_time:
                self.active = False
                return

            with _bascenev1.get_foreground_host_activity().context:
                bs.timer(0.01, _update)

        with _bascenev1.get_foreground_host_activity().context:
            bs.timer(0.01, _update)
