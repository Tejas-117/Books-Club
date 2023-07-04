from books.models import Book, Image
from rest_framework import serializers

from users.serializers import TagSerializer, UserSerializer, UserDetailSerializer
from comments.serializers import CommentDetailSerializer


class ImageSerializer(serializers.ModelSerializer):
    """
    Serialize and Deserialize 'Image' of the books.
    """

    # Serialization: fields returned --> id, url, filename
    # Deserialization: fields retrieved --> book(book_id) , url, filename

    class Meta:
        model = Image
        fields = ["id", "book", "url", "filename"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "book": {"write_only": True, "required": True},
            "url": {"required": True},
            "filename": {"required": True},
        }

class BookDetailSerializer(serializers.ModelSerializer):
    """
    Serialize 'Book' rows with all fields.
    """

    # Serialization: fields returned --> all book_fields, user(details), images, comments(details) and categories

    user = UserDetailSerializer()
    images = ImageSerializer(many=True, read_only=True)
    comments = CommentDetailSerializer(many=True, read_only=True)
    categories = TagSerializer(many=True)

    class Meta:
        model = Book
        fields = "__all__"

class BookPostSerializer(serializers.ModelSerializer):
    """
    Deserialize 'Book'.
    """

    # Deserialization: fields retrieved --> all book_fields except categories

    class Meta:
        model = Book
        fields = [
            "user",
            "title",
            "description",
            "isbn",
            "author",
            "publisher",
            "for_sale",
            "price",
            "address",
            "city",
            "state",
            "country",
        ]

class BookSerializer(serializers.ModelSerializer):
    """
    Serialize 'Book' rows with selected fields.
    """

    # Serialization: fields returned --> all book_fields, user(details), book-images
    images = ImageSerializer(many=True, read_only=True)
    user = UserDetailSerializer()

    class Meta:
        model = Book
        fields = ["id", "user", "title", "description", "for_sale", "price", "images", "author", "created_on"]
        read_only_fields = ["id"]