import tkinter as tk
from tkinter import messagebox, ttk

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Manager")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Configure style
        self.root.configure(bg="#f0f0f0")
        
        # Title Label
        title_label = tk.Label(
            root,
            text="📝 My To-Do List",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        title_label.pack(pady=20)
        
        # Frame for input
        input_frame = tk.Frame(root, bg="#f0f0f0")
        input_frame.pack(pady=10)
        
        # Entry widget
        self.task_entry = tk.Entry(
            input_frame,
            font=("Arial", 12),
            width=30,
            bd=2,
            relief="solid"
        )
        self.task_entry.pack(side=tk.LEFT, padx=5)
        self.task_entry.bind('<Return>', lambda e: self.add_task())
        
        # Add button
        add_btn = tk.Button(
            input_frame,
            text="Add Task",
            font=("Arial", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.add_task
        )
        add_btn.pack(side=tk.LEFT, padx=5)
        
        # Frame for listbox and scrollbar
        list_frame = tk.Frame(root, bg="#f0f0f0")
        list_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox for tasks
        self.task_listbox = tk.Listbox(
            list_frame,
            font=("Arial", 11),
            bd=2,
            relief="solid",
            selectmode=tk.SINGLE,
            yscrollcommand=scrollbar.set,
            activestyle='none',
            selectbackground="#e3f2fd"
        )
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.task_listbox.yview)
        
        # Button frame
        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.pack(pady=15)
        
        # Mark Complete button
        complete_btn = tk.Button(
            button_frame,
            text="✓ Mark Complete",
            font=("Arial", 10),
            bg="#2196F3",
            fg="white",
            bd=0,
            padx=12,
            pady=8,
            cursor="hand2",
            command=self.mark_complete
        )
        complete_btn.grid(row=0, column=0, padx=5)
        
        # Delete button
        delete_btn = tk.Button(
            button_frame,
            text="🗑 Delete Task",
            font=("Arial", 10),
            bg="#f44336",
            fg="white",
            bd=0,
            padx=12,
            pady=8,
            cursor="hand2",
            command=self.delete_task
        )
        delete_btn.grid(row=0, column=1, padx=5)
        
        # Clear All button
        clear_btn = tk.Button(
            button_frame,
            text="Clear All",
            font=("Arial", 10),
            bg="#FF9800",
            fg="white",
            bd=0,
            padx=12,
            pady=8,
            cursor="hand2",
            command=self.clear_all
        )
        clear_btn.grid(row=0, column=2, padx=5)
        
        # Task counter label
        self.counter_label = tk.Label(
            root,
            text="Total Tasks: 0",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#666666"
        )
        self.counter_label.pack(pady=10)
        
    def add_task(self):
        """Add a new task to the list"""
        task = self.task_entry.get().strip()
        if task:
            self.task_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
            self.update_counter()
        else:
            messagebox.showwarning("Empty Task", "Please enter a task!")
    
    def delete_task(self):
        """Delete the selected task"""
        try:
            selected_index = self.task_listbox.curselection()[0]
            self.task_listbox.delete(selected_index)
            self.update_counter()
        except IndexError:
            messagebox.showwarning("No Selection", "Please select a task to delete!")
    
    def mark_complete(self):
        """Mark the selected task as complete"""
        try:
            selected_index = self.task_listbox.curselection()[0]
            task = self.task_listbox.get(selected_index)
            
            # Check if already marked complete
            if not task.startswith("✓ "):
                self.task_listbox.delete(selected_index)
                self.task_listbox.insert(selected_index, f"✓ {task}")
                self.task_listbox.itemconfig(selected_index, fg="#808080")
        except IndexError:
            messagebox.showwarning("No Selection", "Please select a task to mark as complete!")
    
    def clear_all(self):
        """Clear all tasks from the list"""
        if self.task_listbox.size() > 0:
            result = messagebox.askyesno("Confirm", "Are you sure you want to clear all tasks?")
            if result:
                self.task_listbox.delete(0, tk.END)
                self.update_counter()
        else:
            messagebox.showinfo("Empty List", "No tasks to clear!")
    
    def update_counter(self):
        """Update the task counter"""
        count = self.task_listbox.size()
        self.counter_label.config(text=f"Total Tasks: {count}")

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
