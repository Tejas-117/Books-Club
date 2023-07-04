from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import Tag, UserImage
from books.models import Book, WishList, Image

class TagSerializer(serializers.ModelSerializer):
    """
    To serialize and deserialize 'interests/categories'.
    """

    class Meta:
        model = Tag
        fields = "__all__"


class UserImageSerializer(serializers.ModelSerializer):
    """
        Deserialize user-profile-images
    """

    class Meta:
        model = UserImage
        fields = '__all__'
        read_only_fields = ['id']


class UserSerializer(serializers.ModelSerializer):
    """
    To serialize and deserialize 'user' instances.
    """

    # Serialization: fields returned --> id, first_name, last_name
    # Deserialization: fields returned --> all fields except 'id', interests

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
            "gender",
            "date_of_birth",
            "bio"
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "email": {"required": True, "write_only": True},
            "password": {"write_only": True, "required": True},
            "gender": {"write_only": True},
            "date_of_birth": {"write_only": True},
            "profile_image": {"write_only": True},
            "cover_image": {"write_only": True},
        }

    def update(self, instance, validated_data):        
        updated_instance = super().update(instance, validated_data)

        password = self.validated_data.get('password', None)
        # set hashed password if present
        if password is not None:
            updated_instance.set_password(password)
            updated_instance.save()

        return updated_instance

#################################################################
# Added here to prevent circular dependency error
class BookImageSerializer(serializers.ModelSerializer):
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

class BookSerializer(serializers.ModelSerializer):
    """
    Serialize 'Book' rows with selected fields.
    """

    # Serialization: fields returned --> all book_fields, user(details), images
    images = BookImageSerializer(many=True, read_only=True)
    categories = TagSerializer(many=True)

    class Meta:
        model = Book
        fields = ["id", "user", "title", "description", "for_sale", "price", "author", "images", "categories"]
        read_only_fields = ["id"]

class WishListSerializer(serializers.ModelSerializer):
   """
      Serialize each wishlist item of the user.
   """

   user = UserSerializer()
   book = BookSerializer()

   class Meta:
      model = WishList
      fields = "__all__"

##################################################################

class GenderNameField(serializers.RelatedField):
    """
        Return name of gender.
    """
    def to_representation(self, value):
        return value.name

class UserDetailSerializer(serializers.ModelSerializer):
    """
        Serialize 'user' instance with necessary details.
    """
    # Serialization: fields returned --> id, first_name, last_name, user-images
    
    images = UserImageSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "first_name",
            "last_name",
            "images"
        ]

class CompleteUserDetailSerializer(serializers.ModelSerializer):
    """
    To serialize and deserialize 'user' instances with additional information.
    """

    # Serialization: fields returned --> id, name, phone, email, gender, dob, interests, books_uploaded, wishlist, profile-images.

    interests = TagSerializer(many=True, read_only=True)
    books = BookSerializer(many=True, read_only=True)
    wishlist = WishListSerializer(many=True, read_only=True)
    images = UserImageSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "first_name",
            "last_name",
            "gender",
            "date_of_birth",
            "interests",
            "books",
            "wishlist",
            "images",
            "bio"
        ]

# Custom JWToken Serializer
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        user_images = user.images.filter(type__exact='profile')

        # Add custom claims
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        
        # If user has profile image, add it to token
        if len(user_images):
            token['profile'] = user_images[0].url

        return token