from django.db import models

from users.models import User, Tag

class Book(models.Model):
    """
    Model that represent 'books'.
    """

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="books")

    # details of the book.
    title = models.CharField(max_length=120)
    author = models.CharField(max_length=30, null=True)
    description = models.TextField()
    isbn = models.TextField(null=True)
    publisher = models.CharField(max_length=30, null=True)
    categories = models.ManyToManyField(Tag, related_name="categories")

    # details of selling book.
    for_sale = models.BooleanField(default=0)  # default: the book is not for sale
    price = models.DecimalField(
        max_digits=7, decimal_places=2, default=00.00
    )  # default: the price is 00.00

    # location details of the book.
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=40)
    state = models.CharField(max_length=40)
    country = models.CharField(max_length=40)

    # timestamps
    created_on = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    class Meta:
        db_table = "books"
        constraints = [
            models.CheckConstraint(check=~models.Q(title=""), name="non_empty_title"),
            models.CheckConstraint(
                check=~models.Q(description=""), name="non_empty_description"
            ),
            models.CheckConstraint(
                check=~models.Q(address=""), name="non_empty_address"
            ),
            models.CheckConstraint(check=~models.Q(city=""), name="non_empty_city"),
            models.CheckConstraint(check=~models.Q(state=""), name="non_empty_state"),
            models.CheckConstraint(
                check=~models.Q(country=""), name="non_empty_country"
            ),
        ]

    def __str__(self) -> str:
        return self.title


class Image(models.Model):
    """
    Images of the book model.
    """

    id = models.BigAutoField(primary_key=True)
    book = models.ForeignKey(Book, related_name="images", on_delete=models.CASCADE)
    url = models.TextField(default=None)
    filename = models.TextField(default=None)

    class Meta:
        db_table = "book_images"
        constraints = [
            models.CheckConstraint(check=~models.Q(url=""), name="non_empty_url"),
            models.CheckConstraint(
                check=~models.Q(filename=""), name="non_empty_filename"
            ),
        ]


class WishList(models.Model):
    """
        Wishlist of the user.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_wishlist"