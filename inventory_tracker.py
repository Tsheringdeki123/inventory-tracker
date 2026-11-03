import csv
from datetime import datetime
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

matplotlib.use("TkAgg")


# =============================================================================
# 1. AUTHENTICATION & LOGIN WINDOW
# =============================================================================
class LoginWindow:

    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.root.title("System Login - Inventory Management")
        self.root.geometry("420x480")
        self.root.resizable(False, False)
        self.root.configure(bg="#0f172a")

        self.db_name = "inventory.db"
        self.init_user_db()

        self.create_widgets()

    def init_user_db(self):
        """Initializes users table and inserts default credentials if empty."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """)

        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                ("admin", "admin123", "admin"),
            )
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                ("user", "user123", "user"),
            )
            conn.commit()
        conn.close()

    def create_widgets(self):
        card = tk.Frame(
            self.root, bg="#1e293b", padx=30, pady=30, highlightthickness=0
        )
        card.place(relx=0.5, rely=0.5, anchor="center", width=360, height=410)

        lbl_logo = tk.Label(
            card, text="📦", font=("Segoe UI", 32), bg="#1e293b", fg="#2563eb"
        )
        lbl_logo.pack(pady=(0, 5))

        lbl_title = tk.Label(
            card,
            text="Welcome Back",
            font=("Segoe UI", 16, "bold"),
            bg="#1e293b",
            fg="#ffffff",
        )
        lbl_title.pack()

        lbl_sub = tk.Label(
            card,
            text="Sign in to continue",
            font=("Segoe UI", 9),
            bg="#1e293b",
            fg="#94a3b8",
        )
        lbl_sub.pack(pady=(0, 20))

        tk.Label(
            card,
            text="Username",
            font=("Segoe UI", 9, "bold"),
            bg="#1e293b",
            fg="#cbd5e1",
        ).pack(anchor="w")
        self.ent_user = tk.Entry(
            card,
            font=("Segoe UI", 10),
            bg="#334155",
            fg="#ffffff",
            insertbackground="white",
            bd=0,
            relief="flat",
        )
        self.ent_user.pack(fill=tk.X, ipady=6, pady=(2, 12))
        self.ent_user.insert(0, "admin")

        tk.Label(
            card,
            text="Password",
            font=("Segoe UI", 9, "bold"),
            bg="#1e293b",
            fg="#cbd5e1",
        ).pack(anchor="w")
        self.ent_pass = tk.Entry(
            card,
            font=("Segoe UI", 10),
            bg="#334155",
            fg="#ffffff",
            insertbackground="white",
            show="•",
            bd=0,
            relief="flat",
        )
        self.ent_pass.pack(fill=tk.X, ipady=6, pady=(2, 18))
        self.ent_pass.insert(0, "admin123")

        btn_login = tk.Button(
            card,
            text="Login",
            font=("Segoe UI", 10, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#0f172a",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=self.handle_login,
        )
        btn_login.pack(fill=tk.X, ipady=6)

        # Button Press Feedback
        btn_login.bind("<Enter>", lambda e: btn_login.config(bg="#1d4ed8"))
        btn_login.bind("<Leave>", lambda e: btn_login.config(bg="#2563eb"))
        btn_login.bind("<ButtonPress-1>", lambda e: btn_login.config(bg="#0f172a"))
        btn_login.bind("<ButtonRelease-1>", lambda e: btn_login.config(bg="#1d4ed8"))

        lbl_hint = tk.Label(
            card,
            text="Default Logins:\nAdmin: admin / admin123\nUser: user / user123",
            font=("Segoe UI", 8, "italic"),
            bg="#1e293b",
            fg="#64748b",
            justify="center",
        )
        lbl_hint.pack(pady=(15, 0))

    def handle_login(self):
        username = self.ent_user.get().strip()
        password = self.ent_pass.get().strip()

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT role FROM users WHERE username=? AND password=?",
            (username, password),
        )
        result = cursor.fetchone()
        conn.close()

        if result:
            role = result[0]
            messagebox.showinfo(
                "Login Success",
                f"Welcome {username}! Logged in as [{role.upper()}].",
            )
            self.on_login_success(username, role)
        else:
            messagebox.showerror(
                "Login Failed", "Invalid Username or Password. Please try again."
            )


