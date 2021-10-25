import tkinter as tk
import random, time, asyncio


# Size of window and canvas dimensions
GEOMETRY = "1000x700"
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600

# Set data amounts for different buttons
SMALL_DATA = 20
MEDIUM_DATA = 50
LARGE_DATA = 100

# Amount of bars that represent data
data_amount = MEDIUM_DATA
data = []
states = [] # Used for coloring bars in Quick-Sort

# Set the amount of data points
def set_data_amount(amount):
    global data_amount
    data_amount = amount
    generate_data()


# Representation of the data through rectangle with height of the data value
def generate_data():
    global data, states
    data = [random.randrange(0, 600) for _ in range(data_amount)]
    states = [-1 for _ in range(data_amount)]
    canvas.delete("all")
    for i in range(data_amount):
        canvas.create_rectangle(i*CANVAS_WIDTH//data_amount, 0, (i+1)*CANVAS_WIDTH//data_amount, data[i], outline="white", fill="blue", width=1)


# Configure window
root = tk.Tk()
root.title("Sorting Algorithms Visualization")
root.geometry(GEOMETRY)
root.resizable(False, False)
root.configure(bg="#606662")

# Configure canvas
canvas = tk.Canvas(root, bg="white", width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
canvas.pack()

# Generate data that gets initially displayed
generate_data()

# Configure buttons
btn_data_amount = tk.Button(root, text="Small Data Amount", command=lambda: set_data_amount(SMALL_DATA))
btn_data_amount.pack(side=tk.LEFT, padx=5)
btn_data_amount = tk.Button(root, text="Medium Data Amount", command=lambda: set_data_amount(MEDIUM_DATA))
btn_data_amount.pack(side=tk.LEFT, padx=5)
btn_data_amount = tk.Button(root, text="Large Data Amount", command=lambda: set_data_amount(LARGE_DATA))
btn_data_amount.pack(side=tk.LEFT, padx=5)

btn_randomize = tk.Button(root, text = "New Data", command=generate_data)
btn_randomize.pack(side=tk.LEFT, padx=50)

# Drop Down Menu for algorithm choice
algorithm_options = ["Bubble-Sort", "Merge-Sort", "Quick-Sort"]
options = tk.StringVar(value=algorithm_options[0])
dropdown_algorithm = tk.OptionMenu(root, options, *algorithm_options)
dropdown_algorithm.pack(side=tk.LEFT, padx=20)

def refresh(compare, unicolor=False):
    canvas.delete("all")
    i = 0
    while i < data_amount:
        if compare is not None and i == compare and not unicolor:
            canvas.create_rectangle(i*CANVAS_WIDTH//data_amount, 0, (i+1)*CANVAS_WIDTH//data_amount, data[i], outline="white", fill="yellow", width=1)
            canvas.create_rectangle((i+1)*CANVAS_WIDTH//data_amount, 0, (i+2)*CANVAS_WIDTH//data_amount, data[i+1], outline="white", fill="yellow", width=1)
            i += 1
        else:
            canvas.create_rectangle(i*CANVAS_WIDTH//data_amount, 0, (i+1)*CANVAS_WIDTH//data_amount, data[i], outline="white", fill="blue", width=1)
        i += 1
    canvas.update()

def display_data(arr, color_list):
    canvas.delete("all")
    for i in range(data_amount):
        canvas.create_rectangle(i*CANVAS_WIDTH//data_amount, 0, (i+1)*CANVAS_WIDTH//data_amount, arr[i], outline="white", fill=color_list[i], width=1)
    canvas.update()

# Sorting algorithms:
# Bubble Sort:
def bubble_sort():
    global data
    n = len(data)
    for i in range(n-1):
        got_swapped = False
        for j in range(n-i-1):
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]
                got_swapped = True
                refresh(j)
                time.sleep(0.1)
        if not got_swapped:
            break
    refresh(j, unicolor=True)

# Mergesort:
def merge_sort(arr, start, end):
    if start < end:
        mid = (start + end) // 2
        merge_sort(arr, start, mid)
        merge_sort(arr, mid + 1, end)
        merge(arr, start, mid, end)
        display_data(arr, ["yellow" if x >= start and x < mid else "red" if x == mid else "orange" if x > mid and x <=end else "blue" for x in range(len(arr))])
        time.sleep(0.1)
    display_data(arr, ["blue" for x in range(len(arr))])

def merge(arr, start, mid, end):
    # Build a temporary array to avoid modifying the original contents
    temp = [-1 for z in range(end + 1)]
    i = start
    j = mid + 1
    k = 0
    # Merge subarrays in sorted order as long as both still have values
    while i <= mid and j <= end:
        if arr[i] <= arr[j]:
            temp[k] = arr[i]
            k += 1
            i += 1
        else:
            temp[k] = arr[j]
            k += 1
            j += 1
    # Copy over values when only values in the left subarray are left
    while i <= mid:
        temp[k] = arr[i]
        k += 1
        i += 1
    # Copy over values when only values in the right subarray are left
    while j <= end:
        temp[k] = arr[j]
        k += 1
        j += 1
    # Copy sorted values into original array
    for i in range(start, end + 1):
        arr[i] = temp[i - start]


# Quicksort:
async def quick_sort(arr, start, end):
    if start >= end:
        return
    index = await partition(arr, start, end)
    states[index] = -1
    await asyncio.gather(
        quick_sort(arr, start, index - 1),
        quick_sort(arr, index + 1, end)
    )


async def partition(arr, start, end):
    for i in range(start, end):
        states[i] = 1
    pivot_index = start
    pivot_value = arr[end]
    states[pivot_index] = 0
    for i in range(start, end):
        if arr[i] < pivot_value:
            arr[i], arr[pivot_index] = arr[pivot_index], arr[i]
            states[pivot_index] = -1
            pivot_index += 1
            states[pivot_index] = 0
            display_data(arr, ["yellow" if states[x] == 0 else "purple" if states[x] == 1 else "blue" for x in range(len(arr))])
            await asyncio.sleep(0.1)
    arr[pivot_index], arr[end] = arr[end], arr[pivot_index]
    for i in range(start, end):
        if i != pivot_index:
            states[i] = -1
    display_data(arr, ["blue" for _ in range(len(arr))])
    return pivot_index


# Get choice of sorting algorithm and execute on call
def sorting_algorithms(data):
    if options.get() == "Bubble-Sort":
        bubble_sort()
    elif options.get() == "Merge-Sort":
        merge_sort(data, 0, len(data) - 1)
    elif options.get() == "Quick-Sort":
        asyncio.run(quick_sort(data, 0, len(data) - 1))

# Run algorithm button
btn_run = tk.Button(root, text="Run Selected Algorithm", command=lambda: sorting_algorithms(data))
btn_run.pack(side=tk.LEFT, padx=20)

root.mainloop()
