import pytest
from main import BooksCollector

class TestBooksCollector:
    @pytest.fixture
    def book_collector(self):
       return BooksCollector()

    book_1 = 'Гордость и предубеждение и зомби'
    book_2 = '1984'
    book_3 = 'Властелин колец'
    book_4 = 'Зомби'
    unkn_book = 'Книга мыслей'


    @pytest.mark.parametrize("book_name, expected_count", [[book_1, 1],[book_2, 1]])

    # добавляем новую книгу
    def test_add_new_book_valid(self, book_collector, book_name, expected_count):
         book_collector.add_new_book(book_name)
         assert len(book_collector.get_books_genre()) == expected_count

    def test_add_new_book_long_name_fail(self, book_collector):
        book_collector.add_new_book("A" * 41)
        assert len(book_collector.books_genre) == 0

    # устанавливаем книге жанр
    def test_set_book_genre_valid(self, book_collector):
        book_collector.add_new_book(self.book_1)
        book_collector.set_book_genre(self.book_1, "Ужасы")
        assert book_collector.get_book_genre(self.book_1) == "Ужасы"

    def test_set_book_genre_unknown_book_fail(self, book_collector):
        book_collector.set_book_genre(self.unkn_book, 'Фантастика')
        assert book_collector.get_book_genre(self.unkn_book) is None

    def test_set_book_genre_unknown_genre_invalid(self, book_collector):
        book_collector.add_new_book(self.book_3)
        book_collector.set_book_genre(self.book_3, 'Героический эпос')
        assert book_collector.get_book_genre(self.book_3) == ""

    # жанр книги по её имени
    def test_get_book_genre_existing_book_valid(self, book_collector):
        book_collector.add_new_book(self.book_1)
        book_collector.set_book_genre(self.book_1, "Ужасы")
        assert book_collector.get_book_genre(self.book_1) == "Ужасы"

    def test_get_book_genre_nonexistent_book_invalid(self, book_collector):
        assert book_collector.get_book_genre(self.book_1) is None

    # список книг с определённым жанром
    def test_get_books_with_specific_genre_existing_valid(self, book_collector):
        book_collector.add_new_book(self.book_1)
        book_collector.set_book_genre(self.book_1, "Фантастика")
        book_collector.add_new_book(self.book_1)
        book_collector.set_book_genre(self.book_1, 'Фантастика')
        assert book_collector.get_books_with_specific_genre('Фантастика') == [self.book_1, self.book_3]

    def test_get_books_with_specific_genre_nonexisting_invalid(self, book_collector):
        book_collector.add_new_book(self.book_1)
        assert book_collector.get_books_with_specific_genre('Фантастика') == []

    # словарь books_genre
    def test_get_books_genre(self, book_collector):
        book_collector.add_new_book(self.book_1)
        book_collector.set_book_genre(self.book_1, "Фантастика")
        assert book_collector.get_books_genre() == {self.book_1: "Фантастика"}

    #  книги, подходящие детям
    def test_get_books_for_children_valid(self, book_collector):
        book_collector.add_new_book(self.book_1)
        book_collector.set_book_genre(self.book_1, "Фантастика")
        book_collector.add_new_book(self.book_4)
        book_collector.set_book_genre(self.book_4, "Ужасы")
        assert book_collector.get_books_for_children() == [self.book_1]

    def test_get_books_for_children_nothing(self, book_collector):
        book_collector.add_new_book(self.book_4)
        book_collector.set_book_genre(self.book_4, "Ужасы")
        assert book_collector.get_books_for_children() == []

    # книгу в Избранное
    def test_add_book_in_favorites_valid(self, book_collector):
        book_collector.add_new_book(self.book_4)
        book_collector.add_book_in_favorites(self.book_4)
        assert self.book_4 in book_collector.favorites

    def test_add_book_in_favorites_dublicate_book_invalid(self, book_collector):
        book_collector.add_new_book(self.book_4)
        book_collector.add_book_in_favorites(self.book_4)
        book_collector.add_book_in_favorites(self.book_4)
        assert len(book_collector.favorites) == 1

    # удаляем книгу из Избранного
    def test_delete_book_from_favorites_exist_book_valid(self, book_collector):
        book_collector.add_new_book(self.book_4)
        book_collector.add_book_in_favorites(self.book_4)
        book_collector.delete_book_from_favorites(self.book_4)
        assert len(book_collector.favorites) == 0 or self.book_4 not in book_collector.favorites

    def test_delete_book_from_favorites_nonexist_book_valid(self, book_collector):
        book_collector.add_new_book(self.book_4)
        book_collector.add_book_in_favorites(self.book_4)
        book_collector.delete_book_from_favorites("Темные аллеи")
        assert len(book_collector.favorites) == 1

    # получаем список Избранных книг
    def test_get_list_of_favorites_books_valid(self, book_collector):
        book_collector.add_new_book(self.book_4)
        book_collector.add_book_in_favorites(self.book_4)
        assert book_collector.get_list_of_favorites_books() == [self.book_4]