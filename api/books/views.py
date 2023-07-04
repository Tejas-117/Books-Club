from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.parsers import MultiPartParser

from users.models import Tag
from books.models import Book, Image, WishList
from books.serializers import (
    BookSerializer,
    BookDetailSerializer,
    BookPostSerializer,
    ImageSerializer,
)
from api_config.utils.cloudinary_utils import (
    delete_image,
    delete_multiple_images,
    upload_multiple_book_images,
)


@api_view(["GET", "POST"])  # Allowed methods
@permission_classes(
    [IsAuthenticatedOrReadOnly]
)  # Allows POST only for authenticated users
@parser_classes([MultiPartParser])  # Parse 'multipart-formdata'
def books_controller(req):

    # GET all the books saved
    if req.method == "GET":
        books = Book.objects.prefetch_related(
            "categories", "user", "images", "comments"
        ).all()

        # if request is for particular user, send their books (uploads)
        for_user = req.query_params.get("user", "false")

        if for_user == "true":
            user_id = req.user.id
            books = books.filter(user__id=user_id, for_sale=False)

        # retrieve books --> serialize --> JSON response
        
        serializer = BookSerializer(books, many=True)
        return Response(data={"data": {"books": serializer.data}}, status=200)

    # POST a book (user should be authenticated)
    # accepts form-data
    elif req.method == "POST":
        # assign the user-id to the book in request-data object
        req.data._mutable = True
        req.data["user"] = req.user.id
        req.data._mutable = False

        # deserialize JSON data recieved
        book_serializer = BookPostSerializer(data=req.data)

        # if images are not uploaded, return error
        uploaded_images = req.data.getlist("images")
        if len(uploaded_images) == 0:
            return Response(data={'error': { 'message': 'Upload images of the book' }}, status=400)

        if book_serializer.is_valid():
            # save book to DB if serialized successfully. (valid data)
            book = book_serializer.save()

            # save all the categories associated with the book.
            categories_allowed = Tag.objects.filter(
                text__in=req.data.getlist("categories")
            )
            book.categories.add(*categories_allowed)

            # upload images posted with the book. (max 4)
            all_images = upload_multiple_book_images(
                uploaded_images, book, "book-images/"
            )

            # save image details to DB if serialized successfully.
            image_serializer = ImageSerializer(data=all_images, many=True)
            if image_serializer.is_valid():
                image_serializer.save()
            else:
                return Response(
                    data={"error": {'message': image_serializer.errors}},
                    status=500,
                )
            return Response(
                data={
                    "data": {
                        "message": "Successfully uploaded book",
                        "book_id": book.id,
                    }
                },
                status=200,
            )
        else:
            return Response(data={"error": {'message': book_serializer.errors}}, status=400)


