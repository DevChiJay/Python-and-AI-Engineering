
# Simple CLI To-Do List Manager
# This script demonstrates Python basics: lists, loops, strings, numbers, and user input.

# Create an empty list to store to-do items
todo_list = []

def show_menu():
	print("\nTo-Do List Manager")
	print("1. Add a task")
	print("2. View tasks")
	print("3. Remove a task")
	print("4. Exit")

while True:  # This loop keeps the program running until the user chooses to exit
	show_menu()
	choice = input("Enter your choice (1-4): ")  # Get user input as a string

	if choice == "1":
		# Adding a task
		task = input("Enter the task description: ")  # Get task as a string
		todo_list.append(task)  # Add the new task to the end of the list
		print(f'Added: "{task}"')

	elif choice == "2":
		# Viewing all tasks
		if not todo_list:
			print("Your to-do list is empty.")
		else:
			print("\nYour tasks:")
			# Use a loop to print each task with its number
			for idx, task in enumerate(todo_list, start=1):
				print(f"{idx}. {task}")  # idx is a number, task is a string

	elif choice == "3":
		# Removing a task by its number
		if not todo_list:
			print("No tasks to remove.")
		else:
			for idx, task in enumerate(todo_list, start=1):
				print(f"{idx}. {task}")
			num = input("Enter the number of the task to remove: ")
			# Convert the input string to an integer
			if num.isdigit():
				num = int(num)
				# Check if the number is valid
				if 1 <= num <= len(todo_list):
					removed = todo_list.pop(num - 1)  # Remove the task at the given index
					print(f'Removed: "{removed}"')
				else:
					print("Invalid task number.")
			else:
				print("Please enter a valid number.")

	elif choice == "4":
		print("Goodbye!")
		break  # Exit the loop and end the program

	else:
		print("Invalid choice. Please enter a number from 1 to 4.")
