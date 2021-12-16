from __future__ import annotations

from typing import Optional

import ba
import _ba

from cinema_camera.movement import Movement
from cinema_camera.tools.calculate import newton_polynomial


class Camera:
    """Camera class.

    Main class of CC

    Automatically receives/changes the attributes of the game camera,
    when receiving/changing the relevant attributes of this class.
    """

    @property
    def position(self) -> ba.Vec3:
        return ba.Vec3(_ba.get_camera_position())

    @position.setter
    def position(self, value: Optional[ba.Vec3]) -> ba.Vec3:
        assert isinstance(value, ba.Vec3)
        _ba.set_camera_position(value.x, value.y, value.z)

    @property
    def target(self) -> ba.Vec3:
        return ba.Vec3(_ba.get_camera_target())

    @target.setter
    def target(self, value: Optional[ba.Vec3]) -> ba.Vec3:
        assert isinstance(value, ba.Vec3)
        _ba.set_camera_target(value.x, value.y, value.z)

    def __init__(self):
        self.movements: list[Movement] = []
        self.position_at_time: callable = lambda x: x
        self.target_at_time: callable = lambda x: x

        self.current_time: float = -9999
        self.end_time: float = -9999
        self.active: bool = False

    def add_movement(self, movement: Movement) -> None:
        self.movements.append(movement)

    def start_move(self):
        """Starts moving.

        Preparing a data for moving.

        Forms a lists of movement's data and times list,
        then uses it for calculating moving functions.

        And if all right calling self._move().
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
        # FIXME: check settings for newton polynomial
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

            _ba.timer(0.01, _update)

        _ba.timer(0.01, _update)
