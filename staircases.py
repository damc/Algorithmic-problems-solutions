"""Solves the-grandest-staircase-of-them-all

Solution:
Start from the first (biggest) step. For each possible number of bricks
that you can put in the first step, calculate the number of possible
combinations of the staircases that can be put after that first step
with the remaining number of bricks. Sum the numbers of possible
combinations and return the result.

The number of possible combinations of the staircases that can be put
after that first step can be calculated in the same way, recursively.

For number of bricks <= 2, the solutions are hardcoded.

Cache the results of the recursive function so that you don't repeat
calculations.
"""


def solution(n):
    """Solve the-grandest-staircase-of-them-all

    Args:
        n (int): number of bricks, n >= 3

    Returns:
        int: number of different staircases
    """
    return staircases(n, float('inf'), 0)


cache = {}
"""dict: cache for results of staircases() function"""


def staircases(n, max_height, previous_steps):
    """Number of different steps combinations with some constraints.

    Calculates how many different steps combinations there is for the
    given number of bricks. Each step must be lower than the previous
    one. It assumes that the staircase has been already started with
    `previous_steps` number of steps (but the bricks in the previous
    steps are not included in `n`).

    Args:
        n (int): number of bricks to construct the staircase from
        max_height (int, float): max allowed height of a step
        previous_steps (int): number of previous steps in the staircase

    Returns:
        int: number of possible staircases.
    """
    cache_key = n, max_height, previous_steps
    if cache_key in cache:
        return cache[cache_key]

    if n <= 2:
        result = staircases_edge_case(n, max_height, previous_steps)
        cache[cache_key] = result
        return result

    options = 0
    biggest_possible = min(n, max_height)
    for i in range(1, biggest_possible + 1):
        options += staircases(n - i, i - 1, previous_steps + 1)

    cache[cache_key] = options
    return options


def staircases_edge_case(n, max_height, previous_steps):
    """Number of steps combinations for an edge case.

    See `staircases` docs for more details

    Args:
        n (int): number of bricks to construct the staircase from
        max_height (int, float): max allowed height of a step
        previous_steps: number of previous steps in the staircase

    Returns:
        int, None: number of possible staircases or None, if the case
            is not an edge case.
    """
    if previous_steps >= 2:
        if n == 2 and max_height >= 2:
            return 1
        if n == 2 and max_height < 2:
            return 0
        if n == 1 and max_height >= 1:
            return 1
        if n == 1 and max_height < 1:
            return 0
        if n == 0 and max_height >= 0:
            return 1
    if previous_steps == 1:
        if n == 2 and max_height >= 2:
            return 1
        if n == 2 and max_height < 2:
            return 0
        if n == 1 and max_height >= 1:
            return 1
        if n == 1 and max_height < 1:
            return 0
        if n == 0 and max_height >= 0:
            return 0
    if previous_steps == 0:
        if n <= 2:
            return 0
    return None
