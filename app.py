import json
import streamlit as st

# File to store the library data
LIBRARY_FILE = "library.json"

def load_library():
    """Load the library from a file."""
    try:
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_library(library):
    """Save the library to a file."""
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

def add_book(library, title, author, year, genre, read_status):
    """Add a book to the library."""
    library.append({
        "Title": title,
        "Author": author,
        "Year": year,
        "Genre": genre,
        "Read": read_status
    })
    save_library(library)

def remove_book(library, title):
    """Remove a book from the library by title."""
    for book in library:
        if book["Title"].lower() == title.lower():
            library.remove(book)
            save_library(library)
            return True
    return False

def search_book(library, keyword, search_by):
    """Search for a book by title or author."""
    return [book for book in library if keyword.lower() in book[search_by].lower()]

def display_statistics(library):
    """Display total books and percentage read."""
    total_books = len(library)
    read_books = sum(1 for book in library if book["Read"])
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
    return total_books, percentage_read

def main():
    """Streamlit App UI."""
    st.title("📚 Personal Library Manager")
    library = load_library()

    menu = ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Statistics"]
    choice = st.sidebar.selectbox("Select an option", menu)

    if choice == "Add a Book":
        st.subheader("📖 Add a New Book")
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year", min_value=1000, max_value=2025, step=1)
        genre = st.text_input("Genre")
        read_status = st.checkbox("Mark as Read")
        if st.button("Add Book"):
            add_book(library, title, author, year, genre, read_status)
            st.success(f"'{title}' added successfully!")

    elif choice == "Remove a Book":
        st.subheader("❌ Remove a Book")
        book_titles = [book["Title"] for book in library]
        title_to_remove = st.selectbox("Select a book to remove", book_titles)
        if st.button("Remove Book"):
            if remove_book(library, title_to_remove):
                st.success(f"'{title_to_remove}' removed successfully!")
            else:
                st.error("Book not found!")

    elif choice == "Search for a Book":
        st.subheader("🔍 Search for a Book")
        search_by = st.radio("Search by", ["Title", "Author"])
        keyword = st.text_input(f"Enter {search_by}")
        if st.button("Search"):
            results = search_book(library, keyword, search_by)
            if results:
                for book in results:
                    status = "Read" if book["Read"] else "Unread"
                    st.write(f"📖 {book['Title']} by {book['Author']} ({book['Year']}) - {book['Genre']} - {status}")
            else:
                st.warning("No matching books found.")

    elif choice == "Display All Books":
        st.subheader("📚 Your Library")
        if library:
            for book in library:
                status = "Read" if book["Read"] else "Unread"
                st.write(f"📖 {book['Title']} by {book['Author']} ({book['Year']}) - {book['Genre']} - {status}")
        else:
            st.info("Your library is empty.")

    elif choice == "Statistics":
        st.subheader("📊 Library Statistics")
        total_books, percentage_read = display_statistics(library)
        st.write(f"📚 Total books: {total_books}")
        st.write(f"📖 Percentage read: {percentage_read:.2f}%")

if __name__ == "__main__":
    main()