# =============================================================================
# 2. PRODUCT DETAIL VIEW WINDOW
# =============================================================================
class ViewDetailWindow(tk.Toplevel):

    def __init__(self, parent, record):
        super().__init__(parent)
        self.title(f"Product Details - #{record[0]}")
        self.geometry("400x480")
        self.resizable(False, False)
        self.configure(bg="#ffffff")

        self.transient(parent)
        self.grab_set()

        header = tk.Frame(self, bg="#0f172a", height=50)
        header.pack(fill=tk.X)
        tk.Label(
            header,
            text="📄 Full Product Overview",
            font=("Segoe UI", 11, "bold"),
            fg="white",
            bg="#0f172a",
            padx=15,
            pady=12,
        ).pack(anchor="w")

        body = tk.Frame(self, bg="#ffffff", padx=20, pady=20)
        body.pack(fill=tk.BOTH, expand=True)

        details = [
            ("Product ID:", str(record[0])),
            ("Product Name:", str(record[1])),
            ("Category:", str(record[2])),
            ("Quantity in Stock:", f"{record[3]:,} units" if isinstance(record[3], int) else str(record[3])),
            ("Unit Price:", str(record[4])),
            ("Total Inventory Value:", str(record[5])),
            ("Date Recorded:", str(record[6])),
        ]

        for lbl_text, val_text in details:
            row_frame = tk.Frame(body, bg="#ffffff")
            row_frame.pack(fill=tk.X, pady=6)

            tk.Label(
                row_frame,
                text=lbl_text,
                font=("Segoe UI", 9, "bold"),
                bg="#ffffff",
                fg="#64748b",
                width=20,
                anchor="w",
            ).pack(side=tk.LEFT)
            tk.Label(
                row_frame,
                text=val_text,
                font=("Segoe UI", 9, "bold"),
                bg="#ffffff",
                fg="#0f172a",
                anchor="w",
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)

            ttk.Separator(body, orient="horizontal").pack(fill=tk.X, pady=2)

        btn_close = tk.Button(
            self,
            text="Close Window",
            font=("Segoe UI", 9, "bold"),
            bg="#64748b",
            fg="white",
            activebackground="#0f172a",
            activeforeground="white",
            bd=0,
            relief="flat",
            cursor="hand2",
            command=self.destroy,
        )
        btn_close.pack(fill=tk.X, padx=20, pady=(0, 20), ipady=5)
        btn_close.bind("<Enter>", lambda e: btn_close.config(bg="#475569"))
        btn_close.bind("<Leave>", lambda e: btn_close.config(bg="#64748b"))
        btn_close.bind("<ButtonPress-1>", lambda e: btn_close.config(bg="#0f172a"))
        btn_close.bind("<ButtonRelease-1>", lambda e: btn_close.config(bg="#475569"))


