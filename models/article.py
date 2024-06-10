class Article:
    def __init__(self, id=None, title=None, content=None, author=None, magazine_id=None):
        if content is None:
            raise TypeError("Article content cannot be None")
        self._id = id
        self._title = title
        self._content = content
        self._author = author
        self._magazine_id = magazine_id

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def content(self):
        return self._content

    @property
    def author(self):
        return self._author

    @property
    def magazine_id(self):
        return self._magazine_id

    def save(self, cursor):
        cursor.execute(
            "INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
            (self._title, self._content, self._author.id, self._magazine_id)
        )
        self._id = cursor.lastrowid
        return self._id
