from __future__ import annotations

import ba
from ba import app

from typing import Union, Dict

from cinema_camera.tools.calculate import try_calculate


class Movement:

    def __init__(self,
                 num: int,
                 position: ba.Vec3,
                 target: ba.Vec3,
                 during_time: float,
                 speed_graph_cf: float = 1.0,
                 speed_move_cf: ba.Vec3 = ba.Vec3(1.0, 1.0, 1.0),
                 apply_previous_velocity: bool = False) -> None:
        """Movement

        Movement initialization, in this moment movement are not active,
        for start movement you must run self.start method.

        Arguments:
            position - destination position (ba.Vec3)
            target - destination target position (ba.Vec3)
            during_time - time it takes for the camera to pass the movement (float)
            speed_graph_cf - coefficient of speed over time (callable)
            speed_move_cf - coefficient of move's speed over time (Dict[(str, callable)])
        """

        self.num: int = num
        self.position: ba.Vec3 = position
        self.target: ba.Vec3 = target
        self.during_time: float = during_time
        self.speed_graph_cf: float = speed_graph_cf
        self.speed_move_cf: ba.Vec3 = speed_move_cf
        self.apply_previous_velocity: bool = apply_previous_velocity

        self.graph: Dict[(str, callable)] = {
            'x': try_calculate(lambda x: x ** (self.speed_move_cf.x * self.speed_graph_cf)),
            'y': try_calculate(lambda x: x ** (self.speed_move_cf.y * self.speed_graph_cf)),
            'z': try_calculate(lambda x: x ** (self.speed_move_cf.z * self.speed_graph_cf)),
        }