# =============================================================================
# 3. MAIN DASHBOARD APPLICATION
# =============================================================================
class ModernInventorySystem:

    def __init__(self, root, username, role, logout_callback):
        self.root = root
        self.username = username
        self.user_role = role
        self.logout_callback = logout_callback

        self.root.title(
            f"Inventory Management Dashboard - Logged in as: {self.username} ({self.user_role.upper()})"
        )
        self.root.geometry("1120x680")
        self.root.minsize(950, 560)
        self.root.configure(bg="#f8fafc")

        self.db_name = "inventory.db"
        self.init_database()

        self.selected_id = None
        self.sort_reverse = False

        self.setup_styles()
        self.create_widgets()
        self.load_data()

    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                date_added TEXT
            )
        """)

        try:
            cursor.execute("ALTER TABLE products ADD COLUMN date_added TEXT")
        except sqlite3.OperationalError:
            pass

        current_time = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
        cursor.execute(
            "UPDATE products SET date_added=? WHERE date_added IS NULL OR"
            " date_added='' OR date_added='N/A'",
            (current_time,),
        )

        conn.commit()
        conn.close()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.colors = {
            "header_bg": "#0f172a",
            "card_bg": "#ffffff",
            "primary": "#2563eb",
            "primary_hover": "#1d4ed8",
            "success": "#10b981",
            "success_hover": "#059669",
            "danger": "#ef4444",
            "danger_hover": "#dc2626",
            "secondary": "#64748b",
            "secondary_hover": "#475569",
            "warning": "#f59e0b",
            "warning_hover": "#d97706",
            "press_color": "#0f172a",  # Distinct dark press indicator
            "text_dark": "#1e293b",
            "text_light": "#64748b",
            "border": "#e2e8f0",
        }

        self.style.configure(
            "Treeview",
            font=("Segoe UI", 9),
            rowheight=26,
            background="#ffffff",
            fieldbackground="#ffffff",
            foreground=self.colors["text_dark"],
            borderwidth=0,
        )
        self.style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 9, "bold"),
            background="#e2e8f0",
            foreground=self.colors["text_dark"],
            relief="flat",
            padding=4,
        )
        self.style.map("Treeview.Heading", background=[("active", "#cbd5e1")])
        self.style.map(
            "Treeview",
            background=[("selected", "#2563eb")],
            foreground=[("selected", "#ffffff")],
        )

        self.style.configure(
            "TNotebook", background="#f8fafc", borderwidth=0, tabmargins=[10, 5, 0, 0]
        )
        self.style.configure(
            "TNotebook.Tab",
            font=("Segoe UI", 9, "bold"),
            padding=[14, 6],
            background="#e2e8f0",
            foreground="#475569",
        )
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", "#2563eb")],
            foreground=[("selected", "#ffffff")],
        )

    def create_widgets(self):
        header_frame = tk.Frame(self.root, bg=self.colors["header_bg"], height=48)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        title_label = tk.Label(
            header_frame,
            text="📦 Inventory Management Dashboard",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors["header_bg"],
            fg="white",
            padx=15,
            pady=8,
        )
        title_label.pack(side=tk.LEFT)

        user_badge_text = f"👤 {self.username} [{self.user_role.upper()}]"
        lbl_user = tk.Label(
            header_frame,
            text=user_badge_text,
            font=("Segoe UI", 9, "bold"),
            bg="#1e293b",
            fg="#38bdf8",
            padx=10,
            pady=4,
        )
        lbl_user.pack(side=tk.RIGHT, padx=(0, 10))

        btn_logout = self.create_styled_button(
            header_frame,
            "Logout",
            self.colors["danger"],
            self.colors["danger_hover"],
            self.logout_callback,
            px=10,
            py=2,
        )
        btn_logout.pack(side=tk.RIGHT, padx=10)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tab_inventory = tk.Frame(self.notebook, bg="#f8fafc")
        self.notebook.add(self.tab_inventory, text=" Standard Inventory View ")

        self.tab_analytics = tk.Frame(self.notebook, bg="#f8fafc")
        self.notebook.add(
            self.tab_analytics, text=" 📊 Analytics & Visualizations "
        )
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

        self.build_inventory_tab()
        self.build_analytics_tab()

    def build_inventory_tab(self):
        main_container = tk.Frame(self.tab_inventory, bg="#f8fafc", padx=10, pady=10)
        main_container.pack(fill=tk.BOTH, expand=True)

        content_frame = tk.Frame(main_container, bg="#f8fafc")
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 6))

        form_card = tk.Frame(
            content_frame,
            bg="white",
            highlightbackground=self.colors["border"],
            highlightthickness=1,
            padx=12,
            pady=10,
            width=280,
        )
        form_card.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))
        form_card.pack_propagate(False)

        form_title = tk.Label(
            form_card,
            text="Product Details",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg=self.colors["text_dark"],
        )
        form_title.pack(anchor="w", pady=(0, 4))

        inputs_frame = tk.Frame(form_card, bg="white")
        inputs_frame.pack(fill=tk.X)

        fields = [
            ("Product Name:", "ent_name", "entry"),
            ("Category:", "combo_category", "combo"),
            ("Price (Nu.):", "ent_price", "entry"),
            ("Quantity:", "ent_quantity", "entry"),
        ]

        for idx, (label_text, var_name, field_type) in enumerate(fields):
            lbl = tk.Label(
                inputs_frame,
                text=label_text,
                font=("Segoe UI", 8, "bold"),
                bg="white",
                fg=self.colors["text_light"],
            )
            lbl.grid(row=idx * 2, column=0, sticky="w", pady=(4, 1))

            if field_type == "entry":
                entry = tk.Entry(
                    inputs_frame,
                    font=("Segoe UI", 9),
                    bg="#f8fafc",
                    relief="solid",
                    bd=1,
                    highlightthickness=0,
                )
                entry.grid(row=idx * 2 + 1, column=0, sticky="ew", ipady=2)
                setattr(self, var_name, entry)
            elif field_type == "combo":
                combo = ttk.Combobox(
                    inputs_frame,
                    values=[
                        "Electronics",
                        "Hardware",
                        "Stationery",
                        "Groceries",
                        "Clothing",
                        "General",
                    ],
                    state="readonly",
                )
                combo.grid(row=idx * 2 + 1, column=0, sticky="ew", ipady=1)
                combo.current(0)
                setattr(self, var_name, combo)

        inputs_frame.columnconfigure(0, weight=1)

        is_admin = self.user_role == "admin"

        btn_frame = tk.Frame(form_card, bg="white")
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        btn_add = self.create_styled_button(
            btn_frame,
            "Add Product",
            self.colors["success"],
            self.colors["success_hover"],
            self.add_product,
            py=4,
        )
        btn_add.grid(row=0, column=0, padx=(0, 2), pady=2, sticky="ew")

        btn_update = self.create_styled_button(
            btn_frame,
            "Update",
            self.colors["primary"],
            self.colors["primary_hover"],
            self.update_product,
            py=4,
        )
        btn_update.grid(row=0, column=1, padx=(2, 0), pady=2, sticky="ew")

        btn_delete = self.create_styled_button(
            btn_frame,
            "Delete",
            self.colors["danger"],
            self.colors["danger_hover"],
            self.delete_product,
            py=4,
        )
        btn_delete.grid(row=1, column=0, padx=(0, 2), pady=2, sticky="ew")

        btn_clear = self.create_styled_button(
            btn_frame,
            "Clear Fields",
            self.colors["secondary"],
            self.colors["secondary_hover"],
            self.clear_fields,
            py=4,
        )
        btn_clear.grid(row=1, column=1, padx=(2, 0), pady=2, sticky="ew")

        if not is_admin:
            btn_add.config(state="disabled", bg="#cbd5e1", cursor="arrow")
            btn_update.config(state="disabled", bg="#cbd5e1", cursor="arrow")
            btn_delete.config(state="disabled", bg="#cbd5e1", cursor="arrow")
            tk.Label(
                form_card,
                text="🔒 Read-Only Access (User Role)",
                font=("Segoe UI", 8, "italic"),
                bg="white",
                fg=self.colors["danger"],
            ).pack(pady=(4, 0))

        btn_export = self.create_styled_button(
            btn_frame,
            "📥 Export to CSV",
            self.colors["warning"],
            self.colors["warning_hover"],
            self.export_to_csv,
            py=4,
        )
        btn_export.grid(row=2, column=0, columnspan=2, pady=(4, 0), sticky="ew")

        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

        display_card = tk.Frame(
            content_frame,
            bg="white",
            highlightbackground=self.colors["border"],
            highlightthickness=1,
            padx=10,
            pady=10,
        )
        display_card.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        search_frame = tk.Frame(display_card, bg="white")
        search_frame.pack(fill=tk.X, pady=(0, 8))

        search_lbl = tk.Label(
            search_frame,
            text="🔍 Search:",
            font=("Segoe UI", 9, "bold"),
            bg="white",
            fg=self.colors["text_dark"],
        )
        search_lbl.pack(side=tk.LEFT, padx=(0, 6))

        self.ent_search = tk.Entry(
            search_frame, font=("Segoe UI", 9), bg="#f8fafc", relief="solid", bd=1
        )
        self.ent_search.pack(
            side=tk.LEFT, fill=tk.X, expand=True, ipady=3, padx=(0, 6)
        )
        self.ent_search.bind("<KeyRelease>", self.search_products)

        btn_view_item = self.create_styled_button(
            search_frame,
            "👁️ View Details",
            self.colors["primary"],
            self.colors["primary_hover"],
            self.view_selected_product,
            px=8,
            py=3,
        )
        btn_view_item.pack(side=tk.LEFT, padx=(0, 4))

        btn_view_all = self.create_styled_button(
            search_frame,
            "📋 View All",
            self.colors["success"],
            self.colors["success_hover"],
            self.view_all_products,
            px=8,
            py=3,
        )
        btn_view_all.pack(side=tk.LEFT, padx=(0, 4))

        btn_reset = self.create_styled_button(
            search_frame,
            "Reset Table",
            self.colors["secondary"],
            self.colors["secondary_hover"],
            self.load_data,
            px=8,
            py=3,
        )
        btn_reset.pack(side=tk.RIGHT)

        table_frame = tk.Frame(display_card, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = (
            "ID",
            "Name",
            "Category",
            "Quantity",
            "Price",
            "Total Cost",
            "Date Recorded",
        )
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", selectmode="browse"
        )

        col_widths = {
            "ID": 35,
            "Name": 110,
            "Category": 90,
            "Quantity": 65,
            "Price": 80,
            "Total Cost": 95,
            "Date Recorded": 150,
        }
        for col in columns:
            self.tree.heading(
                col, text=col, command=lambda _col=col: self.sort_column(_col)
            )
            self.tree.column(col, width=col_widths[col], anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.tag_configure("evenrow", background="#ffffff")
        self.tree.tag_configure("oddrow", background="#f8fafc")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Double-1>", lambda e: self.view_selected_product())

        self.lbl_status = tk.Label(
            main_container,
            text="System Ready.",
            font=("Segoe UI", 8, "italic"),
            bg="#f8fafc",
            fg=self.colors["text_light"],
            anchor="w",
        )
        self.lbl_status.pack(fill=tk.X, side=tk.BOTTOM, pady=(2, 4))

        stats_frame = tk.Frame(main_container, bg="#f8fafc")
        stats_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.card_total_items = self.create_stat_card(
            stats_frame, "Total Products", "0", "#2563eb", 0
        )
        self.card_total_stock = self.create_stat_card(
            stats_frame, "Total Units in Stock", "0", "#10b981", 1
        )
        self.card_total_value = self.create_stat_card(
            stats_frame, "Total Inventory Value", "Nu. 0.00", "#f59e0b", 2
        )

    def build_analytics_tab(self):
        container = tk.Frame(self.tab_analytics, bg="#f8fafc", padx=15, pady=15)
        container.pack(fill=tk.BOTH, expand=True)

        top_bar = tk.Frame(container, bg="#f8fafc")
        top_bar.pack(fill=tk.X, pady=(0, 10))

        tk.Label(
            top_bar,
            text="📊 Inventory Analytics & Data Visualization",
            font=("Segoe UI", 12, "bold"),
            bg="#f8fafc",
            fg=self.colors["text_dark"],
        ).pack(side=tk.LEFT)

        btn_refresh_charts = self.create_styled_button(
            top_bar,
            "🔄 Refresh Visuals",
            self.colors["primary"],
            self.colors["primary_hover"],
            self.render_charts,
            px=10,
            py=4,
        )
        btn_refresh_charts.pack(side=tk.RIGHT)

        self.chart_frame = tk.Frame(container, bg="white")
        self.chart_frame.pack(fill=tk.BOTH, expand=True)

    def render_charts(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT category, SUM(quantity), SUM(quantity * price) FROM products"
            " GROUP BY category"
        )
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            tk.Label(
                self.chart_frame,
                text="No inventory data available to chart.",
                font=("Segoe UI", 11),
                bg="white",
                fg=self.colors["text_light"],
            ).pack(expand=True)
            return

        categories = [r[0] for r in rows]
        stock_levels = [r[1] if r[1] else 0 for r in rows]
        values = [r[2] if r[2] else 0.0 for r in rows]

        fig = Figure(figsize=(9, 4.5), dpi=100)
        fig.patch.set_facecolor("#ffffff")

        ax1 = fig.add_subplot(121)
        bars = ax1.bar(
            categories, stock_levels, color="#2563eb", edgecolor="#1d4ed8"
        )
        ax1.set_title(
            "Stock Units by Category", fontsize=10, fontweight="bold", pad=10
        )
        ax1.set_ylabel("Quantity (Units)", fontsize=8)
        ax1.tick_params(axis="x", rotation=25, labelsize=8)
        ax1.tick_params(axis="y", labelsize=8)
        ax1.grid(axis="y", linestyle="--", alpha=0.5)

        for bar in bars:
            yval = bar.get_height()
            ax1.text(
                bar.get_x() + bar.get_width() / 2.0,
                yval + 0.5,
                f"{int(yval)}",
                ha="center",
                va="bottom",
                fontsize=8,
            )

        ax2 = fig.add_subplot(122)
        if sum(values) > 0:
            ax2.pie(
                values,
                labels=categories,
                autopct="%1.1f%%",
                startangle=140,
                colors=["#10b981", "#f59e0b", "#3b82f6", "#ef4444", "#8b5cf6"],
                textprops={"fontsize": 8},
            )
            ax2.set_title(
                "Inventory Value Distribution",
                fontsize=10,
                fontweight="bold",
                pad=10,
            )
        else:
            ax2.text(
                0.5,
                0.5,
                "No Value Data",
                ha="center",
                va="center",
                transform=ax2.transAxes,
            )

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def on_tab_change(self, event):
        selected_tab = self.notebook.index(self.notebook.select())
        if selected_tab == 1:
            self.render_charts()

    # =========================================================================
    # 4. SEARCH & SELECTION CONTROLS
    # =========================================================================
    def search_products(self, event=None):
        """Filters table dynamically on search entry keypress."""
        query = self.ent_search.get().strip()

        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, name, category, quantity, price, date_added 
            FROM products 
            WHERE LOWER(name) LIKE ? OR LOWER(category) LIKE ?
            ORDER BY id ASC
            """,
            (f"%{query.lower()}%", f"%{query.lower()}%"),
        )
        rows = cursor.fetchall()
        conn.close()

        for idx, row in enumerate(rows):
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            total_cost = row[3] * row[4]
            date_val = row[5] if len(row) > 5 and row[5] else "N/A"
            self.tree.insert(
                "",
                tk.END,
                values=(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    f"Nu. {row[4]:.2f}",
                    f"Nu. {total_cost:.2f}",
                    date_val,
                ),
                tags=(tag,),
            )
        self.set_status(f"Filtered {len(rows)} record(s) matching '{query}'.")

    def view_selected_product(self):
        selected = self.tree.selection()
        if not selected:
            self.set_status("Selection Error: Select a row to view.", is_error=True)
            messagebox.showwarning(
                "Selection Error",
                "Please select a product from the table first to view its details.",
            )
            return

        item = self.tree.item(selected[0])
        record = item["values"]
        ViewDetailWindow(self.root, record)

    def view_all_products(self):
        self.ent_search.delete(0, tk.END)
        self.load_data()
        self.set_status("Displayed all inventory records.")

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            record = item["values"]
            self.selected_id = record[0]

            self.ent_name.delete(0, tk.END)
            self.ent_name.insert(0, record[1])

            if record[2] in self.combo_category["values"]:
                self.combo_category.set(record[2])

            price_clean = str(record[4]).replace("Nu. ", "").replace(",", "")
            self.ent_price.delete(0, tk.END)
            self.ent_price.insert(0, price_clean)

            self.ent_quantity.delete(0, tk.END)
            self.ent_quantity.insert(0, record[3])

    # =========================================================================
    # 5. CORE CRUD, EXPORT & UTILITIES
    # =========================================================================
    def set_status(self, message, is_error=False):
        color = self.colors["danger"] if is_error else self.colors["secondary"]
        self.lbl_status.config(text=f"Status: {message}", fg=color)

    def create_stat_card(self, parent, title, value, color, col):
        card = tk.Frame(
            parent,
            bg="white",
            highlightbackground=self.colors["border"],
            highlightthickness=1,
            padx=12,
            pady=6,
        )
        card.grid(row=0, column=col, sticky="ew", padx=4)
        parent.columnconfigure(col, weight=1)

        accent = tk.Frame(card, bg=color, height=3)
        accent.pack(fill=tk.X, side=tk.TOP, pady=(0, 4))

        lbl_title = tk.Label(
            card,
            text=title,
            font=("Segoe UI", 8, "bold"),
            bg="white",
            fg=self.colors["text_light"],
        )
        lbl_title.pack(anchor="w")

        lbl_val = tk.Label(
            card,
            text=value,
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg=self.colors["text_dark"],
        )
        lbl_val.pack(anchor="w")

        return lbl_val

    def create_styled_button(
        self, parent, text, bg_color, hover_color, command, px=8, py=4
    ):
        """Creates button with hover and active press feedback (dark visual indicator)."""
        press_color = self.colors["press_color"]

        btn = tk.Button(
            parent,
            text=text,
            font=("Segoe UI", 8, "bold"),
            bg=bg_color,
            fg="white",
            activebackground=press_color,
            activeforeground="white",
            bd=0,
            relief="flat",
            cursor="hand2",
            padx=px,
            pady=py,
            command=command,
        )

        # Dynamic color change bindings for Press and Hover
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))
        btn.bind("<ButtonPress-1>", lambda e: btn.config(bg=press_color))
        btn.bind("<ButtonRelease-1>", lambda e: btn.config(bg=hover_color))

        return btn

    def update_metrics(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*), SUM(quantity), SUM(quantity * price) FROM products"
        )
        count, total_stock, total_val = cursor.fetchone()
        conn.close()

        count = count if count else 0
        total_stock = total_stock if total_stock else 0
        total_val = total_val if total_val else 0.0

        self.card_total_items.config(text=str(count))
        self.card_total_stock.config(text=f"{total_stock:,}")
        self.card_total_value.config(text=f"Nu. {total_val:,.2f}")

    def validate_inputs(self):
        name = self.ent_name.get().strip()
        category = self.combo_category.get().strip()
        quantity = self.ent_quantity.get().strip()
        price = self.ent_price.get().strip()

        if not name or not category or not quantity or not price:
            self.set_status(
                "Validation Error: All fields are required!", is_error=True
            )
            messagebox.showerror("Validation Error", "All fields are required!")
            return None

        try:
            quantity = int(quantity)
            if quantity < 0:
                raise ValueError
        except ValueError:
            self.set_status(
                "Validation Error: Quantity must be a positive integer!", is_error=True
            )
            messagebox.showerror(
                "Validation Error", "Quantity must be a positive integer!"
            )
            return None

        try:
            price = float(price)
            if price < 0:
                raise ValueError
        except ValueError:
            self.set_status(
                "Validation Error: Price must be a positive number!", is_error=True
            )
            messagebox.showerror(
                "Validation Error", "Price must be a positive number!"
            )
            return None

        return name, category, quantity, price

    def add_product(self):
        if self.user_role != "admin":
            messagebox.showerror(
                "Permission Denied", "Only Administrators can add products."
            )
            return

        data = self.validate_inputs()
        if data is None:
            return

        current_timestamp = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Calculates next available ID based on current highest existing ID
        cursor.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM products")
        next_id = cursor.fetchone()[0]

        cursor.execute(
            "INSERT INTO products (id, name, category, quantity, price, date_added)"
            " VALUES (?, ?, ?, ?, ?, ?)",
            (next_id, *data, current_timestamp),
        )
        conn.commit()
        conn.close()

        self.set_status(f"Product '{data[0]}' added with ID #{next_id}!")
        messagebox.showinfo("Success", f"Product added successfully as ID #{next_id}!")
        self.clear_fields()
        self.load_data()

    def update_product(self):
        if self.user_role != "admin":
            messagebox.showerror(
                "Permission Denied", "Only Administrators can update products."
            )
            return

        if not self.selected_id:
            self.set_status(
                "Selection Error: Select a row to update.", is_error=True
            )
            messagebox.showwarning(
                "Selection Error",
                "Please select a record from the list to update.",
            )
            return

        data = self.validate_inputs()
        if data is None:
            return

        current_timestamp = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE products 
            SET name=?, category=?, quantity=?, price=?, date_added=? 
            WHERE id=?
            """,
            (*data, current_timestamp, self.selected_id),
        )
        conn.commit()
        conn.close()

        self.set_status(f"Record ID #{self.selected_id} updated successfully!")
        messagebox.showinfo("Success", "Product updated successfully!")
        self.clear_fields()
        self.load_data()

    def delete_product(self):
        if self.user_role != "admin":
            messagebox.showerror(
                "Permission Denied", "Only Administrators can delete products."
            )
            return

        if not self.selected_id:
            self.set_status(
                "Selection Error: Select a row to delete.", is_error=True
            )
            messagebox.showwarning(
                "Selection Error",
                "Please select a record from the list to delete.",
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete Product ID #{self.selected_id}?",
        )
        if confirm:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id=?", (self.selected_id,))
            conn.commit()
            conn.close()

            self.set_status(f"Record ID #{self.selected_id} deleted successfully.")
            messagebox.showinfo("Success", "Product deleted successfully!")
            self.clear_fields()
            self.load_data()

    def clear_fields(self):
        self.selected_id = None
        self.ent_name.delete(0, tk.END)
        self.combo_category.current(0)
        self.ent_price.delete(0, tk.END)
        self.ent_quantity.delete(0, tk.END)
        self.tree.selection_remove(self.tree.selection())
        self.set_status("Input fields cleared.")

    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="Export Inventory Data",
        )
        if not file_path:
            return

        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, category, quantity, price, date_added FROM products ORDER BY id ASC"
            )
            rows = cursor.fetchall()
            conn.close()

            with open(file_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
                    ["ID", "Name", "Category", "Quantity", "Price (Nu.)", "Total Value (Nu.)", "Date Added"]
                )
                for row in rows:
                    total_val = row[3] * row[4]
                    writer.writerow([row[0], row[1], row[2], row[3], row[4], total_val, row[5]])

            self.set_status(f"Exported data to {file_path}")
            messagebox.showinfo("Export Successful", f"Data exported successfully to:\n{file_path}")
        except Exception as e:
            self.set_status(f"Export failed: {str(e)}", is_error=True)
            messagebox.showerror("Export Error", f"Failed to export data:\n{str(e)}")

    def sort_column(self, col):
        items = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]

        def parse_val(val):
            clean_str = str(val).replace("Nu. ", "").replace(",", "")
            try:
                return float(clean_str)
            except ValueError:
                return val.lower()

        items.sort(key=lambda t: parse_val(t[0]), reverse=self.sort_reverse)

        for index, (val, k) in enumerate(items):
            self.tree.move(k, "", index)
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.tree.item(k, tags=(tag,))

        self.sort_reverse = not self.sort_reverse

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, category, quantity, price, date_added FROM products ORDER BY id ASC"
        )
        rows = cursor.fetchall()
        conn.close()

        for idx, row in enumerate(rows):
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            total_cost = row[3] * row[4]
            date_val = row[5] if len(row) > 5 and row[5] else "N/A"
            self.tree.insert(
                "",
                tk.END,
                values=(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    f"Nu. {row[4]:.2f}",
                    f"Nu. {total_cost:.2f}",
                    date_val,
                ),
                tags=(tag,),
            )

        self.update_metrics()
        self.set_status("Table loaded successfully.")


# =============================================================================
# 6. APPLICATION ENTRY POINT
# =============================================================================
def main():
    root = tk.Tk()

    def on_login_success(username, role):
        for widget in root.winfo_children():
            widget.destroy()

        def logout():
            for widget in root.winfo_children():
                widget.destroy()
            LoginWindow(root, on_login_success)

        ModernInventorySystem(root, username, role, logout)

    LoginWindow(root, on_login_success)
    root.mainloop()


if __name__ == "__main__":
    main()