@api_view(["GET", "PUT", "DELETE"])  # Allowed methods.
@permission_classes(
    [IsAuthenticated]
)
def book_controller(req, **kwargs):
    book_id = kwargs["book_id"]
    user = req.user

    # GET information of a single book
    if req.method == "GET":
        try:
            book = Book.objects.prefetch_related(
                "categories", "user", "comments", "images"
            ).get(pk=book_id)
            book_serializer = BookDetailSerializer(book)

            data = book_serializer.data

            # add if the book is present in the 'wishlist of the user'
            wishlist_qs = WishList.objects.prefetch_related('book', 'user')
            in_wishlist = wishlist_qs.filter(book__id=book_id, user__id=user.id)
            
            if in_wishlist:
                data['in_wishlist'] = True
            else:
                data['in_wishlist'] = False

            return Response(data={"data": {"book": data}}, status=200)
        except Book.DoesNotExist:
            return Response(
                data={"error": {"message": "Resource not found"}}, status=404
            )

    # UPDATE information of a book.
    # accepts form-data
    elif req.method == "PUT":
        try:
            MAX_IMAGES_PER_BOOK = 4

            # Check if the 'book' object exists.
            book = Book.objects.prefetch_related("user", "images").get(pk=book_id)
            number_of_images_stored = len(book.images.all())

            # If the 'book' owner is different from authenticated user, do not allow to update.
            if book.user.id != req.user.id:
                return Response(data={"error": { "message": "Forbidden" }}, status=403)

            # Get images to delete from request-data.
            images_to_delete = req.data.getlist("delete_images")
            number_of_images_to_delete = len(images_to_delete)

            # Delete images from DB.
            Image.objects.filter(
                Q(filename__in=images_to_delete), Q(book=book_id)
            ).delete()

            # Delete images from cloud.
            for image in images_to_delete:
                res = delete_image(image)

            # Get new images to save from request-data
            images_to_upload = req.data.getlist("images")
            number_of_images_to_save = min(
                MAX_IMAGES_PER_BOOK
                - (number_of_images_stored - number_of_images_to_delete),
                len(images_to_upload),
            )

            # Save new images to cloud
            all_images = upload_multiple_book_images(
                images_to_upload, book, "book-images/", number_of_images_to_save
            )

            # Save new images to DB if serialized successfully
            image_serializer = ImageSerializer(data=all_images, many=True)
            if image_serializer.is_valid():
                image_serializer.save()
            else:
                return Response(
                    data={"error": {"message": image_serializer.errors}},
                    status=500,
                )

            # Update all the 'categories' from the book
            book.categories.clear()  # remove existing categories
            new_categories = Tag.objects.filter(text__in=req.data.getlist("categories"))
            book.categories.add(*new_categories)

            # Update the book data in DB.
            book_serializer = BookPostSerializer(book, data=req.data, partial=True)
            if book_serializer.is_valid():
                book = book_serializer.save()
                return Response(
                    data={
                        "data": {
                            "message": "Successfully updated book.",
                            "book_id": book.id,
                        }
                    },
                    status=200,
                )
            else:
                return Response(
                    data={"error": {"message": book_serializer.errors}},
                    status=500,
                )

        except Book.DoesNotExist:
            return Response(
                data={"error": {"message": "Resource not found"}}, status=404
            )

    # DELETE a book.
    elif req.method == "DELETE":
        try:
            # Check if the 'book' is saved in DB.
            book_queryset = Book.objects.prefetch_related("comments", "images", "categories")
            book = book_queryset.get(pk=book_id)

            # If the 'book' owner is different from authenticated user, do not allow to delete.
            if book.user.id != req.user.id:
                return Response(data={"error": {"message": "Forbidden"}}, status=403)

            # Delete 'images' related to book from cloud.
            delete_multiple_images(book.images.all())

            # Delete 'book' from DB along with it 'comments', 'images'
            book_queryset.filter(pk=book_id).delete()

            return Response(
                data={"data": {"message": "Successfully deleted the book."}}, status=200
            )
        except Book.DoesNotExist:
            return Response(
                data={"error": {"message": "Resource not found"}}, status=404
            )

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def book_wishlist_controller(req, **kwargs):
    # get user and book
    user = req.user
    book_id = kwargs['book_id']

    # if the book does not exist return error
    book = get_object_or_404(Book, pk=book_id)

    # if the user is trying to add/delete own book from wishlist, return error.
    if book.user == user:
        return Response(data={'error': {'message': "Couldn't modify wishlist"}}, status=400)

    wishlist_qs = WishList.objects.all()

    try:
        # if book is already present in the wishlist remove it
        book_in_wishlist = wishlist_qs.get(Q(book=book_id), Q(user=user.id))
        wishlist_qs.filter(Q(book=book_id), Q(user=user.id)).delete()
        return Response(data={'data': {'message': 'Book removed from wishlist'} }, status=200)
    except:
        # if book is not present in the wishlist add it
        wishlist_qs.create(user=user, book=book)
        return Response(data={'data': {'message': 'Book added to wishlist'}}, status=200)