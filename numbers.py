def solution(l):
    mod3 = {i: [] for i in range(3)}
    for digit in l:
        mod3[digit % 3].append(digit)
    for key in mod3:
        mod3[key].sort(reverse=True)

    digits_sum = sum(l)
    remainder = digits_sum % 3

    if remainder != 0:
        if mod3[remainder]:
            mod3[remainder].pop()
        else:
            another = 2 if remainder == 1 else 1
            if len(mod3[another]) >= 2:
                mod3[another].pop()
                mod3[another].pop()
            else:
                return 0

    remaining_digits = []
    for i in range(3):
        remaining_digits += mod3[i]
    remaining_digits.sort(reverse=True)

    result = 0
    for digit in remaining_digits:
        result = result * 10 + digit

    return result
