def solution(x):
    result = ''
    for c in x:
        if ord('a') <= ord(c) <= ord('z'):
            encrypted_ascii = ord('z') - (ord(c) - ord('a'))
            result += chr(encrypted_ascii)
        else:
            result += c
    return result

