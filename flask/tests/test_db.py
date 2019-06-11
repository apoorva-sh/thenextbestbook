from bson.json_util import dumps
import os
import sys
import mongomock
# To enable books to be discovered by test cases
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..')))
from app.controllers.models.books import BooksCollection


def test_regex_search():
    """
    tests regex search on books collection
    """
    collection = mongomock.MongoClient().db.collection
    objects = [{"title": "title_1"}, {"title": "title_2"}]
    for obj in objects:
        obj['_id'] = collection.insert_one(obj)
    books_collection = BooksCollection(collection)
    result = books_collection.get_books_by_regex("title_1")

    assert '[{"title": "title_1"}]' == dumps(result)


def test_similar_books():
    """
    fetch similar_books  for the given book_id
    """
    # Inserting documents to the mock collection
    collection = mongomock.MongoClient().db.collection
    objects = [{"book_id": "AB123LTPL", "title": "title_1",
                "similar_books": ["123", "456", "768"]}]
    for obj in objects:
        obj['_id'] = collection.insert_one(obj)

    # call
    books_collection = BooksCollection(collection)
    result = books_collection.get_similar_books_by_book_id("AB123LTPL")

    assert '[{"similar_books": ["123", "456", "768"]}]' == dumps(result)


def test_get_books_details_by_id():
    """
    get all book details for
    """
    collection = mongomock.MongoClient().db.collection
    objects = [{"book_id": "123", "title": "title_1"},
               {"book_id": "456", "title": "title_2"},
               {"book_id": "789", "title": "title_3"}]

    for obj in objects:
        obj['_id'] = collection.insert_one(obj)
    books_collection = BooksCollection(collection)
    result = books_collection.get_books_details(["123", "456", "789"])

    assert '[{"book_id": "123", "title": "title_1"}, {"book_id": "456", "title": "title_2"}, {"book_id": "789", "title": "title_3"}]'\
           == dumps(result)