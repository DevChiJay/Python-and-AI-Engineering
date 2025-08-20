
# Number Analyzer CLI Tool
# Demonstrates Python control flow: if, for, range, break, continue, else, pass, match, functions, lambda, and docstrings.

def analyze_number(num, *, show_even=True, show_odd=True):
	"""
	Analyze a number and print if it's even or odd.
	Uses keyword-only arguments for options.
	"""
	# if statement checks a condition
	if num % 2 == 0 and show_even:
		print(f"{num} is even.")
	elif num % 2 != 0 and show_odd:
		print(f"{num} is odd.")
	else:
		pass  # 'pass' does nothing, used as a placeholder

def print_range(start, end):
	"""
	Print numbers in a range using for loop and range().
	Skips numbers divisible by 3 using continue.
	Stops at 42 using break.
	"""
	for i in range(start, end):  # for loop with range
		if i == 42:
			print("Reached 42, stopping early with break.")
			break  # exit the loop
		if i % 3 == 0:
			continue  # skip numbers divisible by 3
		print(i)
	else:
		# else on a for loop runs if loop wasn't broken
		print("Finished printing range without hitting 42.")

# Lambda expression: a small anonymous function
square = lambda x: x * x

def match_example(value):
	"""
	Demonstrates the match statement (Python 3.10+).
	"""
	# match statement checks patterns
	match value:
		case 0:
			print("Zero!")
		case 1 | 2:
			print("One or Two!")
		case int() as n if n > 2:
			print(f"A positive integer greater than 2: {n}")
		case str() as s:
			print(f"A string: {s}")
		case _:
			print("Something else!")

def main():
	"""Main function to run the CLI tool."""
	print("Welcome to the Number Analyzer!")
	while True:
		print("\nMenu:")
		print("1. Analyze a number (even/odd)")
		print("2. Print a range (skip multiples of 3, stop at 42)")
		print("3. Square a number (lambda demo)")
		print("4. Match statement demo")
		print("5. Exit")
		choice = input("Choose an option (1-5): ")

		if choice == "1":
			n = input("Enter a number: ")
			if n.isdigit():
				analyze_number(int(n))
			else:
				print("Please enter a valid integer.")

		elif choice == "2":
			start = input("Start of range: ")
			end = input("End of range: ")
			if start.isdigit() and end.isdigit():
				print_range(int(start), int(end))
			else:
				print("Please enter valid integers.")

		elif choice == "3":
			n = input("Enter a number to square: ")
			if n.isdigit():
				print(f"{n} squared is {square(int(n))}")
			else:
				print("Please enter a valid integer.")

		elif choice == "4":
			val = input("Enter a value (number or text): ")
			# Try to convert to int if possible
			try:
				val = int(val)
			except ValueError:
				pass
			match_example(val)

		elif choice == "5":
			print("Goodbye!")
			break
		else:
			print("Invalid choice. Please select 1-5.")

if __name__ == "__main__":
	main()
