from __future__ import annotations

from typing import Union, Optional, List

import _ba
import ba

from cinema_camera.movement import Movement
from cinema_camera.tools.calculate import newton_polynomial


class Camera:

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
        self.movements: List[Movement] = []
        self.smooth: callable = lambda x: x
        self.smooth_target: callable = lambda x: x
        self.move_time: float = -9999

    def add_movement(self, movement: Movement) -> None:
        self.movements.append(movement)

    def move(self):
        self.move_time = 0

        times = []
        now_time = 0.0
        for mv in self.movements:
            times.append(mv.during_time + now_time)
            now_time = times[-1]

        self.smooth = newton_polynomial(
            times,
            [mv.position[0] for mv in self.movements],
            [mv.position[1] for mv in self.movements],
            [mv.position[2] for mv in self.movements]
        )

        self.smooth_target = newton_polynomial(
            times,
            [mv.target[0] for mv in self.movements],
            [mv.target[1] for mv in self.movements],
            [mv.target[2] for mv in self.movements]
        )

        with ba.Context('ui'):
            cur_time = 0.0
            for i, mv in enumerate(self.movements):
                _ba.timer(float(cur_time) + i * 0.05, ba.Call(mv.start, self.movements[i - 1]))
                cur_time += mv.during_time

    def move_to(self, movement: Movement, previous_movement: Union[Movement, None]) -> None:
        """Move camera

        Smooth camera move to the specified position.

        Arguments:
            movement - destination information (Movement)
            previous_movement - previous movement, if it exists (Union[Movement, None])

        Return:
            -> None
        """

        if previous_movement:
            if previous_movement != movement:
                if previous_movement.active:
                    with ba.Context('ui'):
                        _ba.timer(0.01, ba.Call(self.move_to, movement, previous_movement))
                    return

        print('move_to:', movement.position, 'called')

        original_position = self.position
        original_target = self.target
        displacement_vector = movement.position - self.position
        displacement_target_vector = movement.target - self.target

        dt = movement.during_time

        if dt<=0.0:
            self.position = movement.position
            self.target = movement.target
            print('-> end, position:', self.position)
            movement.active = False
            return

        graph_x = movement.graph.get('x', lambda x: x)
        graph_y = movement.graph.get('y', lambda x: x)
        graph_z = movement.graph.get('z', lambda x: x)

        update_count = 0
        need_update_count = dt / 0.01
        last = 0

        def _update() -> None:
            nonlocal update_count, last
            current_time = update_count * 0.01
            self.move_time += 0.01
            end_time = need_update_count * 0.01
            new_position = \
                original_position + ba.Vec3(
                    (
                            graph_x(current_time / end_time) *
                            displacement_vector.x
                    ),
                    (
                            graph_y(current_time / end_time) *
                            displacement_vector.y
                    ),
                    (
                            graph_z(current_time / end_time) *
                            displacement_vector.z
                    ))
            new_target = \
                original_target + ba.Vec3(
                    (
                            graph_x(current_time / end_time) *
                            displacement_target_vector.x
                    ),
                    (
                            graph_y(current_time / end_time) *
                            displacement_target_vector.y
                    ),
                    (
                            graph_z(current_time / end_time) *
                            displacement_target_vector.z
                    ))

            # self.position = new_position
            self.position = self.smooth(self.move_time)
            # self.target = new_target
            self.target = self.smooth_target(self.move_time)

            if update_count >= need_update_count:
                update_count = 0
                print('-> end, position:', self.position)
                movement.active = False
                return

            if update_count % 10 == 0:
                pl_vec = new_position - original_position
                print(f'speed x:', pl_vec.x - last)
                last = pl_vec.x
            update_count += 1
            _ba.timer(0.01, _update)

        _ba.timer(0.01, _update)
