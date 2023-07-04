from cmath import log
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from books.models import Book
from comments.serializers import CommentPostSerializer
from comments.models import Comment


@api_view(["POST"])  # Allowed HTTP methods.
@permission_classes([IsAuthenticated])  # Required permissions.
def comment_post_controller(req, *args, **kwargs):
    book_id = kwargs["book_id"]

    # POST a comment to book.
    if req.method == "POST":
        # Check if the book is in the DB.
        try:
            book = Book.objects.get(pk=book_id)

            # Assign 'book_id' and 'user_id' to the comment
            req.data["book"] = book.id
            req.data["user"] = req.user.id

            if len(req.data['comment']) == 0:
                return Response(data={"error": {"message": "Comment can't be empty" }}, status=400)

            # Serialize the 'comment' and save if valid
            comment_serializer = CommentPostSerializer(data=req.data)

            if comment_serializer.is_valid():
                comment_serializer.save()
                return Response(
                    data={"data": {"message": "Successfully posted comment"}},
                    status=200,
                )
            else:
                return Response(data={"error": {"message": comment_serializer.errors}}, status=400)

        except (Book.DoesNotExist, KeyError):
            return Response(data={"error": {"message": "Resource not found."}}, status=404)


@api_view(["DELETE", "PUT"])
@permission_classes([IsAuthenticated])
def comment_update_controller(req, book_id, comment_id):
    # DELETE a comment to book.
    comment = Comment.objects.filter(pk=comment_id)

    # If comment is not found return the error.
    if comment.first() is None:
        return Response(data={"error": {"message": "Resource not found"}}, status=404)

    # If the comment was not posted by the authenticated user,  don't delete/update the comment.
    if comment.first().user.id != req.user.id:
        return Response(data={"error": {"message": "Forbidden"}}, status=403)

    if req.method == "DELETE":
        # Delete the comment.
        comment.delete()
        return Response(
            data={"data": {"message": "Successfully deleted comment"}}, status=200
        )

    elif req.method == "PUT":
        comment_serializer = CommentPostSerializer(
            comment.first(), data=req.data, partial=True
        )

        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(
                data={
                    "data": {
                        "message": "Successfully updated comment",
                        "comment_id": comment_id,
                    }
                },
                status=200,
            )
        return Response(data={"error": {"message": comment_serializer.errors}}, status=400)
