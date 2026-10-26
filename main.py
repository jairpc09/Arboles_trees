
import tkinter as tk
from tkinter import ttk, messagebox


class ContactNode:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
        self.key = name.casefold()
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, name, phone):
        if self.root is None:
            self.root = ContactNode(name, phone)
            return True

        current = self.root
        key = name.casefold()

        while True:
            if key == current.key:
                return False

            if key < current.key:
                if current.left is None:
                    current.left = ContactNode(name, phone)
                    return True
                current = current.left
            else:
                if current.right is None:
                    current.right = ContactNode(name, phone)
                    return True
                current = current.right

    def search(self, name):
        current = self.root
        key = name.casefold()

        while current is not None:
            if key == current.key:
                return current
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        return None

    def delete(self, name):
        self.root, deleted = self._delete_node(
            self.root, name.casefold()
        )
        return deleted

    def _delete_node(self, node, key):
        if node is None:
            return None, False

        if key < node.key:
            node.left, deleted = self._delete_node(node.left, key)
            return node, deleted

        if key > node.key:
            node.right, deleted = self._delete_node(node.right, key)
            return node, deleted

        if node.left is None:
            return node.right, True

        if node.right is None:
            return node.left, True

        successor = node.right
        while successor.left is not None:
            successor = successor.left

        node.name = successor.name
        node.phone = successor.phone
        node.key = successor.key

        node.right, _ = self._delete_node(
            node.right, successor.key
        )
        return node, True

    def inorder(self):
        contacts = []

        def traverse(node):
            if node is not None:
                traverse(node.left)
                contacts.append(node)
                traverse(node.right)

        traverse(self.root)
        return contacts

    def count(self):
        return len(self.inorder())


class ContactManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Contact Manager")
        self.root.geometry("1050x720")
        self.root.minsize(800, 600)
        self.root.configure(bg="#eaf6ff")
        self.root.option_add("*TEntry*background", "#f8fbff")
        self.root.option_add("*TEntry*foreground", "#1f2937")
        self.root.option_add("*TEntry*insertBackground", "#1f2937")

        self.tree = BinarySearchTree()
        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Title.TLabel", font=("Arial", 20, "bold"), foreground="#3a485f", background="#edf7ff")
        style.configure("Section.TLabel", font=("Arial", 12, "bold"), foreground="#3a485f", background="#edf7ff")
        style.configure("Panel.TFrame", background="#f5fbff")
        style.configure("Form.TLabelframe", background="#f5fbff", bordercolor="#b7d7ff")
        style.configure("Form.TLabelframe.Label", foreground="#3a485f", font=("Arial", 10, "bold"), background="#f5fbff")
        style.configure("Primary.TButton", font=("Arial", 10, "bold"), background="#9ecaff", foreground="#17324d")
        style.configure("Secondary.TButton", font=("Arial", 10), background="#dfefff", foreground="#17324d")
        style.map("Primary.TButton", background=[("active", "#7bb8ff")])
        style.map("Secondary.TButton", background=[("active", "#cfe8ff")])
        style.configure("Treeview", rowheight=28, background="#f9fcff", fieldbackground="#f9fcff", foreground="#2d3748")
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#d5ebff", foreground="#2d3748")
        style.map("Treeview.Heading", background=[("active", "#c5e1ff")])
        style.configure("Header.TFrame", background="#edf7ff", borderwidth=1, relief="solid")

        header = ttk.Frame(self.root, padding=15, style="Header.TFrame")
        header.pack(fill="x", padx=12, pady=(12, 0))

        ttk.Label(
            header,
            text="Smart Contact Manager",
            style="Title.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            header,
            text="Binary Search Tree Contact Management",
            foreground="#5d7288"
        ).pack(anchor="w", pady=(4, 0))

        form = ttk.LabelFrame(
            self.root, text="Contact Information", padding=12, style="Form.TLabelframe"
        )
        form.pack(fill="x", padx=15, pady=10)

        ttk.Label(form, text="Contact Name:", foreground="#4a4057").grid(
            row=0, column=0, sticky="w", padx=5, pady=6
        )
        self.name_entry = ttk.Entry(form, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=6)
        self.name_entry.configure(style="TEntry")

        ttk.Label(form, text="Phone Number:", foreground="#4a4057").grid(
            row=0, column=2, sticky="w", padx=5, pady=6
        )
        self.phone_entry = ttk.Entry(form, width=25)
        self.phone_entry.grid(row=0, column=3, padx=5, pady=6)
        self.phone_entry.configure(style="TEntry")

        buttons = ttk.Frame(form, style="Panel.TFrame")
        buttons.grid(
            row=1, column=0, columnspan=4,
            sticky="w", padx=5, pady=8
        )

        ttk.Button(
            buttons, text="Add Contact", style="Primary.TButton", command=self.add_contact
        ).pack(side="left", padx=(0, 6))

        ttk.Button(
            buttons, text="Search Contact", style="Secondary.TButton", command=self.search_contact
        ).pack(side="left", padx=6)

        ttk.Button(
            buttons, text="Delete Contact", style="Secondary.TButton", command=self.delete_contact
        ).pack(side="left", padx=6)

        ttk.Button(
            buttons, text="Clear Fields", style="Secondary.TButton", command=self.clear_fields
        ).pack(side="left", padx=6)

        content = ttk.Frame(self.root, padding=(15, 8), style="Panel.TFrame")
        content.pack(fill="both", expand=True)

        left = ttk.Frame(content, style="Panel.TFrame")
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))

        ttk.Label(
            left, text="Contact Tree", style="Section.TLabel"
        ).pack(anchor="w", pady=(0, 5))

        self.canvas = tk.Canvas(
            left, background="#f8fcff",
            highlightthickness=1, highlightbackground="#b9d7ff",
            bd=0
        )
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<Configure>", lambda event: self.draw_tree())

        right = ttk.Frame(content, width=300, style="Panel.TFrame")
        right.pack(side="right", fill="y", padx=(8, 0))

        ttk.Label(
            right, text="Contact List", style="Section.TLabel"
        ).pack(anchor="w", pady=(0, 5))

        self.contact_list = ttk.Treeview(
            right,
            columns=("name", "phone"),
            show="headings",
            height=16,
            style="Treeview"
        )
        self.contact_list.heading("name", text="Name")
        self.contact_list.heading("phone", text="Phone")
        self.contact_list.column("name", width=115)
        self.contact_list.column("phone", width=125)
        self.contact_list.pack(fill="both", expand=True)

        self.contact_list.bind(
            "<<TreeviewSelect>>", self.select_contact
        )

        self.status = ttk.Label(
            self.root, text="Ready | Total contacts: 0",
            relief="flat", anchor="w", padding=8, foreground="#3a3f58", background="#d7ebff"
        )
        self.status.pack(fill="x", side="bottom", padx=15, pady=(0, 10))

    def add_contact(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()

        if not name or not phone:
            messagebox.showwarning(
                "Missing Information",
                "Please enter both the contact name and phone number."
            )
            return

        if not phone.isdigit():
            messagebox.showwarning(
                "Invalid Phone Number",
                "The phone number must contain digits only."
            )
            return

        if self.tree.insert(name, phone):
            self.refresh()
            self.status.config(text=f"Contact added: {name}")
            self.clear_fields()
        else:
            messagebox.showwarning(
                "Duplicate Contact",
                "A contact with this name already exists."
            )

    def search_contact(self):
        name = self.name_entry.get().strip()

        if not name:
            messagebox.showwarning(
                "Missing Information",
                "Enter a contact name to search."
            )
            return

        contact = self.tree.search(name)

        if contact:
            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, contact.phone)
            self.status.config(
                text=f"Contact found: {contact.name}"
            )
            messagebox.showinfo(
                "Contact Found",
                f"Name: {contact.name}\nPhone: {contact.phone}"
            )
        else:
            self.status.config(text=f"Contact not found: {name}")
            messagebox.showinfo(
                "Search Result", "Contact not found."
            )

    def delete_contact(self):
        name = self.name_entry.get().strip()

        if not name:
            messagebox.showwarning(
                "Missing Information",
                "Enter a contact name to delete."
            )
            return

        if self.tree.delete(name):
            self.refresh()
            self.clear_fields()
            self.status.config(text=f"Contact deleted: {name}")
        else:
            messagebox.showinfo(
                "Delete Result", "Contact not found."
            )

    def select_contact(self, event):
        selected = self.contact_list.selection()

        if not selected:
            return

        values = self.contact_list.item(selected[0], "values")
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, values[0])
        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, values[1])

    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)

    def refresh(self):
        for item in self.contact_list.get_children():
            self.contact_list.delete(item)

        for contact in self.tree.inorder():
            self.contact_list.insert(
                "", "end", values=(contact.name, contact.phone)
            )

        self.draw_tree()
        self.status.config(
            text=f"Ready | Total contacts: {self.tree.count()}"
        )

    def draw_tree(self):
        self.canvas.delete("all")

        if self.tree.root is None:
            self.canvas.create_text(
                max(self.canvas.winfo_width() // 2, 100),
                max(self.canvas.winfo_height() // 2, 100),
                text="No contacts yet",
                fill="gray",
                font=("Arial", 14)
            )
            return

        width = self.canvas.winfo_width()
        self._draw_node(
            self.tree.root, width / 2, 45,
            max(width / 4, 35), 1
        )

    def _draw_node(self, node, x, y, offset, level):
        if node is None or level > 8:
            return

        child_y = y + 85

        if node.left is not None:
            child_x = x - offset
            self.canvas.create_line(
                x, y + 18, child_x, child_y - 18,
                fill="#7f8c8d", width=2
            )
            self._draw_node(
                node.left, child_x, child_y,
                max(offset / 2, 25), level + 1
            )

        if node.right is not None:
            child_x = x + offset
            self.canvas.create_line(
                x, y + 18, child_x, child_y - 18,
                fill="#7f8c8d", width=2
            )
            self._draw_node(
                node.right, child_x, child_y,
                max(offset / 2, 25), level + 1
            )

        self.canvas.create_oval(
            x - 50, y - 20, x + 50, y + 20,
            fill="#d5eaff", outline="#78afea", width=2
        )
        self.canvas.create_oval(
            x - 44, y - 14, x + 44, y + 14,
            fill="#c9e4ff", outline=""
        )
        self.canvas.create_text(
            x, y, text=node.name[:13],
            font=("Arial", 9, "bold"), fill="#1f2937"
        )


if __name__ == "__main__":
    window = tk.Tk()
    app = ContactManagerApp(window)
    window.mainloop()
