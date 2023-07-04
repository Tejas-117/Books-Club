from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models

from users.models import User
from books.models import Book


class Offer(models.Model):
    # Buyer interested in the book
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer")

    # Book for sale/exchange.
    posted_book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="posted_book"
    )

    # Book made as an offer for exchange.
    exchange_book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="exchange_book", null=True
    )

    # If book was for sale, price offered.
    for_purchase = models.BooleanField(default=False)  # by default books are exchanged
    price = models.DecimalField(
        max_digits=7, decimal_places=2, default=00.00
    )  # since books are exchanged price=0

    # Description of the offer (optional)
    description = models.CharField(max_length=150, blank=True)

    # Trade status
    status = models.CharField(max_length=100, default="processing")

    # Timestamps
    created_on = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    class Meta:
        db_table = "offers"
        constraints = [
            models.CheckConstraint(
                check=models.Q(status__in=["processing", "rejected", "accepted"]),
                name="possible_offer_status",
            )
        ]

    # return seller of the book
    def get_seller(self):
        return self.posted_book.user
