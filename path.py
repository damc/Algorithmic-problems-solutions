from collections import deque


def square_number_to_coordinates(square_number):
    return square_number % 8, square_number / 8


def point_distance(source, destination):
    if source == destination:
        return 0

    distance = {source: 0}

    positions = deque()
    positions.append(source)
    while positions:
        position = positions.popleft()
        position_x, position_y = position

        options = [
            (position_x + 2, position_y + 1),
            (position_x + 2, position_y - 1),
            (position_x + 1, position_y + 2),
            (position_x + 1, position_y - 2),
            (position_x - 1, position_y + 2),
            (position_x - 1, position_y - 2),
            (position_x - 2, position_y + 1),
            (position_x - 2, position_y - 1)
        ]
        for option in options:
            option_x, option_y = option
            if not (0 <= option_x < 8 and 0 <= option_y < 8):
                continue
            if option in distance:
                continue
            if option == destination:
                return distance[position] + 1
            distance[option] = distance[position] + 1
            positions.append(option)


def solution(src, dest):
    return point_distance(
        square_number_to_coordinates(src),
        square_number_to_coordinates(dest)
    )
