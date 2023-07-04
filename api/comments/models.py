from django.db import models

from users.models import User
from books.models import Book


class Comment(models.Model):
    """
    Comments of the book
    """

    id = models.BigAutoField(primary_key=True)
    book = models.ForeignKey(Book, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # comment on the book by any user
    comment = models.CharField(max_length=300)

    # timestamps
    created_on = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    class Meta:
        db_table = "book_comments"
        constraints = [
            models.CheckConstraint(
                check=~models.Q(comment=""), name="non_empty_comment_body"
            ),
        ]
