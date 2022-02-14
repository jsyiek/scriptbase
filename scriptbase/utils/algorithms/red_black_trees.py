from typing import List


class RedBlackTree:

    def __init__(self, key: int):
        # 0 = black, 1 = red
        self.is_red = False
        self.key = key
        self.children: List[RedBlackTree] = [None, None]

    def __repr__(self):
        j = ', '.join([b.__repr__() for b in self.children])
        return_val = f"[{self.key} ({'Red' if self.is_red else 'Black'}) -> {j}]"
        return return_val

    @classmethod
    def create_red_node(cls, key: int):
        new_node = RedBlackTree(key)
        new_node.is_red = True
        return new_node

    def flip(self):
        self.is_red = not self.is_red

    def insert(self, key: int):
        if key == self.key:
            return
        elif key > self.key:
            if self.children[1] is None:
                self.children[1] = RedBlackTree.create_red_node(key)
            else:
                self.children[1].insert(key)
        else: # key < self.key
            if self.children[0] is None:
                self.children[0] = RedBlackTree.create_red_node(key)
            else:
                self.children[0].insert(key)
        self.balance()

    def rotate_right(self):
        left_child = self.children[0]
        left_child_key, (left_child_left, left_child_right) = left_child.key, left_child.children

        key, (left, right) = self.key, self.children

        self.key = left_child_key
        self.children = [left_child_left, left]

        left_child.key = key
        left_child.children = [left_child_right, right]

        self.is_red, left_child.is_red = left_child.is_red, self.is_red

    def rotate_left(self):
        right_child = self.children[1]
        right_child_key, (right_child_left, right_child_right) = right_child.key, right_child.children

        key, (left, right) = self.key, self.children

        self.key = right_child_key
        self.children = [right, right_child_right]

        right_child.key = key
        right_child.children = [left, right_child_left]

        self.is_red, right_child.is_red = right_child.is_red, self.is_red

    def balance(self):
        if self.is_red and all(c is not None for c in self.children):
            if self.is_red == self.children[0].is_red == self.children[1].is_red == 0:
                self.flip()
                self.rotate_right()
        elif self.children[1] is not None and self.is_red == self.children[1].is_red and self.children[0] is None:
            if self.is_red:
                self.children[1].flip()
            else:
                self.flip()
            self.rotate_left()
        elif self.children[0] is not None and self.is_red == self.children[0].is_red and self.children[1] is None:
            if self.is_red:
                self.children[0].flip()
            else:
                self.flip()
            self.rotate_right()

        # elif self.children[1] is not None and self.is_red == self.children[1].is_red and self.children[0] is None:
        #     self.children[1].flip()
        #     self.rotate_left()
        # elif self.children[0] is not None and self.is_red == self.children[0].is_red and self.children[1] is None:
        #     self.flip()


if __name__ == "__main__":
    tree = RedBlackTree(5)
    tree.insert(7)
    tree.insert(6)
    tree.insert(10)
    tree.insert(11)
    tree.insert(12)
    print(tree)
