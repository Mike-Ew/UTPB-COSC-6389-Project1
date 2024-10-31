import math
import random
import tkinter as tk
from tkinter import *

num_cities = 50
city_scale = 5
padding = 100

# Parameters for ACO
alpha = 1.0  # Influence of pheromone
beta = 5.0  # Influence of heuristic value (visibility)
evaporation = 0.5  # Pheromone evaporation rate
ant_count = 20  # Number of ants
max_iterations = 100  # Maximum number of iterations for ACO
stagnation_limit = (
    20  # Number of iterations with no improvement to consider convergence
)

# Parameters for GA
population_size = 100
mutation_rate = 0.02
crossover_rate = 0.8
ga_iterations = 5000


class Node:
    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.index = index  # Unique identifier for the city

    def draw(self, canvas, color="black"):
        canvas.create_oval(
            self.x - city_scale,
            self.y - city_scale,
            self.x + city_scale,
            self.y + city_scale,
            fill=color,
            tags="cities",
        )


class Edge:
    def __init__(self, a, b):
        self.city_a = a
        self.city_b = b
        self.length = math.hypot(a.x - b.x, a.y - b.y)

    def draw(self, canvas, color="black", dash=(2, 4)):
        canvas.create_line(
            self.city_a.x,
            self.city_a.y,
            self.city_b.x,
            self.city_b.y,
            fill=color,
            width=1,
            dash=dash,
            tags="edges",
        )


class UI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Traveling Salesman")
        self.option_add("*tearOff", FALSE)
        width, height = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (width, height))
        self.state("zoomed")

        self.canvas = Canvas(self)
        self.canvas.place(x=0, y=0, width=width, height=height)
        w = width - padding
        h = height - padding * 2

        self.cities_list = []
        self.edges_list = []
        self.tour = []
        self.best_distance = None
        self.iteration = 0
        self.stagnant_iterations = 0  # For convergence check
        self.optimizing = False  # Flag to control optimization loop
        self.algorithm = "2-opt"  # Default algorithm
        self.pheromone = {}  # Pheromone levels for ACO
        self.population = []  # Population for GA
        self.status_label = tk.Label(self, text="Distance: 0.00")
        self.status_label.place(x=10, y=10)

        # Algorithm selection
        self.algorithm_var = tk.StringVar(value="2-opt")
        self.radio_2opt = tk.Radiobutton(
            self, text="2-opt", variable=self.algorithm_var, value="2-opt"
        )
        self.radio_aco = tk.Radiobutton(
            self, text="ACO", variable=self.algorithm_var, value="ACO"
        )
        self.radio_ga = tk.Radiobutton(
            self, text="GA", variable=self.algorithm_var, value="GA"
        )
        self.radio_2opt.place(x=10, y=40)
        self.radio_aco.place(x=70, y=40)
        self.radio_ga.place(x=130, y=40)

        # Solve button
        self.solve_button = tk.Button(
            self, text="Solve", command=self.start_optimization
        )
        self.solve_button.place(x=200, y=38)

        def generate_cities():
            self.cities_list.clear()
            self.edges_list.clear()
            self.tour.clear()
            self.best_distance = None
            self.iteration = 0
            self.stagnant_iterations = 0
            self.optimizing = False
            self.algorithm = self.algorithm_var.get()
            self.pheromone.clear()
            self.population.clear()
            # Generate cities
            for idx in range(num_cities):
                x = random.randint(padding, w)
                y = random.randint(padding, h)
                node = Node(x, y, idx)
                self.cities_list.append(node)
            # Generate all possible edges
            N = len(self.cities_list)
            for i in range(N):
                for j in range(i + 1, N):
                    edge = Edge(self.cities_list[i], self.cities_list[j])
                    self.edges_list.append(edge)
            draw_cities()
            # Do not initialize the tour or draw it here

        def draw_cities():
            self.canvas.delete("all")
            # Draw all edges as dotted black lines
            for edge in self.edges_list:
                edge.draw(self.canvas, color="black", dash=(2, 4))
            # Draw cities
            for n in self.cities_list:
                n.draw(self.canvas)
            # Do not draw the tour here

        # Menu s