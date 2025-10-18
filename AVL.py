import tkinter as tk
import time

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def insert(self, root, key):
        if not root:
            return Node(key)
        elif key < root.key:
            root.left = self.insert(root.left, key)
        elif key > root.key:
            root.right = self.insert(root.right, key)
        else:
            return root

        left_height = self.getHeight(root.left)
        right_height = self.getHeight(root.right)
        root.height = 1 + max(left_height, right_height)

        balance = self.getBalance(root)

        # Rotations
        if balance > 1 and key < root.left.key:
            return self.rightRotate(root)
        if balance < -1 and key > root.right.key:
            return self.leftRotate(root)
        if balance > 1 and key > root.left.key:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)
        if balance < -1 and key < root.right.key:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def delete(self, root, key):
        if not root:
            return root
        elif key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            # Node to be deleted found
            if not root.left:
                temp = root.right
                root = None
                return temp
            elif not root.right:
                temp = root.left
                root = None
                return temp

            temp = self.getMinValueNode(root.right)
            root.key = temp.key
            root.right = self.delete(root.right, temp.key)

        if not root:
            return root

        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))
        balance = self.getBalance(root)

        # Rebalancing
        if balance > 1 and self.getBalance(root.left) >= 0:
            return self.rightRotate(root)
        if balance > 1 and self.getBalance(root.left) < 0:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)
        if balance < -1 and self.getBalance(root.right) <= 0:
            return self.leftRotate(root)
        if balance < -1 and self.getBalance(root.right) > 0:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def leftRotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        return y

    def rightRotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3

        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        return y

    def getHeight(self, root):
        if not root:
            return 0
        return root.height

    def getBalance(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

    def getMinValueNode(self, root):
        if root is None or root.left is None:
            return root
        return self.getMinValueNode(root.left)

    def contains(self, root, key):
        """Return True if key exists in tree rooted at root."""
        if not root:
            return False
        if key == root.key:
            return True
        elif key < root.key:
            return self.contains(root.left, key)
        else:
            return self.contains(root.right, key)


class AnimatedAVLVisualizer:
    def __init__(self, avl_tree):
        self.window = tk.Tk()
        self.window.title("AVL Tree Visualization")
        self.window.geometry("950x650")
        self.window.configure(bg="#E3F2FD")

        # Title
        title_label = tk.Label(
            self.window,
            text="AVL Tree Visualizer",
            font=("Helvetica", 18, "bold"),
            fg="#0D47A1",
            bg="#E3F2FD"
        )
        title_label.pack(side="top", pady=(10, 5))

        # Control frame below title
        control_frame = tk.Frame(self.window, bg="#E3F2FD")
        control_frame.pack(side="top", pady=(5, 10))

        tk.Label(control_frame, text="Enter number:", bg="#E3F2FD", font=("Arial", 11, "bold")).pack(side="left", padx=5)
        self.entry = tk.Entry(control_frame, width=10, font=("Consolas", 11))
        self.entry.pack(side="left", padx=5)

        btn_style = {"bg": "#1976D2", "fg": "white", "font": ("Arial", 10, "bold"), "width": 8, "relief": "raised"}
        tk.Button(control_frame, text="Insert", command=self.insert_node, **btn_style).pack(side="left", padx=5)
        tk.Button(control_frame, text="Delete", command=self.delete_node, **btn_style).pack(side="left", padx=5)
        tk.Button(control_frame, text="Clear", command=self.clear_tree, **btn_style).pack(side="left", padx=5)

        # Canvas
        self.canvas = tk.Canvas(self.window, width=900, height=520, bg="#8AD9E8")
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)

        # backend
        self.avl = avl_tree
        self.root_node = None
        self.positions = {}

    def insert_node(self):
        val = self.entry.get().strip()
        if val.lstrip("-").isdigit():
            key = int(val)
            self.root_node = self.avl.insert(self.root_node, key)
            self.animate_redraw()
            self.entry.delete(0, tk.END)
        else:
            self.flash_message("Please enter a valid integer")

    def delete_node(self):
        val = self.entry.get().strip()
        if not val.lstrip("-").isdigit():
            self.flash_message("Please enter a valid integer")
            return

        key = int(val)

        # Check existence first
        if not self.avl.contains(self.root_node, key):
            self.flash_message(f"Key {key} not found")
            self.entry.delete(0, tk.END)
            return

        # Perform delete and redraw (we know key existed)
        self.root_node = self.avl.delete(self.root_node, key)
        self.animate_redraw()
        self.entry.delete(0, tk.END)

    def clear_tree(self):
        self.root_node = None
        self.positions = {}
        self.canvas.delete("all")

    def flash_message(self, text, duration=900):
        popup = tk.Toplevel(self.window)
        popup.title("Message")
        popup.geometry("220x90")
        tk.Label(popup, text=text, padx=10, pady=6).pack(expand=True)
        popup.after(duration, popup.destroy)

    def _compute_positions(self, node, x, y, offset, pos_dict):
        if node:
            pos_dict[node.key] = (x, y)
            self._compute_positions(node.left, x - offset, y + 100, max(20, offset // 2), pos_dict)
            self._compute_positions(node.right, x + offset, y + 100, max(20, offset // 2), pos_dict)

    def _draw_node_at(self, key, x, y):
        radius = 22
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                fill="#90CAF9", outline="#333", width=2)
        self.canvas.create_text(x, y, text=str(key), font=("Arial", 12, "bold"))

    def _draw_edges_with_positions(self, node, pos_dict):
        if not node:
            return
        if node.left and node.left.key in pos_dict and node.key in pos_dict:
            x1, y1 = pos_dict[node.key]
            x2, y2 = pos_dict[node.left.key]
            self.canvas.create_line(x1, y1 + 18, x2, y2 - 18, width=2, fill="#555")
        if node.right and node.right.key in pos_dict and node.key in pos_dict:
            x1, y1 = pos_dict[node.key]
            x2, y2 = pos_dict[node.right.key]
            self.canvas.create_line(x1, y1 + 18, x2, y2 - 18, width=2, fill="#555")
        self._draw_edges_with_positions(node.left, pos_dict)
        self._draw_edges_with_positions(node.right, pos_dict)

    def animate_redraw(self):
        new_positions = {}
        if self.root_node:
            self._compute_positions(self.root_node, 450, 60, 220, new_positions)

        animation_steps = 18
        for step in range(animation_steps):
            current_positions = {}
            progress = (step + 1) / animation_steps
            for key, (x_new, y_new) in new_positions.items():
                if key in self.positions:
                    x_old, y_old = self.positions[key]
                    x = x_old + (x_new - x_old) * progress
                    y = y_old + (y_new - y_old) * progress
                else:
                    x = x_new
                    start_y = y_new - 80
                    y = start_y + (y_new - start_y) * progress
                current_positions[key] = (int(x), int(y))

            self.canvas.delete("all")
            self._draw_edges_with_positions(self.root_node, current_positions)
            for key, (x, y) in current_positions.items():
                self._draw_node_at(key, x, y)

            self.window.update()
            time.sleep(0.02)

        self.positions = {k: (int(x), int(y)) for k, (x, y) in new_positions.items()}

    def run(self):
        self.entry.bind('<Return>', lambda e: self.insert_node())
        self.window.mainloop()


if __name__ == "__main__":
    tree = AVLTree()
    app = AnimatedAVLVisualizer(tree)
    app.run()
