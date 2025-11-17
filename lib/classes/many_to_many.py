# classes/many_to_many.py

class Article:
    all = []

    def __init__(self, author, magazine, title):
        # Validate author and magazine types at creation time
        if not isinstance(author, Author):
            raise Exception("Author must be an Author instance.")
        if not isinstance(magazine, Magazine):
            raise Exception("Magazine must be a Magazine instance.")

        # Validate title at creation time
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise Exception("Title must be a string 5-50 characters long.")

        # set internal attributes
        self._author = author
        self._magazine = magazine
        self._title = title

        Article.all.append(self)

    # title: read-only
    @property
    def title(self):
        return self._title

    # author: mutable, but ignore invalid assignments
    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if isinstance(value, Author):
            self._author = value
        # else: ignore invalid assignment (do nothing)

    # magazine: mutable, but ignore invalid assignments
    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        if isinstance(value, Magazine):
            self._magazine = value
        # else: ignore invalid assignment


class Author:
    def __init__(self, name):
        if not isinstance(name, str):
            raise Exception("Name must be a string.")
        if len(name) == 0:
            raise Exception("Name must not be empty.")
        self._name = name

    # name: read-only (immutable)
    @property
    def name(self):
        return self._name

    # returns list of Article instances written by this author
    def articles(self):
        return [a for a in Article.all if a.author is self]

    # returns unique list of Magazine instances this author has written for
    def magazines(self):
        return list({a.magazine for a in self.articles()})

    # create and return new Article associated with this author
    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    # returns unique list of category strings; None if no articles
    def topic_areas(self):
        mags = self.magazines()
        if not mags:
            return None
        return list({m.category for m in mags})


class Magazine:
    all = []

    def __init__(self, name, category):
        # Use the setter logic by assigning to properties
        # but ensure invalid creation raises (tests expect validation at creation)
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise Exception("Magazine name must be a string 2-16 characters long.")
        if not isinstance(category, str) or len(category) == 0:
            raise Exception("Category must be a non-empty string.")

        self._name = name
        self._category = category

        Magazine.all.append(self)

    # name property is mutable, but ignore invalid assignments (no exceptions)
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and (2 <= len(value) <= 16):
            self._name = value
        # else: ignore invalid assignment

    # category property is mutable, but ignore invalid assignments (no exceptions)
    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._category = value
        # else: ignore invalid assignment

    # returns list of Article instances published by this magazine
    def articles(self):
        return [a for a in Article.all if a.magazine is self]

    # unique list of Author instances who have written for this magazine
    def contributors(self):
        return list({a.author for a in self.articles()})

    # titles of articles; None if no articles
    def article_titles(self):
        arts = self.articles()
        if not arts:
            return None
        return [a.title for a in arts]

    # authors who have written more than 2 articles for this magazine; None if none
    def contributing_authors(self):
        counts = {}
        for a in self.articles():
            counts.setdefault(a.author, 0)
            counts[a.author] += 1
        result = [author for author, cnt in counts.items() if cnt > 2]
        return result if result else None

    # classmethod top_publisher: Magazine with most articles; None if no articles
    @classmethod
    def top_publisher(cls):
        if not Article.all:
            return None
        return max(cls.all, key=lambda mag: len(mag.articles()))
