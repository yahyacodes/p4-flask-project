from faker import Faker
from app import app
from models import db, User, Profile, Book, Borrow, BookCategory, Author, Review
from datetime import datetime, timedelta

fake = Faker()

with app.app_context():
    def users_profiles(users=10):
        for _ in range(users):
            user = User(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password()
            )
            db.session.add(user)
            profile = Profile(
                firstname=fake.first_name(),
                lastname=fake.last_name(),
                user=user
            )
            db.session.add(profile)
        db.session.commit()

    def seed_authors(authors=5):
        for _ in range(authors):
            author = Author(
                authorname=fake.name()
            )
            db.session.add(author)
        db.session.commit()

    def book_categories(books=20, categories=5):
        for _ in range(books):
            book = Book(
                title=fake.sentence(),
                description=fake.paragraph(),
                author_id=fake.random_int(min=1, max=authors),
                user_id=fake.random_int(min=1, max=users)
            )
            db.session.add(book)

            for _ in range(fake.random_int(min=1, max=categories)):
                category = BookCategory(
                    categoryname=fake.word(),
                    book=book
                )
                db.session.add(category)
        db.session.commit()

    def seed_borrows(borrows=15, days_range=30):
        for _ in range(borrows):
            borrow = Borrow(
                book_id=fake.random_int(min=1, max=books),
                user_id=fake.random_int(min=1, max=users),
                date=fake.date_time_this_decade(),
                return_date=fake.date_time_this_decade() + timedelta(days=fake.random_int(min=1, max=days_range))
            )
            db.session.add(borrow)
        db.session.commit()

    def seed_reviews(reviews=30):
        for _ in range(reviews):
            review = Review(
                comment=fake.paragraph(),
                book_id=fake.random_int(min=1, max=books),
                user_id=fake.random_int(min=1, max=users)
            )
            db.session.add(review)
        db.session.commit()

    if __name__ == "__main__":
        users = 10
        authors = 5
        books = 20
        categories = 5
        borrows = 15
        reviews = 30

        users_profiles(users)
        seed_authors(authors)
        book_categories(books, categories)
        seed_borrows(borrows)
        seed_reviews(reviews)
        
    print("🦸‍♂️ Done seeding!")
