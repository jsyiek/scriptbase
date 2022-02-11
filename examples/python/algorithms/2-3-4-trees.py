from typing import List


class two_three_four_tree:
    def __init__(self, key: int):
        self.keys = [key]
        self.branches: List['two_three_four_tree'] = []

    def __repr__(self):
        j = ''.join([b.__repr__() for b in self.branches])
        return_val = f"[{self.keys} -> {j}]"
        return return_val

    def insert_key(self, key: int) -> int:
        # PRECONDITION: Only called when len(self.keys) < 3
        i = 0
        while i < len(self.keys) and self.keys[i] - key < 0:
            i += 1
        self.keys.insert(i, key)
        return i

    def insert(self, item: int):
        if item in self.keys:
            return

        if len(self.branches) == 0:
            if len(self.keys) == 3:
                new_self = self.split()
                new_self.insert(item)
                self.branches = new_self.branches
                self.keys = new_self.keys
                return

            self.insert_key(item)
            return

        i = 0
        while i < len(self.keys) and self.keys[i] - item < 0:
            i += 1

        possible_new_node = self.branches[i].insert(item)
        if possible_new_node is not None:
            if len(self.keys) == 3:
                new_self = self.split()
                new_index = new_self.insert_key(possible_new_node.keys[0])
                new_self.branches.insert(new_index, possible_new_node.branches[1])
                new_self.branches.insert(new_index, possible_new_node.branches[0])
                self.branches = new_self.branches
                self.keys = new_self.keys
                return self
            new_index = self.insert_key(possible_new_node.keys[0])
            self.branches.insert(new_index, possible_new_node.branches[1])
            self.branches.insert(new_index, possible_new_node.branches[0])


    def split(self):
        # PRECONDITION: Only called when len(self.keys) == 3
        middle_key = self.keys[1]
        new_node = two_three_four_tree(middle_key)
        new_node.branches = [two_three_four_tree(self.keys[0]), two_three_four_tree(self.keys[2])]
        new_node.branches[0].branches = self.branches[:2]
        new_node.branches[1].branches = self.branches[2:]

        return new_node


if __name__ == "__main__":
    tree = two_three_four_tree(5)
    tree.insert(6)
    tree.insert(7)
    tree.insert(8)
    tree.insert(4)
    tree.insert(3)
    tree.insert(2)
    tree.insert(5)
    for x in range(1000):
        tree.insert(x)
    print(tree)
