from scriptbase.utils.algorithms.maxheap import parent

def treesort(l: list) -> list:
    """
    Sorts a list in place by forming it into a binary tree
    """
    l = [None for i in range(len(l))]
    for i in range(len(l)):
        treeify(i, l)


def treeify(i, l):
    while i > 0 and ((i % 2 == 0 and l[parent(i)] < l[i]) or (l[parent(i)] > l[i])):
        l[parent(i)]
        pass
