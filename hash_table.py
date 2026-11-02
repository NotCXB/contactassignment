class Contact:
    '''
    Contact class to represent a contact with a name and number.
    Attributes:
        name (str): The name of the contact.
        number (str): The phone number of the contact.
    '''
    
    def __init__(self, name: str, number: str):
        self.name = name
        self.number = number

    def __str__(self) -> str:
        return f"{self.name}: {self.number}"

class Node:
    '''
    Node class to represent a single entry in the hash table.
    Attributes:
        key (str): The key (name) of the contact.
        value (Contact): The value (Contact object) associated with the key.
        next (Node): Pointer to the next node in case of a collision.
    '''
   
    def __init__(self, key: str, value: Contact):
        self.key = key
        self.value = value
        self.next = None

class HashTable:
    '''
    HashTable class to represent a hash table for storing contacts.
    Attributes:
        size (int): The size of the hash table.
        data (list): The underlying array to store linked lists for collision handling.
    Methods:
        hash_function(key): Converts a string key into an array index.
        insert(key, value): Inserts a new contact into the hash table.
        search(key): Searches for a contact by name.
        print_table(): Prints the structure of the hash table.
    '''
    
    def __init__(self, size: int = 10):
        if size <= 0:
            raise ValueError("Hash table size must be positive.")
        self.size = size
        self.data = [None] * size

    def hash_function(self, key: str) -> int:
        return sum(ord(character) for character in key) % self.size

    def insert(self, key: str, value: str) -> None:
        """Insert a name and phone number, or update an existing contact."""
        index = self.hash_function(key)
        current = self.data[index]

        if current is None:
            self.data[index] = Node(key, Contact(key, value))
            return

        while True:
            if current.key == key:
                current.value.number = value
                return
            if current.next is None:
                current.next = Node(key, Contact(key, value))
                return
            current = current.next

    def search(self, key: str):
        """Return the matching contact, or None if the name is absent."""
        current = self.data[self.hash_function(key)]
        while current is not None:
            if current.key == key:
                return current.value
            current = current.next
        return None

    def print_table(self) -> None:
        for index, current in enumerate(self.data):
            contacts = []
            while current is not None:
                contacts.append(f"- {current.value}")
                current = current.next
            contents = " ".join(contacts) if contacts else "Empty"
            print(f"Index {index}: {contents}")

# Test your hash table implementation here.  
if __name__ == "__main__":
    table = HashTable(10)

    # 1. Test inserting and finding a contact.
    table.insert("John", "909-876-1234")
    contact = table.search("John")
    assert contact is not None
    assert contact.number == "909-876-1234"
    assert str(contact) == "John: 909-876-1234"

    # 2. Test searching for a name that doesn't exist.
    assert table.search("Chris") is None

    # 3. Test collisions.
    # Amy and May contain the same letters, so their ord() sums match.
    assert table.hash_function("Amy") == table.hash_function("May")

    table.insert("Amy", "111-222-3333")
    table.insert("May", "222-333-1111")

    # Both contacts must remain accessible despite sharing an index.
    assert table.search("Amy").number == "111-222-3333"
    assert table.search("May").number == "222-333-1111"

    # Check that both contacts are in the linked list.
    index = table.hash_function("Amy")
    node = table.data[index]
    names = []
    while node is not None:
        names.append(node.key)
        node = node.next

    assert "Amy" in names
    assert "May" in names

    # 4. Test duplicate names at both positions in the chain.
    table.insert("Amy", "999-999-9999")
    table.insert("May", "888-888-8888")

    assert table.search("Amy").number == "999-999-9999"
    assert table.search("May").number == "888-888-8888"

    # Updating must not create additional nodes.
    node = table.data[index]
    names = []
    while node is not None:
        names.append(node.key)
        node = node.next

    assert names.count("Amy") == 1
    assert names.count("May") == 1

    # 5. Visually inspect the table.
    table.print_table()
    print("All tests passed!")