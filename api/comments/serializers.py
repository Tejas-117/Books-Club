from rest_framework import serializers

from comments.models import Comment
from users.serializers import UserDetailSerializer


class CommentDetailSerializer(serializers.ModelSerializer):
    """
    Serialize 'Comment' of the books.
    """

    # Serialization: fields returned --> id, comment, user(details)

    user = UserDetailSerializer()

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["id"]


class CommentPostSerializer(serializers.ModelSerializer):
    """
    Deserialize 'Comment'.
    """

    # Deserialization: fields retrieved -->  comment, user(user_id), book(book_id)

    class Meta:
        model = Comment
        fields = ["comment", "book", "user"]
        extra_kwargs = {"book": {"required": True}, "user": {"required": True}}
