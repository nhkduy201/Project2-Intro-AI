class MyHeap:
    def __init__(self, arr):
        self.arr = arr
        self.build_heap()

    def swap(self, i, j):
        self.arr[i], self.arr[j] = self.arr[j], self.arr[i]

    def heapify_down(self, i):
        while self.has_left_child(i):
            smaller_child_index = self.get_left_child_index(i)
            if self.has_right_child(i) and self.right_child(i).get_cost_plus_heu() < self.left_child(i).get_cost_plus_heu():
                smaller_child_index = self.get_right_child_index(i)
            if self.arr[i].get_cost_plus_heu() < self.arr[smaller_child_index].get_cost_plus_heu():
                break
            self.swap(i, smaller_child_index)
            i = smaller_child_index

    def heapify_up(self, i):
        while self.has_parent(i) and self.parent(i).get_cost_plus_heu() > self.arr[i].get_cost_plus_heu():
            self.swap(self.get_parent_index(i), i)
            i = self.get_parent_index(i)

    def build_heap(self):
        for i in range(len(self.arr)//2 - 1, -1, -1):
            self.heapify_down(i)

    def poll(self):
        if len(self.arr) == 0:
            return
        self.arr[-1], self.arr[0] = self.arr[0], self.arr[-1]
        val = self.arr[-1]
        self.arr.pop()
        self.heapify_down(0)
        return val

    def add(self, item):
        self.arr.append(item)
        self.heapify_up(len(self.arr) - 1)
        return

    def has_parent(self, i):
        return self.get_parent_index(i) >= 0

    def parent(self, i):
        return self.arr[self.get_parent_index(i)]

    def get_parent_index(self, i):
        return (i - 1) // 2

    def has_left_child(self, i):
        return self.get_left_child_index(i) < len(self.arr)

    def has_right_child(self, i):
        return self.get_right_child_index(i) < len(self.arr)

    def right_child(self, i):
        return self.arr[self.get_right_child_index(i)]

    def left_child(self, i):
        return self.arr[self.get_left_child_index(i)]

    def get_left_child_index(self, i):
        return 2 * i + 1

    def get_right_child_index(self, i):
        return 2 * i + 2


class MyNode:
    def __init__(self, cost, heu, cla, sol):
        self.cost = cost
        self.heu = heu
        self.cla = cla
        self.sol = sol

    def get_cost_plus_heu(self):
        return self.cost + self.heu
