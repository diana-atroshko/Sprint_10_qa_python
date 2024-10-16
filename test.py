import pytest
from main import BooksCollector

class TestBooksCollector:
    @pytest.fixture
    def book_collector(self):
       return BooksCollector()

    @pytest.mark.parametrize("book_name, expected_count", [['Гордость и предубеждение и зомби', 1],['Гордость и предубеждение и зомби', 1]])

    # добавляем новую книгу
    def test_add_new_book_valid(self, book_collector, book_name, expected_count):
         book_collector.add_new_book(book_name)
         assert len(book_collector.get_books_genre()) == expected_count

    def test_add_new_book_long_name_fail(self, book_collector):
        book_collector.add_new_book("A" * 41)
        assert len(book_collector.books_genre) == 0

    # устанавливаем книге жанр
    def test_set_book_genre_valid(self, book_collector):
        book_collector.add_new_book('Гордость и предубеждение и зомби')
        book_collector.set_book_genre("Гордость и предубеждение и зомби", "Ужасы")
        assert book_collector.get_book_genre("Гордость и предубеждение и зомби") == "Ужасы"

    def test_set_book_genre_unknown_book_fail(self, book_collector):
        book_collector.set_book_genre('Книга мыслей', 'Фантастика')
        assert book_collector.get_book_genre("Книга мыслей") is None

    def test_set_book_genre_unknown_genre_invalid(self, book_collector):
        book_collector.add_new_book('Властелин колец')
        book_collector.set_book_genre('Властелин колец', 'Героический эпос')
        assert book_collector.get_book_genre('Властелин колец') == ""

    # жанр книги по её имени
    def test_get_book_genre_existing_book_valid(self, book_collector):
        book_collector.add_new_book('Гордость и предубеждение и зомби')
        book_collector.set_book_genre("Гордость и предубеждение и зомби", "Ужасы")
        assert book_collector.get_book_genre("Гордость и предубеждение и зомби") == "Ужасы"

    def test_get_book_genre_nonexistent_book_invalid(self, book_collector):
        assert book_collector.get_book_genre("Гордость и предубеждение и зомби") is None

    # список книг с определённым жанром
    def test_get_books_with_specific_genre_existing_valid(self, book_collector):
        book_collector.add_new_book('Гордость и предубеждение и зомби')
        book_collector.set_book_genre("Гордость и предубеждение и зомби", "Фантастика")
        book_collector.add_new_book('Властелин колец')
        book_collector.set_book_genre('Властелин колец', 'Фантастика')
        assert book_collector.get_books_with_specific_genre('Фантастика') == ["Гордость и предубеждение и зомби", 'Властелин колец']

    def test_get_books_with_specific_genre_nonexisting_invalid(self, book_collector):
        book_collector.add_new_book('Гордость и предубеждение и зомби')
        assert book_collector.get_books_with_specific_genre('Фантастика') == []

    # словарь books_genre
    def test_get_books_genre(self, book_collector):
        book_collector.add_new_book('Гордость и предубеждение и зомби')
        book_collector.set_book_genre('Гордость и предубеждение и зомби', "Фантастика")
        assert book_collector.get_books_genre() == {"Гордость и предубеждение и зомби": "Фантастика"}

    #  книги, подходящие детям
    def test_get_books_for_children_valid(self, book_collector):
        book_collector.add_new_book('Гордость и предубеждение и зомби')
        book_collector.set_book_genre('Гордость и предубеждение и зомби', "Фантастика")
        book_collector.add_new_book('Зомби')
        book_collector.set_book_genre("Зомби", "Ужасы")
        assert book_collector.get_books_for_children() == ['Гордость и предубеждение и зомби']

    def test_get_books_for_children_nothing(self, book_collector):
        book_collector.add_new_book('Зомби')
        book_collector.set_book_genre("Зомби", "Ужасы")
        assert book_collector.get_books_for_children() == []

    # книгу в Избранное
    def test_add_book_in_favorites_valid(self, book_collector):
        book_collector.add_new_book('Зомби')
        book_collector.add_book_in_favorites("Зомби")
        assert "Зомби" in book_collector.favorites

    def test_add_book_in_favorites_dublicate_book_invalid(self, book_collector):
        book_collector.add_new_book('Зомби')
        book_collector.add_book_in_favorites("Зомби")
        book_collector.add_book_in_favorites("Зомби")
        assert len(book_collector.favorites) == 1

    # удаляем книгу из Избранного
    def test_delete_book_from_favorites_exist_book_valid(self, book_collector):
        book_collector.add_new_book('Зомби')
        book_collector.add_book_in_favorites("Зомби")
        book_collector.delete_book_from_favorites("Зомби")
        assert len(book_collector.favorites) == 0 or "Зомби" not in book_collector.favorites

    def test_delete_book_from_favorites_nonexist_book_valid(self, book_collector):
        book_collector.add_new_book('Зомби')
        book_collector.add_book_in_favorites("Зомби")
        book_collector.delete_book_from_favorites("Темные аллеи")
        assert len(book_collector.favorites) == 1

    # получаем список Избранных книг
    def test_get_list_of_favorites_books_valid(self, book_collector):
        book_collector.add_new_book('Зомби')
        book_collector.add_book_in_favorites("Зомби")
        assert book_collector.get_list_of_favorites_books() == ['Зомби']