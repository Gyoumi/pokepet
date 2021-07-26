import random
def binarySearchExpGain(level):
    start = 36
    end = 410

    mid = 1
    while start < end:
        mid = start + ((end - start)//2)
        rand = random.randrange(0, 101) * (0.023 * max(level, 70))
        if rand > 50:
            start = mid + 1
        else:
            end = mid - 1
            
    if mid > 400:
        mid *= 5

    enemy = random.randrange(-5, 6)
    return mid, enemy