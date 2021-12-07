from __future__ import annotations

import ba
from threading import Thread




# from cinema_camera import cm
# cm()
def create_mode() -> None:
    """Easy method for create custom moves.

    Every line enter the movement data:
    >>> {time} {position x} {position y} {position z} {target x} {target y} {target z}

    Double press enter for end creating and show results (will run moves).
    """

    print('Create mode active')
    print('Enter movements data in format:')
    print('{time} {position x} {position y} {position z} {target x} {target y} {target z}')

    def start_create():
        i = 1
        need_end_creating = False
        moves = []
        while not need_end_creating:
            inp = input(f'line {i}: ')

            if not inp:
                break
            elif inp == 'back':
                delete_movement = moves.pop(-1)
                print(f'Successfully delete {i} movement:', delete_movement)

            movement_data = list(map(float, inp.split()))

            if len(movement_data) < 4:
                print('Not enough data')
                continue
            else:
                md = movement_data[:7]
                md += [0.0] * (7 - len(movement_data))
                moves.append(
                    Movement(ba.Vec3(md[1], md[2], md[3]),
                             ba.Vec3(md[4], md[5], md[6]),
                             md[0])
                )
                print(f'Successfully add {i} movement:', moves[-1])
            i += 1

        print(moves)
        ba.pushcall(lambda: run_moves(moves), from_other_thread=True)

    create_mode_thread = Thread(target=start_create)
    create_mode_thread.start()




# from cinema_camera import test1
# test1()
def test1():
    moves = [
        Movement(ba.Vec3(4, 20, 10), ba.Vec3(0, 0, 0), 2.0),
        Movement(ba.Vec3(2, 8, -7), ba.Vec3(0, 3, 0), 0.7),

        Movement(ba.Vec3(0, 5, -10), ba.Vec3(0, 4, 0), 1.0),

        Movement(ba.Vec3(-2, 8, -7), ba.Vec3(0, 3, 0), 1.0),
        Movement(ba.Vec3(-4, 20, 10), ba.Vec3(0, 0, 0), 0.7),
    ]

    run_moves(moves)


cm = create_mode

