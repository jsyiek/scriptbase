from typing import List


def parent(index):
    return (index - 2)//2 if not (index % 2) else (index - 1) // 2


def heapify(l: List[int]):

    for i in range(len(l)):
        heapify_index(l, i)

    return l


def heapify_index(l: List[int], i: int):
    while i > 0 and l[parent(i)] < l[i]:
        new_i = parent(i)
        l[i], l[new_i] = l[new_i], l[i]
        i = new_i


def push(l: List[int], e: int):
    l.append(e)
    heapify_index(l, len(l) - 1)
    return l


def popmax(l: List[int]):
    element = l.pop(0)
    heapify(l)
    return element


if __name__ == "__main__":
    data = [1,10,85,12,3,6,102,27,37]
    print(heapify(data))
    print(popmax(data))
    print(data)
    print(push(data, 1000))
