from math import floor, sqrt


class TaskInput:
    def __init__(self, dimensions, your_position, trainer_position, distance):
        self.dimensions = dimensions
        self.your_position = your_position
        self.trainer_position = trainer_position
        self.distance = distance


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x, self.y) == (self.x, self.y)


class Dimensions:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class Line:
    def __init__(self, a, b, vertical_x=None):
        self.a = a
        self.b = b
        self.vertical_x = vertical_x





class LinesSpread:
    def __init__(self, point_a, point_b, distance=None):
        self.point_a = point_a
        self.point_b = point_b
        self.distance = distance


class LinesSpreadIntersection:
    pass


def solution(dimensions, your_position, trainer_position, distance):
    task_input = TaskInput(
        Dimensions(dimensions[0], dimensions[1]),
        Point(your_position[0], your_position[1]),
        Point(trainer_position[0], trainer_position[1]),
        distance
    )

    central_directions, central_ignore = central(task_input)
    north_directions, north_ignore = north(task_input, central_ignore)
    south_directions, south_ignore = south(task_input, central_ignore)
    west_directions, west_ignore = west(task_input, central_ignore)
    east_directions, east_ignore = east(task_input, central_ignore)
    north_west_directions = north_west(
        task_input,
        central_ignore + north_ignore + west_ignore
    )
    north_east_directions = north_east(
        task_input,
        central_ignore + north_ignore + east_ignore
    )
    south_west_directions = south_west(
        task_input,
        central_ignore + south_ignore + west_ignore
    )
    south_east_directions = south_east(
        task_input,
        central_ignore + south_ignore + east_ignore
    )

    return (
            central_directions +
            north_directions +
            south_directions +
            east_directions +
            west_directions +
            north_west_directions +
            north_east_directions +
            south_west_directions +
            south_east_directions
    )


def central(task_input):
    your_position = task_input.your_position
    trainer_position = task_input.trainer_position
    distance = task_input.distance
    dimensions = task_input.dimensions

    trainers = [trainer_position]
    trainers += mirror_reflections(trainer_position, dimensions)
    your_clones = mirror_reflections(your_position, dimensions)

    trainers_to_shoot = []
    positions_to_check = trainers + your_clones

    for trainer in trainers:
        if distance_between(your_position, trainer) > distance:
            continue

        between = False
        for position in positions_to_check:
            if is_point_between(position, your_position, trainer):
                between = True
                break

        if not between:
            trainers_to_shoot.append(trainer)

    lines_to_ignore = [
        LinesSpread(task_input.your_position, trainer)
        for trainer in trainers_to_shoot
    ]

    return len(trainers_to_shoot), lines_to_ignore


def mirror_reflections(point, dimensions):
    return [
        mirror_reflection_top(point, dimensions)
        mirror_reflection_right(point, dimensions),
        mirror_reflection_top_right(point, dimensions)
    ]


def mirror_reflection_top(point, dimensions):
    return Point(point.x, point.y + 2 * (dimensions.height - point.y))


def mirror_reflection_right(point, dimensions):
    return Point(point.x + 2 * (dimensions.width - point.x), point.y)


def mirror_reflection_top_right(point, dimensions):
    return Point(
        point.x + 2 * (dimensions.width - point.x),
        point.y + 2 * (dimensions.height - point.y)
    )


def is_point_between(checked, a, b):
    if checked == a or checked == b:
        return False

    if b.x == a.x:
        return checked.x == b.x and min(a.y, b.y) < checked.y < max(a.y, b.y)

    line_equation_a = (b.y - a.y) / (b.x - a.x)  # fix floating division
    line_equation_b = a.y - (a.x * line_equation_a)

    line_y_at_x = checked.x * line_equation_a + line_equation_b
    return (
            line_y_at_x == checked.y and
            min(a.x, b.x) <= checked.x <= max(a.x, b.x) and
            min(a.y, b.y) <= checked.y <= max(a.y, b.y)
    )


