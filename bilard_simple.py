"""Solve bringing a gun

The solution passes all tests but one. I have found a few different
solutions that solve this task with time complexity: (n/max(dx, dy))^2
where n - maximum distance, dx and dy - dimensions, but I wouldn't
expect them to pass the worst case test too. I haven't found anything
better than that time complexity, although possibly I was close.
"""


from copy import copy


YOU = 0
TRAINER = 1

LEFT = 0
RIGHT = 1

UP = 0
DOWN = 1

directions = {}


def solution(dimensions, your_position, trainer_position, distance):
    for person in (YOU, TRAINER):
        for vertical_direction in (UP, DOWN):
            for horizontal_direction in (RIGHT, LEFT):
                central = your_position if person == YOU else trainer_position
                starting_positions = [
                    central,
                    mirror_top(central, dimensions),
                    mirror_right(central, dimensions),
                    mirror_top_right(central, dimensions)
                ]
                for starting_position in starting_positions:
                    search(
                        dimensions,
                        your_position,
                        starting_position,
                        distance,
                        vertical_direction,
                        horizontal_direction,
                        person
                    )
    neighbours(dimensions, your_position, your_position, distance, YOU)
    neighbours(dimensions, trainer_position, your_position, distance, TRAINER)
    return trainer_directions()


def mirror_top(position, dimensions):
    return (
        position[0],
        position[1] + 2 * (dimensions[1] - position[1])
    )


def mirror_right(position, dimensions):
    return (
        position[0] + 2 * (dimensions[0] - position[0]),
        position[1]
    )


def mirror_top_right(position, dimensions):
    return (
        position[0] + 2 * (dimensions[0] - position[0]),
        position[1] + 2 * (dimensions[1] - position[1])
    )


def search(
        dimensions,
        your_position,
        starting_position,
        distance,
        vertical,
        horizontal,
        person
):
    fixed_starting_position = fix_position(your_position, starting_position)
    position = copy(fixed_starting_position)
    two_width = 2 * dimensions[0]
    two_height = 2 * dimensions[1]
    while is_within_distance(position, distance):
        while is_within_distance(position, distance):
            check(position, person)
            position[1] += two_height if vertical == UP else -two_height
        position[0] += two_width if horizontal == RIGHT else -two_width
        position[1] = fixed_starting_position[1]


def fix_position(your_position, position):
    return [
        position[0] - your_position[0],
        position[1] - your_position[1]
    ]


def is_within_distance(position, distance):
    return position[0] ** 2 + position[1] ** 2 <= distance ** 2


def check(position, person):
    if position == [0, 0]:
        return

    simple = simplify(position)
    direction = (
        position[0] ** 2 + position[1] ** 2,
        person
    )
    if simple in directions:
        directions[simple].append(direction)
        return
    directions[simple] = [direction]


def simplify(position):
    if position[0] == 0:
        return 0, 1 if position[1] > 0 else -1
    if position[1] == 0:
        return 1 if position[0] > 0 else -1, 0

    gcd_ = gcd(abs(position[0]), abs(position[1]))
    return position[0] / gcd_, position[1] / gcd_


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def neighbours(dimensions, position, your_position, distance, person):
    positions = (
        mirror_left(position),
        mirror_top_left(position, dimensions),
        mirror_bottom_right(position, dimensions),
        mirror_bottom(position),
        mirror_bottom_left(position),
    )
    for position in positions:
        fixed = fix_position(your_position, position)
        if is_within_distance(fixed, distance):
            check(fixed, person)


def mirror_bottom(position):
    return (
        position[0],
        -position[1]
    )


def mirror_left(position):
    return (
        -position[0],
        position[1]
    )


def mirror_top_left(position, dimensions):
    return (
        -position[0],
        position[1] + 2 * (dimensions[1] - position[1])
    )


def mirror_bottom_right(position, dimensions):
    return (
        position[0] + 2 * (dimensions[0] - position[0]),
        -position[1]
    )


def mirror_bottom_left(position):
    return (
        -position[0],
        -position[1]
    )



def trainer_directions():
    result = 0

    for simple in directions:
        min_distance = float('inf')
        min_person = None
        for direction in directions[simple]:
            if min_distance > direction[0]:
                min_distance = direction[0]
                min_person = direction[1]
        if min_person == TRAINER:
            result += 1

    return result
