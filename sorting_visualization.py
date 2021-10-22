import tkinter as tk
import random

# Amount of bars that represent data
data_amount = 20

# Size of window and canvas dimensions
GEOMETRY = "1000x700"
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600

# Set data amounts for different buttons
SMALL_DATA = 10
MEDIUM_DATA = 20
LARGE_DATA = 100

# Set the amount of data points
def set_data_amount(amount):
    global data_amount
    data_amount = amount
    generate_data()


# Representation of the data through rectangle with height of the data value
def generate_data():
    data = [random.randrange(0, 600) for _ in range(data_amount)]
    canvas.delete("all")
    for i in range(data_amount):
        canvas.create_rectangle(i*CANVAS_WIDTH//data_amount, 0, (i+1)*CANVAS_WIDTH//data_amount, data[i], outline="red", fill="blue", width=1)


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
dropdown_algorithm = tk.OptionMenu(root, tk.StringVar(value=algorithm_options[0]), *algorithm_options)
dropdown_algorithm.pack(side=tk.LEFT, padx=20)

# Run algorithm button
btn_run = tk.Button(root, text="Run Selected Algorithm")
btn_run.pack(side=tk.LEFT, padx=20)

root.mainloop()
