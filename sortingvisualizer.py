import tkinter as tk
import random
import time
import matplotlib.pyplot as plt



def bubble_sort(arr):
    a = arr
    n = len(a)
    for i in range(n):
        for j in range(n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
            yield a, j, j + 1


def insertion_sort(arr):
    a = arr
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
            yield a, j, j + 1
        a[j + 1] = key
        yield a, j, j + 1


def selection_sort(arr):
    a = arr
    n = len(a)
    for i in range(n):
        min_i = i
        for j in range(i + 1, n):
            if a[j] < a[min_i]:
                min_i = j
            yield a, min_i, j

        a[i], a[min_i] = a[min_i], a[i]
        yield a, i, min_i


def merge_sort(arr):
    a = arr

    def merge(start, mid, end):
        left = a[start:mid]
        right = a[mid:end]
        i = j = 0
        k = start

        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                a[k] = left[i]
                i += 1
            else:
                a[k] = right[j]
                j += 1
            k += 1
            yield a, k - 1, mid

        while i < len(left):
            a[k] = left[i]
            i += 1
            k += 1
            yield a, k - 1, mid

        while j < len(right):
            a[k] = right[j]
            j += 1
            k += 1
            yield a, k - 1, mid

    def divide(start, end):
        if end - start > 1:
            mid = (start + end) // 2
            yield from divide(start, mid)
            yield from divide(mid, end)
            yield from merge(start, mid, end)

    yield from divide(0, len(a))


def quick_sort(arr):
    a = arr

    def partition(low, high):

        pivot = a[high]
        i = low

        for j in range(low, high):
            if a[j] < pivot:
                a[i], a[j] = a[j], a[i]
                i += 1
            yield a, i, j

        a[i], a[high] = a[high], a[i]
        yield a, i, high
        return i

    def qs(low, high):
        if low < high:
            p = yield from partition(low, high)
            yield from qs(low, p - 1)
            yield from qs(p + 1, high)

    yield from qs(0, len(a) - 1)


ALGORITHMS = {
    "Bubble Sort": bubble_sort,
    "Insertion Sort": insertion_sort,
    "Selection Sort": selection_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
}



class SortingVisualizer:

    def __init__(self, root):

        self.root = root
        root.title("Sorting Visualizer + Multi-Line Graph")

        top = tk.Frame(root)
        top.pack()

        tk.Label(top, text="Algorithm: ").pack(side="left")

        self.alg_choice = tk.StringVar(value="Bubble Sort")
        tk.OptionMenu(top, self.alg_choice, *ALGORITHMS.keys()).pack(side="left")

        tk.Button(top, text="Shuffle", command=self.shuffle).pack(side="left", padx=5)
        tk.Button(top, text="Start", command=self.start_sort).pack(side="left", padx=5)
        tk.Button(top, text="Show Graphs", command=self.plot_graphs).pack(side="left", padx=5)

        self.canvas = tk.Canvas(root, width=900, height=400, bg="white")
        self.canvas.pack(pady=10)

        self.data = []
        self.shuffle()

    def shuffle(self):
        self.data = [random.randint(10, 400) for _ in range(60)]
        self.draw(self.data, -1, -1)

    def draw(self, data, i1, i2):
        self.canvas.delete("all")
        width = 900
        height = 400
        bar_w = width / len(data)

        for i, v in enumerate(data):
            x0 = i * bar_w
            y0 = height - v
            x1 = (i + 1) * bar_w
            y1 = height

            color = "red" if i == i1 or i == i2 else "skyblue"
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

        self.root.update_idletasks()
    def start_sort(self):
        arr = self.data.copy()
        algo_name = self.alg_choice.get()
        algo_fn = ALGORITHMS[algo_name]

        for step, i, j in algo_fn(arr):
            self.draw(step, i, j)
            time.sleep(0.005)

    def plot_graphs(self):
        sizes = [50, 100, 200, 300]
        results = {name: [] for name in ALGORITHMS}

        for n in sizes:
            base = [random.randint(1, 5000) for _ in range(n)]

            for algo_name, algo_fn in ALGORITHMS.items():
                arr = base.copy()
                start = time.time()

                for _ in algo_fn(arr):
                    pass

                end = time.time()
                results[algo_name].append((end - start) * 1000)  # ms

        plt.figure(figsize=(8, 5))
        for algo_name, times in results.items():
            plt.plot(sizes, times, marker='o', label=algo_name)

        plt.title("Sorting Algorithms Time Complexity (Line Graph)")
        plt.xlabel("Input Size")
        plt.ylabel("Time (ms)")
        plt.legend()
        plt.grid()
        plt.show()

        plt.figure(figsize=(8, 5))
        width = 0.15
        x = range(len(sizes))

        for i, (algo_name, times) in enumerate(results.items()):
            bar_x = [p + i * width for p in x]
            plt.bar(bar_x, times, width=width, label=algo_name)

        plt.xticks([p + width for p in x], sizes)
        plt.title("Sorting Algorithms Time Complexity (Bar Graph)")
        plt.xlabel("Input Size")
        plt.ylabel("Time (ms)")
        plt.legend()
        plt.show()


root = tk.Tk()
app = SortingVisualizer(root)
root.mainloop()