def distance_between(a, b):
    return sqrt(((a.x - b.x) ** 2) + ((a.y - b.y) ** 2))


def north(task_input, lines_spreads_to_ignore):
    your_position = task_input.your_position
    trainer_position = task_input.trainer_position
    dimensions = task_input.dimensions

    if your_position.x == trainer_position.x:
        directions_left = 0
        ignore_left = []
    else:
        directions_left, ignore_left = north_column(
            task_input,
            trainer_position,
            lines_spreads_to_ignore
        )

    directions_right, ignore_right = north_column(
        task_input,
        mirror_reflection_right(trainer_position, dimensions),
        lines_spreads_to_ignore
    )

    return directions_left + directions_right, ignore_left + ignore_right


def north_column(task_input, first_trainer_position, lines_spreads_to_ignore):
    your_position = task_input.your_position
    trainer_position = task_input.trainer_position
    distance = task_input.distance
    dimensions = task_input.dimensions

    lines_spread = LinesSpread(
        your_position,
        first_trainer_position,
        2 * dimensions.height
    )
    directions = points_within_distance(lines_spread, distance) - 2

    min_y = lines_spread.point_b.y
    max_y = min_y + ((directions - 1) * lines_spread.distance)
    directions -= points_on_intersection_at_x(
        [lines_spread] + lines_spreads_to_ignore,
        lines_spread.point_b.x,
        min_y,
        max_y
    )

    if your_position.x == trainer_position.x:
        return directions, [lines_spread]


def points_within_distance(lines_spread, distance):
    """Number of points that meet certain constraints.

    The constraints are:
    1. They must belong to the `lines_spread` (be positioned at it).
    2. They must be within `distance` from the `lines_spread.point_a`.
    3. Their x coordinate must be equal to `lines_spread.point_b.x`.
    """
    a = lines_spread.point_a
    b = lines_spread.point_b
    lines_spread_distance_squared = (lines_spread.distance ** 2)

    under_sqrt = (
            -a.x ** 2 * lines_spread_distance_squared +
            2 * a.x * b.x * lines_spread_distance_squared -
            b.x ** 2 * lines_spread_distance_squared +
            distance ** 2 * lines_spread_distance_squared
    )

    top = (
            sqrt(under_sqrt) +
            a.y * lines_spread.distance -
            b.y * lines_spread.distance
    )

    threshold = top / lines_spread_distance_squared + 1  # fix float division
    return floor(threshold)
    # floor(equation generated by wolphram) + 1
    # check if the equation work
    # float division fix


def points_on_intersection_at_x(line_spread, line_spread_list, x, until):
    """Number of points that meet certain constraints.

    To do: refactor so that min_y and max_y is given as argument and `line_spread`
    is in the line_spread_list.

    It's already used as if it was already refactored (in the north_column)

    The constraints are:
    1. They must belong to the intersection of `line_spread` and all
        line spreads from `line_spread_list`.
    2. Their x coordinate must be x.
    3. Their y coordinate can't be higher than:
    line_spread.point_b.y + ((until - 1) * line_spread.distance)
    """
    max_y = line_spread.point_b.y + ((until - 1) * line_spread.distance)

    result = 0
    for line_spread_from_list in line_spread_list:
        if line_spread_from_list.distance is None:
            line = Line.from_points(
                line_spread_from_list.point_a,
                line_spread_from_list.point_b
            )
            y = line.y_at_x(x)
            if line_spread.does_point_belong(Point(x, y)) and y < max_y:
                result += 1
        # handle distance not None later, not needed for North

    return result

def line_through(a, b):
    if b.x == a.x:
        return Line()

    line_equation_a = (b.y - a.y) / (b.x - a.x)  # fix floating division
    line_equation_b = a.y - (a.x * line_equation_a)
    return Line(line_equation_a, line_equation_b)