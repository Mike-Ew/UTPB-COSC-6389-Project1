import math
import random
import tkinter as tk
from tkinter import *

num_nodes = 50
num_edges = 100
node_scale = 15  # Increased to 15
edge_width = 2
padding = 100


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = None
        self.neighbors = []

    def draw(self, canvas):
        color = self.color if self.color else "black"
        canvas.create_oval(
            self.x - node_scale,
            self.y - node_scale,
            self.x + node_scale,
            self.y + node_scale,
            fill=color,
        )


class Edge:
    def __init__(self, a, b):
        self.node_a = a
        self.node_b = b
        self.length = math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

    def draw(self, canvas, color="grey", style=(2, 4)):
        canvas.create_line(
            self.node_a.x,
            self.node_a.y,
            self.node_b.x,
            self.node_b.y,
            fill=color,
            width=edge_width,
            dash=style,
        )


class UI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Graph Coloring")
        self.option_add("*tearOff", FALSE)
        width, height = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (width, height))
        self.state("zoomed")

        self.canvas = Canvas(self)
        self.canvas.place(x=0, y=0, width=width, height=height)
        w = width - padding
        h = height - padding * 2

        self.nodes_list = []
        self.edges_list = []
        self.edges_set = set()

        def add_node():
            x = random.randint(padding, w)
            y = random.randint(padding, h)
            node = Node(x, y)
            self.nodes_list.append(node)

        def add_edge():
            a = random.randint(0, len(self.nodes_list) - 1)
            b = random.randint(0, len(self.nodes_list) - 1)
            edge_key = (min(a, b), max(a, b))
            while a == b or edge_key in self.edges_set:
                a = random.randint(0, len(self.nodes_list) - 1)
                b = random.randint(0, len(self.nodes_list) - 1)
                edge_key = (min(a, b), max(a, b))

            edge = Edge(self.nodes_list[a], self.nodes_list[b])
            self.edges_set.add(edge_key)
            self.edges_list.append(edge)

            # Update neighbors
            self.nodes_list[a].neighbors.append(self.nodes_list[b])
            self.nodes_list[b].neighbors.append(self.nodes_list[a])

        def generate_graph():
            self.nodes_list.clear()
            self.edges_list.clear()
            self.edges_set.clear()
            for _ in range(num_nodes):
                add_node()
            for _ in range(num_edges):
                add_edge()
            draw_graph()

        def draw_graph():
            clear_canvas()
            for e in self.edges_list:
                e.draw(self.canvas)
            for n in self.nodes_list:
                n.draw(self.canvas)

        def clear_canvas():
            self.canvas.delete("all")

        def color_graph():
            colors = [
                "red",
                "green",
                "blue",
                "yellow",
                "cyan",
                "magenta",
                "orange",
                "purple",
                "pink",
                "brown",
                "gray",
                "olive",
                "maroon",
            ]
            for node in self.nodes_list:
                used_colors = set(
                    neighbor.color for neighbor in node.neighbors if neighbor.color
                )
                for color in colors:
                    if color not in used_colors:
                        node.color = color
                        break
                else:
                    node.color = "black"  # Default color if no other color is available

        def solve():
            color_graph()
            draw_graph()

        # Create menu
        menu_bar = Menu(self)
        self["menu"] = menu_bar

        menu_gc = Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_gc, label="Graph Coloring", underline=0)
        menu_gc.add_command(label="Generate", command=generate_graph, underline=0)
        menu_gc.add_command(label="Solve", command=solve, underline=0)

        self.mainloop()


if __name__ == "__main__":
    UI()
