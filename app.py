import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# -------------------- Theme --------------------
BG_COLOR = "#B6771D"
FG_COLOR = "#000000"
ACCENT = "#0099ff"
CARD = "#7B542F"

plt.style.use("dark_background")
sns.set_theme(style="darkgrid")


# -------------------- Main Dashboard Class --------------------
class SearchableDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("📊 Student Progress BY ABDULHAMEED")
        self.root.geometry("1700x900")
        self.root.configure(bg=BG_COLOR)
        self.df = None
        self.filtered_df = None

        # Sidebar
        self.sidebar = tk.Frame(root, bg=CARD, width=250)
        self.sidebar.pack(side="left", fill="y")

        tk.Label(self.sidebar, text="  STUDENT ANALYTICS  ", fg="white", bg=CARD,
                 font=("Segoe UI", 20, "bold")).pack(pady=20)
 
        # Buttons
        self.create_button("📂 Load CSV", self.load_csv)
        self.create_button("🔍 Apply Filters", self.apply_filters)
        self.create_button("📊 Show Charts", self.show_dashboard)
        self.create_button("🧑‍🎓 Student Detail", self.show_detail_section)
        self.create_button("🧹 Reset", self.reset_app)
        self.create_button("↩️ Exit", root.quit)
       

        
         
        tk.Label(self.sidebar, text="__________________________________________________", fg="white", bg=CARD, height=1).pack(pady=10)    
        
        # Filters
        tk.Label(self.sidebar, text="  Filters  ", fg="white", bg=CARD, font=("Segoe UI", 25, "bold")).pack(pady=5)
        self.create_filter("Gender", "gender_var")
        self.create_filter("Test Prep Course", "prep_var")
        self.create_filter("Lunch Type", "lunch_var")
        self.create_filter("Parental Education", "parent_var")

        # Container
        self.container = tk.Frame(root, bg=BG_COLOR,)
        self.container.pack(side="left", fill="both", expand=True)
        self.show_welcome()
        
        # # Login Pic
        # tk.Label(self.sidebar, text="ADMIN", fg="white", bg=CARD,font=("arial",25,'bold')).pack(pady=10) 
        
        

    # ---------- Sidebar Button ----------
    def create_button(self, text, cmd):
        btn = tk.Button(self.sidebar, text=text, command=cmd, fg="#B6771D", bg="White",
                        font=("Segoe UI", 11, "bold"), relief="flat", cursor="hand2")
        btn.pack(fill="x", padx=15, pady=8, ipady=5)

    # ---------- Filters ----------
    def create_filter(self, label_text, var_name):
        tk.Label(self.sidebar, text=f"{label_text}:", bg=CARD, fg="white").pack(anchor="w", padx=10)
        var = tk.StringVar(value="All")
        cb = ttk.Combobox(self.sidebar, textvariable=var,font=("arial",15), values=["All"], state="readonly")
        cb.pack(fill="x", padx=15, pady=10)
        setattr(self, var_name, var)
        setattr(self, f"{var_name}_cb", cb)

    # ---------- Welcome Screen ----------
    def show_welcome(self):
        for w in self.container.winfo_children():
            w.destroy()
        tk.Label(self.container, text="Welcome to Student Performance Dashboard!",
                 fg="white", bg=BG_COLOR, font=("Segoe UI", 38, "bold")).pack(pady=60)
        tk.Label(self.container, text="Upload a CSV file to view and search all students.",
                 fg="#ffffff", bg=BG_COLOR, font=("Segoe UI", 18,"bold")).pack(pady=8)

    # ---------- Load CSV ----------
    def load_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        try:
            self.df = pd.read_csv(path)
            if "avg_score" not in self.df.columns:
                self.df["avg_score"] = self.df[["math score", "reading score", "writing score"]].mean(axis=1)
            self.filtered_df = self.df.copy()

            # Update filters
            self.gender_var_cb["values"] = ["All"] + sorted(self.df["gender"].dropna().unique().tolist())
            self.prep_var_cb["values"] = ["All"] + sorted(self.df["test preparation course"].dropna().unique().tolist())
            self.lunch_var_cb["values"] = ["All"] + sorted(self.df["lunch"].dropna().unique().tolist())
            self.parent_var_cb["values"] = ["All"] + sorted(self.df["parental level of education"].dropna().unique().tolist())

            messagebox.showinfo("Success", "✅ CSV Loaded Successfully.")
            self.show_all_students()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading file:\n{e}")

    # ---------- Show All Students ----------
    def show_all_students(self):
        for w in self.container.winfo_children():
            w.destroy()

        # Header with search bar
        header = tk.Frame(self.container, bg=BG_COLOR)
        header.pack(fill="x", pady=10)

        tk.Label(header, text=f"📋 All Students ({len(self.filtered_df)} Records)",
                 fg="white", bg=BG_COLOR, font=("Segoe UI", 25, "bold")).pack(side="left", padx=20)

        tk.Label(header, text="🔎 Search by S.No:", bg=BG_COLOR, fg="white",
                 font=("Segoe UI", 18,"bold")).pack(side="left", padx=10)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(header, textvariable=self.search_var, width=30, font=("Segoe UI", 11))
        search_entry.pack(side="left", padx=5)
        tk.Button(header, text="Search", bg="#114ffa", fg="white", font=("Segoe UI", 11, "bold"),
                  command=self.search_student).pack(side="left", padx=5,)
        
   
        
        # Add numbering
        display_df = self.filtered_df.copy().reset_index(drop=True)
        display_df.insert(0, "S.No.", range(1, len(display_df) + 1))

        # Scrollable Frame
        frame = tk.Frame(self.container, bg=CARD)
        frame.pack(fill="both", expand=True, padx=15, pady=10)

        tree_scroll_y = tk.Scrollbar(frame, orient="vertical")
        tree_scroll_y.pack(side="right", fill="y")
        tree_scroll_x = tk.Scrollbar(frame, orient="horizontal")
        tree_scroll_x.pack(side="bottom", fill="x")

        self.tree = ttk.Treeview(frame, show="headings", yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)
        self.tree.pack(fill="both", expand=True)
        tree_scroll_y.config(command=self.tree.yview)
        tree_scroll_x.config(command=self.tree.xview)

        style = ttk.Style()
        style.configure("Treeview", background=CARD, fieldbackground=CARD, foreground="White", rowheight=25)

        self.tree["columns"] = list(display_df.columns)
        for col in display_df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130, anchor="center")

        for _, row in display_df.iterrows():
            self.tree.insert("", "end", values=list(row))

    # ---------- Search Student ----------
    def search_student(self):
        query = self.search_var.get().strip().lower()
        if not query:
            self.show_all_students()
            return

        # Try to interpret query as serial number (S.No.)
        try:
            sno = int(query)
            if 1 <= sno <= len(self.filtered_df):
                matches = self.filtered_df.iloc[[sno - 1]]
                self.filtered_df = matches
                self.show_all_students()
                return
        except ValueError:
            pass

        # Otherwise, search by ID or Name columns
        columns_to_search = [col for col in self.filtered_df.columns if "id" in col.lower() or "name" in col.lower()]
        if not columns_to_search:
            messagebox.showwarning("Not Found", "⚠️ No Name or ID column found in dataset.")
            return

        matches = self.filtered_df[
            self.filtered_df[columns_to_search].apply(
                lambda row: row.astype(str).str.lower().str.contains(query).any(), axis=1
            )
        ]

        if matches.empty:
            messagebox.showinfo("No Results", f"No records found for: {query}")
            return

        self.filtered_df = matches
        self.show_all_students()

    # ---------- Apply Filters ----------
    def apply_filters(self):
        if self.df is None:
            messagebox.showwarning("No Data", "Please load a CSV first!")
            return

        df = self.df.copy()
        if self.gender_var.get() != "All":
            df = df[df["gender"] == self.gender_var.get()]
        if self.prep_var.get() != "All":
            df = df[df["test preparation course"] == self.prep_var.get()]
        if self.lunch_var.get() != "All":
            df = df[df["lunch"] == self.lunch_var.get()]
        if self.parent_var.get() != "All":
            df = df[df["parental level of education"] == self.parent_var.get()]

        self.filtered_df = df
        messagebox.showinfo("Filters Applied", f"✅ {len(df)} students matched your filters.")
        self.show_all_students()

    # ---------- Charts ----------
    def show_dashboard(self):
        if self.filtered_df is None or self.filtered_df.empty:
            messagebox.showwarning("No Data", "No data to visualize!")
            return

        for w in self.container.winfo_children():
            w.destroy()

        tk.Label(self.container, text="📊 Dashboard Visualization", fg="White", bg=BG_COLOR,
                 font=("Segoe UI", 23, "bold")).pack(pady=10)

        fig, axes = plt.subplots(2, 2, figsize=(11, 8))

        sns.histplot(self.filtered_df["avg_score"], bins=20, ax=axes[0, 0], color=ACCENT)
        axes[0, 0].set_title("Average Score Distribution")

        sns.boxplot(x="gender", y="math score", data=self.filtered_df, ax=axes[0, 1], palette="crest")
        axes[0, 1].set_title("Math Score by Gender")

        mean_prep = self.filtered_df.groupby("test preparation course")[["math score", "reading score", "writing score"]].mean()
        mean_prep.plot(kind="bar", ax=axes[1, 0], color=["#00ccff", "#66ccff", "#99ccff"])
        axes[1, 0].set_title("Average Scores by Test Prep")

        corr = self.filtered_df[["math score", "reading score", "writing score", "avg_score"]].corr()
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=axes[1, 1])
        axes[1, 1].set_title("Correlation Matrix")

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)

    # ---------- Student Detail ----------
    def show_detail_section(self):
        if self.filtered_df is None or self.filtered_df.empty:
            messagebox.showwarning("No Data", "Please load data first!")
            return

        for w in self.container.winfo_children():
            w.destroy()

        tk.Label(self.container, text="🧑‍🎓 Individual Student Detail", fg="White", bg=BG_COLOR,
                 font=("Segoe UI", 25, "bold")).pack(pady=20)

        control = tk.Frame(self.container, bg=BG_COLOR)
        control.pack(pady=10)

        tk.Label(control, text="Enter Student No.:", fg="white", bg=BG_COLOR, font=("Segoe UI", 20)).pack(side="left", padx=5)
        self.index_entry = tk.Entry(control, width=30)
        self.index_entry.pack(side="left", padx=5)

        tk.Button(control, text="Show Detail", bg=ACCENT, fg="white",
                  command=self.display_student, font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)

        self.detail_box = tk.Text(self.container, bg=CARD, fg="white", font=("Arial", 16),
                                  height=100, width=100, wrap="word")
        self.detail_box.pack(pady=20)

    def display_student(self):
        try:
            idx = int(self.index_entry.get()) - 1
            if idx < 0 or idx >= len(self.filtered_df):
                messagebox.showerror("Error", "Invalid student number!")
                return
            student = self.filtered_df.iloc[idx]
            self.detail_box.delete(1.0, tk.END)
            self.detail_box.insert(tk.END, f"{student.to_string()}\n\n")
            class_avg = self.filtered_df[["math score", "reading score", "writing score"]].mean()
            diff = student[["math score", "reading score", "writing score"]] - class_avg
            self.detail_box.insert(tk.END, "Difference from Class Average:\n")
            self.detail_box.insert(tk.END, diff.to_string())
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------- Reset ----------
    def reset_app(self):
        self.df = None
        self.filtered_df = None
        for w in self.container.winfo_children():
            w.destroy()
        self.show_welcome()

# -------------------- Run App --------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = SearchableDashboard(root)
    root.mainloop()
