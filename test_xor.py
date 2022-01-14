from xor import solution


def bruteforce_solution(start, length):
    a = []
    current = start
    for i in range(length):
        a.append([])
        for j in range(length):
            a[i].append(current)
            current += 1

    result = 0
    for i in range(length):
        for j in range(length - i):
            result = result ^ a[i][j]
    return result


def test_bruteforce_solution():
    assert bruteforce_solution(0, 3) == 2
    assert bruteforce_solution(17, 4) == 14


def test_solution():
    correct = 0
    all = 0
    for i in range(0, 10):
        for j in range(1, 10):
            b = bruteforce_solution(i, j)
            s = solution(i, j)

            print("Testing " + str(i) + ", " + str(j))
            print("BruteForce: " + str(b))
            print("Solution: " + str(s))
            print("")

            if b == s:
                correct += 1
            all += 1

    print("correct: " + str(correct))
    print("all: " + str(all))


test_solution()


def odd_of_odd_between(first_in_row, last_in_row):
    if first_in_row % 2:
        return ((last_in_row - first_in_row) / 2) % 2 == 0
    return ((last_in_row - first_in_row + 1) / 2) % 2 == 1


assert odd_of_odd_between(0, 2)
assert odd_of_odd_between(0, 1)
assert odd_of_odd_between(0, 6)
assert odd_of_odd_between(0, 5)
assert not odd_of_odd_between(0, 3)
assert not odd_of_odd_between(0, 4)
assert odd_of_odd_between(1, 5)
assert odd_of_odd_between(2, 4)
assert not odd_of_odd_between(1, 3)
assert odd_of_odd_between (2, 3)