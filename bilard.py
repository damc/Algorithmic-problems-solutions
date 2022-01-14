from math import floor, sqrt


FIRST = 0
SECOND = 1


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


class EightPoints:
    def __init__(self, points, trainers):
        self.points = points
        self.trainers = trainers


def solution(dimensions, your_position, trainer_position, distance):
    task_input = TaskInput(
        Dimensions(dimensions[0], dimensions[1]),
        Point(your_position[0], your_position[1]),
        Point(trainer_position[0], trainer_position[1]),
        distance
    )

    directions = top_right(task_input)
    return directions


def top_right(task_input):
    eight_points = eight_points_top_right()
    return (
        smash_trainers(eight_points, task_input, FIRST) +
        smash_trainers(eight_points, task_input, SECOND)
    )


def smash_trainers(eight_points, task_input, which):
    position = eight_points.trainers[0]
    row = 0
    directions = 0
    while is_within_distance(position, task_input.distance):
        directions += directions_in_row(row, which, eight_points, task_input)
        position += 2 * task_input.dimensions.width
        row += 1
    return directions


def eight_points_top_right():
    return EightPoints(None, None)


def directions_in_row(row, which, eight_points, task_input):
    all_points_ = all_points(row, which, eight_points, task_input)
    excluded_points_ = excluded_points(row, which, eight_points, task_input)
    return all_points_ - excluded_points_


def all_points(row, which, eight_points, task_input):
    horizontal_distance = (
            eight_points.trainers[which].x +
            row * 2 * task_input.dimensions.width
    )
    diagonal_distance = task_input.distance
    max_vertical_distance = sqrt(
        diagonal_distance ** 2 -
        horizontal_distance ** 2
    )
    point_distance = 2 * task_input.distance.height
    return floor(max_vertical_distance / point_distance) + 1


def excluded_points(row, which, eight_points, task_input):
    for point in eight_points.points:
        zero_point = Point(
            point.x - 2 * task_input.dimensions.width,
            point.y
        )
        start = relative_point(zero_point, task_input.your_position)
        row_x = (
                eight_points.trainers[which] +
                row * 2 * task_input.dimensions.width
        )
        relative_row_x = relative_coordinate(zero_point.x, row_x)
        # count few varaibles and then do this i something


def relative_point(relative, point):
    return Point(
        point.x - relative.x,
        point.x - relative.y
    )


def relative_coordinate(relative, coordinate):
    return coordinate - relative


def is_within_distance(position, distance):
    return position[0] ** 2 + position[1] ** 2 <= distance ** 2