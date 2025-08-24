import sys
import datetime
from fibo import fib
from collections import deque

# Contact Management System
contacts = {
    'friends': [],      # List as stack for friend contacts
    'family': deque(),  # Queue for family contacts
    'work': set(),      # Set for work contacts
    'groups': {}        # Dictionary for group management
}

def add_friend(name, phone):
    contacts['friends'].append({'name': name, 'phone': phone})  # Using list as stack

def add_family(name, phone):
    contacts['family'].append({'name': name, 'phone': phone})  # Using queue

def add_work(name, phone):
    contacts['work'].add((name, phone))  # Using set (tuple as immutable item)

def create_group(group_name, members=None):
    if members is None:
        members = []
    contacts['groups'][group_name] = members  # Dictionary usage

def remove_last_friend():
    if contacts['friends']:
        return contacts['friends'].pop()  # Stack operation (LIFO)
    return None

def remove_first_family():
    if contacts['family']:
        return contacts['family'].popleft()  # Queue operation (FIFO)
    return None

def remove_work_contact(name, phone):
    contacts['work'].discard((name, phone))  # Set operation

def main():    
    # Fibonacci numbers module imported from file fibo.py
    fib(500)

    # Demonstrate list as stack
    add_friend("John", "123-456")
    add_friend("Alice", "789-012")
    
    # Demonstrate queue
    add_family("Mom", "111-222")
    add_family("Dad", "333-444")
    
    # Demonstrate set
    add_work("Bob", "555-666")
    add_work("Carol", "777-888")
    add_work("Bob", "555-666")  # Duplicate won't be added
    
    # Demonstrate dictionary and nested list
    create_group("Team A", [
        {"name": "John", "role": "lead"},
        {"name": "Alice", "role": "dev"}
    ])
    
    # Demonstrate looping through different data structures
    print("\nFriends (Stack):")
    for friend in reversed(contacts['friends']):  # LIFO order
        print(f"{friend['name']}: {friend['phone']}")
    
    print("\nFamily (Queue):")
    for family in contacts['family']:  # FIFO order
        print(f"{family['name']}: {family['phone']}")
    
    print("\nWork Contacts (Set):")
    for name, phone in contacts['work']:
        print(f"{name}: {phone}")
    
    print("\nGroups (Dictionary with nested lists):")
    for group_name, members in contacts['groups'].items():
        print(f"\n{group_name}:")
        for member in members:
            print(f"  {member['name']} - {member['role']}")
    
    # Demonstrate del statement
    last_friend = remove_last_friend()
    if last_friend:
        print(f"\nRemoved last friend: {last_friend['name']}")
    
    first_family = remove_first_family()
    if first_family:
        print(f"Removed first family member: {first_family['name']}")


if __name__ == "__main__":
    main()
