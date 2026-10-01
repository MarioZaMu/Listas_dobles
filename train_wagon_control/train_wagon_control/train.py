"""Train wagon control built on a doubly linked list.

Data Structures - Doubly linked lists.
Every wagon is a node with two pointers: next and prev.
Run it without a UI:  python train.py
"""


class Wagon:
    """List node: wagon data plus two pointers."""

    def __init__(self, wagon_id, wagon_type, cargo):
        self.id = wagon_id
        self.type = wagon_type
        self.cargo = cargo
        self.next = None   # following wagon
        self.prev = None   # previous wagon


class Train:
    """Doubly linked list of wagons."""

    def __init__(self):
        self.head = None      # first wagon
        self.tail = None      # last wagon
        self.length = 0
        self.current = None   # selected wagon (used to traverse)
        self._counter = 0     # ids are never reused

    def _new_wagon(self, wagon_type, cargo):
        self._counter += 1
        return Wagon(f"V{self._counter}", wagon_type, cargo)

    # add to end
    def append(self, wagon_type, cargo):
        new_wagon = self._new_wagon(wagon_type, cargo)
        if self.head is None:
            self.head = new_wagon
            self.tail = new_wagon
            self.current = new_wagon
        else:
            new_wagon.prev = self.tail
            self.tail.next = new_wagon
            self.tail = new_wagon
        self.length += 1
        return new_wagon

    # add to start
    def prepend(self, wagon_type, cargo):
        new_wagon = self._new_wagon(wagon_type, cargo)
        if self.head is None:
            self.head = new_wagon
            self.tail = new_wagon
            self.current = new_wagon
        else:
            new_wagon.next = self.head
            self.head.prev = new_wagon
            self.head = new_wagon
        self.length += 1
        return new_wagon

    # reach an index starting from the closest end
    def traverse_to_index(self, index):
        if index < 0 or index >= self.length:
            raise IndexError("No wagon at that position.")
        if index <= self.length // 2:
            node = self.head
            for _ in range(index):
                node = node.next
        else:
            node = self.tail
            for _ in range(self.length - 1 - index):
                node = node.prev
        return node

    # insert at an index
    def insert(self, index, wagon_type, cargo):
        if index <= 0:
            return self.prepend(wagon_type, cargo)
        if index >= self.length:
            return self.append(wagon_type, cargo)
        new_wagon = self._new_wagon(wagon_type, cargo)
        leader = self.traverse_to_index(index - 1)
        follower = leader.next
        leader.next = new_wagon
        new_wagon.prev = leader
        new_wagon.next = follower
        follower.prev = new_wagon
        self.length += 1
        return new_wagon

    # delete at an index
    def remove(self, index):
        node = self.traverse_to_index(index)
        if node.prev is not None:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next is not None:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        if self.current is node:
            self.current = node.next or node.prev
        node.next = None
        node.prev = None
        self.length -= 1
        return node

    # traverse in both directions
    def go_next(self):
        if self.current is None or self.current.next is None:
            return False
        self.current = self.current.next
        return True

    def go_prev(self):
        if self.current is None or self.current.prev is None:
            return False
        self.current = self.current.prev
        return True

    def go_head(self):
        self.current = self.head

    def go_tail(self):
        self.current = self.tail

    def index_of(self, node):
        i = 0
        node_at = self.head
        while node_at is not None:
            if node_at is node:
                return i
            node_at = node_at.next
            i += 1
        return -1

    def to_text(self):
        parts = []
        node = self.head
        while node is not None:
            parts.append(node.id)
            node = node.next
        return " <-> ".join(parts) if parts else "(empty train)"

    def print_list(self):
        print(self.to_text())


if __name__ == "__main__":
    train = Train()
    train.append("passenger", "48 passengers")
    train.append("cargo", "Coffee, 22 t")
    train.append("tank", "Fuel")
    train.prepend("dining", "Restaurant")
    train.print_list()                    # V4 <-> V1 <-> V2 <-> V3
    train.insert(2, "passenger", "30 passengers")
    train.print_list()                    # V4 <-> V1 <-> V5 <-> V2 <-> V3
    train.remove(0)
    train.print_list()                    # V1 <-> V5 <-> V2 <-> V3
    train.go_tail()
    while train.go_prev():                # walk backwards using prev
        print("moved back to", train.current.id)
