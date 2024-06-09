# class Author:
#     def __init__(self, id=None, name=None):
#         self._id = id
#         self._name = name

#     @property
#     def id(self):
#         return self._id

#     @property
#     def name(self):
#         return self._name

#     @name.setter
#     def name(self, value):
#         if isinstance(value, str) and len(value) > 0:
#             self._name = value
#         else:
#             raise ValueError("Name must be a non-empty string")

#     def create_author(self, cursor):
#         cursor.execute("INSERT INTO authors (name) VALUES (?)", (self._name,))
#         self._id = cursor.lastrowid
#         return self._id

#     @classmethod
#     def get_all_authors(cls, cursor):
#         cursor.execute("SELECT * FROM authors")
#         authors_data = cursor.fetchall()
#         return [cls(author_data[0], author_data[1]) for author_data in authors_data]

#     def articles(self, cursor):
#         cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self._id,))
#         articles_data = cursor.fetchall()
#         return articles_data

#     def magazines(self, cursor):
#         cursor.execute("""
#             SELECT magazines.*
#             FROM magazines
#             JOIN articles ON magazines.id = articles.magazine_id
#             WHERE articles.author_id = ?
#         """, (self._id,))
#         magazines_data = cursor.fetchall()
#         return magazines_data

