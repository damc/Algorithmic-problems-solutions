"""Solve queue-to-do

Time complexity: log(m) * n
Space complexity: log(m)
m - id of the last checked worker
n - length of the checkpoint line
"""

from copy import copy


def solution(start, length):
    """Solve queue-to-do

    Algorithm:
    Calculate each digit of the binary representation of the result
    separately, one after another. At the end, convert the binary
    representation to decimal and return it.

    Args:
        start(int): first worker id
        length(int): length of the checkpoint line

    Returns:
        int: checksum the trainers would submit before lunch
    """
    last_number_ = start + pow(length, 2) - 1
    binary_length_ = binary_length(last_number_)

    binary_digits = []
    for i in range(binary_length_):
        binary_digits.append(calculate_digit(start, length, i))

    return bin2dec(binary_digits)


def binary_length(number):
    """Calculate the number of digits in binary representation

    Args:
        number(int)

    Returns:
        int: number of digits in binary representation (with no leading
        zeros)
    """
    result = 0
    while number != 0:
        result += 1
        number = number / 2
    return result


def calculate_digit(start, length, position):
    """Calculate a digit of the checksum in the binary representation

    Algorithm:
    The digit is the result of the XOR operation on all digits at the
    position in all numbers of the checked workers' ids.

    If we have an
    expression consisting of 0s and 1s connected with XOR operator,
    then the result is 1 if and only if the number of 1s in the
    expression is odd (because the result changes each time when
    the digit on the right side of the expression is 1 and remains the
    same if the right side is 0).

    For each row, we check if the number of 1s in that row is odd.
    If the number of rows like that is odd, then the number of all
    1s at that position is also odd, otherwise it's even. Therefore,
    we return 1 in the first case and 0 in the second case.

    Args:
        start(int): first worker id
        length(int): length of the checkpoint line
        position(int): position of the digit in the binary
            representation, starting from the least significant digit

    Returns:
        int: digit of the checksum at the given position
    """
    first = start
    ones = 0
    for i in range(length):
        row_length = length - i
        last = first + row_length - 1
        ones += int(ones_odd(first, last, position))
        first += length
    return ones % 2


def ones_odd(first_in_row, last_in_row, position):
    """Calculate if the number of 1s in the row is odd.

    Algorithm:
    It's different depending on the case.

    Args:
        first_in_row(int): First number in the row.
        last_in_row(int): Last number in the row.
        position(int): Position of the digit, starting from the least
            significant digit.

    Returns:
        bool: whether the number of 1s in the row is odd.
    """
    power = pow(2, position)

    quotient_in_first = first_in_row / power
    remainder_in_first = first_in_row % power

    quotient_in_last = last_in_row / power
    remainder_in_last = last_in_row % power

    if first_in_row == last_in_row:
        return bool(quotient_in_first % 2)

    if quotient_in_first == quotient_in_last:
        if quotient_in_first % 2 == 1:
            return bool((last_in_row - first_in_row + 1) % 2)
        return False

    if quotient_in_first + 1 == quotient_in_last:
        if position == 0:
            return 1
        if quotient_in_first % 2 == 1:
            return bool(remainder_in_first % 2)
        return bool((remainder_in_last + 1) % 2)

    if quotient_in_first + 1 < quotient_in_last:
        if position == 0:
            return odd_of_odd_between(first_in_row, last_in_row)

        result = 0
        if quotient_in_first % 2 == 1:
            result += remainder_in_first
        if quotient_in_last % 2 == 1:
            result += remainder_in_last + 1
        return bool(result % 2)


def odd_of_odd_between(first, last):
    """Whether the number of odd numbers between the arguments is odd

    This is inclusive with respect to the arguments.
    
    Args:
        first(int)
        last(int)

    Returns:
        bool: Whether the number of odd numbers between the arguments
            is odd (inclusive).
    """
    if first % 2:
        return ((last - first) / 2) % 2 == 0
    return ((last - first + 1) / 2) % 2 == 1


def bin2dec(binary_digits):
    """Convert binary number to decimal

    Args:
        binary_digits(list): contains the digits in the binary
            representation, starting from the least significant digit

    Returns:
        int: converted number
    """
    binary_digits_reversed = copy(binary_digits)
    binary_digits_reversed.reverse()
    result = 0
    for digit in binary_digits_reversed:
        result = result * 2 + digit
    return result
