import unittest
from models.article import Article
from models.author import Author
from models.magazine import Magazine
from database.setup import create_tables, get_db_connection

class TestModels(unittest.TestCase):

    def setUp(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()
        create_tables()
        self.cursor.execute('DELETE FROM articles')
        self.cursor.execute('DELETE FROM authors')
        self.cursor.execute('DELETE FROM magazines')
        self.conn.commit()

    def tearDown(self):
        self.conn.close()

    def test_author_creation(self):
        author = Author(name="John Doe")
        author.create_author(self.cursor)
        self.assertEqual(author.name, "John Doe")
        self.assertIsNotNone(author.id)

    def test_article_creation(self):
        author = Author(name="John Doe")
        author.create_author(self.cursor)
        magazine = Magazine(name="Tech Weekly", category="Technology")
        magazine.save(self.cursor)
        article = Article(title="Test Title", content="Test Content", author=author, magazine_id=magazine.id)
        article.save(self.cursor)
        self.assertEqual(article.title, "Test Title")
        self.assertEqual(article.content, "Test Content")
        self.assertEqual(article.author.id, author.id)
        self.assertEqual(article.magazine_id, magazine.id)
        self.assertIsNotNone(article.id)

    def test_magazine_creation(self):
        magazine = Magazine(name="Tech Weekly", category="Technology")
        magazine.save(self.cursor)
        self.assertEqual(magazine.name, "Tech Weekly")
        self.assertEqual(magazine.category, "Technology")
        self.assertIsNotNone(magazine.id)

    def test_author_articles(self):
        author = Author(name="John Doe")
        author.create_author(self.cursor)
        magazine = Magazine(name="Tech Weekly", category="Technology")
        magazine.save(self.cursor)
        Article(title="Title 1", content="Content 1", author=author, magazine_id=magazine.id).save(self.cursor)
        Article(title="Title 2", content="Content 2", author=author, magazine_id=magazine.id).save(self.cursor)
        articles = author.articles(self.cursor)
        self.assertEqual(len(articles), 2)

    def test_author_magazines(self):
        author = Author(name="John Doe")
        author.create_author(self.cursor)
        magazine1 = Magazine(name="Tech Weekly", category="Technology")
        magazine2 = Magazine(name="Health Monthly", category="Health")
        magazine1.save(self.cursor)
        magazine2.save(self.cursor)
        Article(title="Title 1", content="Content 1", author=author, magazine_id=magazine1.id).save(self.cursor)
        Article(title="Title 2", content="Content 2", author=author, magazine_id=magazine2.id).save(self.cursor)
        magazines = author.magazines(self.cursor)
        self.assertEqual(len(magazines), 2)

    def test_magazine_articles(self):
        author = Author(name="John Doe")
        author.create_author(self.cursor)
        magazine = Magazine(name="Tech Weekly", category="Technology")
        magazine.save(self.cursor)
        Article(title="Title 1", content="Content 1", author=author, magazine_id=magazine.id).save(self.cursor)
        Article(title="Title 2", content="Content 2", author=author, magazine_id=magazine.id).save(self.cursor)
        articles = magazine.article_titles(self.cursor)
        self.assertEqual(len(articles), 2)

    def test_magazine_contributors(self):
        author1 = Author(name="John Doe")
        author2 = Author(name="Jane Smith")
        author1.create_author(self.cursor)
        author2.create_author(self.cursor)
        magazine = Magazine(name="Tech Weekly", category="Technology")
        magazine.save(self.cursor)
        Article(title="Title 1", content="Content 1", author=author1, magazine_id=magazine.id).save(self.cursor)
        Article(title="Title 2", content="Content 2", author=author2, magazine_id=magazine.id).save(self.cursor)
        contributors = magazine.contributing_authors(self.cursor)
        self.assertEqual(len(contributors), 2)

    def test_magazine_article_titles(self):
        author = Author(name="John Doe")
        author.create_author(self.cursor)
        magazine = Magazine(name="Tech Weekly", category="Technology")
        magazine.save(self.cursor)
        Article(title="Title 1", content="Content 1", author=author, magazine_id=magazine.id).save(self.cursor)
        Article(title="Title 2", content="Content 2", author=author, magazine_id=magazine.id).save(self.cursor)
        titles = magazine.article_titles(self.cursor)
        self.assertEqual(len(titles), 2)
        self.assertIn("Title 1", titles)
        self.assertIn("Title 2", titles)

    def test_magazine_contributing_authors(self):
        author1 = Author(name="John Doe")
        author2 = Author(name="Jane Smith")
        author1.create_author(self.cursor)
        author2.create_author(self.cursor)
        magazine = Magazine(name="Tech Weekly", category="Technology")
        magazine.save(self.cursor)
        Article(title="Title 1", content="Content 1", author=author1, magazine_id=magazine.id).save(self.cursor)
        Article(title="Title 2", content="Content 2", author=author1, magazine_id=magazine.id).save(self.cursor)
        Article(title="Title 3", content="Content 3", author=author1, magazine_id=magazine.id).save(self.cursor)
        Article(title="Title 4", content="Content 4", author=author2, magazine_id=magazine.id).save(self.cursor)
        authors = magazine.contributing_authors(self.cursor)
        self.assertEqual(len(authors), 2)

    def test_author_name_setter(self):
        author = Author(name="John Doe")
        author.name = "Jane Doe"
        self.assertEqual(author.name, "Jane Doe")
        with self.assertRaises(ValueError):
            author.name = ""

    def test_magazine_name_setter(self):
        magazine = Magazine(name="Tech Weekly", category="Technology")
        magazine.name = "Health Monthly"
        self.assertEqual(magazine.name, "Health Monthly")
        with self.assertRaises(ValueError):
            magazine.name = ""

    def test_magazine_category_setter(self):
        magazine = Magazine(name="Tech Weekly", category="Technology")
        magazine.category = "Health"
        self.assertEqual(magazine.category, "Health")
        with self.assertRaises(ValueError):
            magazine.category = ""

    def test_article_content(self):
        author = Author(name="John Doe")
        author.create_author(self.cursor)
        magazine = Magazine(name="Tech Weekly", category="Technology")
        magazine.save(self.cursor)
        article = Article(title="Test Title", content="Test Content", author=author, magazine_id=magazine.id)
        article.save(self.cursor)
        self.assertEqual(article.content, "Test Content")

    def test_article_without_content(self):
        author = Author(name="John Doe")
        author.create_author(self.cursor)
        magazine = Magazine(name="Tech Weekly", category="Technology")
        magazine.save(self.cursor)
        with self.assertRaises(TypeError):
            Article(title="Test Title", author=author, magazine_id=magazine.id).save(self.cursor)

    def test_duplicate_author_name(self):
        author1 = Author(name="John Doe")
        author2 = Author(name="John Doe")
        author1.create_author(self.cursor)
        author2.create_author(self.cursor)
        self.assertNotEqual(author1.id, author2.id)

    def test_duplicate_magazine_name(self):
        magazine1 = Magazine(name="Tech Weekly", category="Technology")
        magazine2 = Magazine(name="Tech Weekly", category="Health")
        magazine1.save(self.cursor)
        magazine2.save(self.cursor)
        self.assertNotEqual(magazine1.id, magazine2.id)

    def test_magazine_no_articles(self):
        magazine = Magazine(name="Tech Weekly", category="Technology")
        magazine.save(self.cursor)
        articles = magazine.article_titles(self.cursor)
        self.assertEqual(len(articles), 0)

    def test_author_no_articles(self):
        author = Author(name="John Doe")
        author.create_author(self.cursor)
        articles = author.articles(self.cursor)
        self.assertEqual(len(articles), 0)

    def test_magazine_no_contributors(self):
        magazine = Magazine(name="Tech Weekly", category="Technology")
        magazine.save(self.cursor)
        contributors = magazine.contributing_authors(self.cursor)
        self.assertEqual(len(contributors), 0)

    def test_magazine_no_article_titles(self):
        magazine = Magazine(name="Tech Weekly", category="Technology")
        magazine.save(self.cursor)
        titles = magazine.article_titles(self.cursor)
        self.assertListEqual(titles, [])

    def test_magazine_no_contributing_authors(self):
        magazine = Magazine(name="Tech Weekly", category="Technology")
        magazine.save(self.cursor)
        authors = magazine.contributing_authors(self.cursor)
        self.assertEqual(len(authors), 0)

if __name__ == '__main__':
    unittest.main()
