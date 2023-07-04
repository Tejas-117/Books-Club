from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import Tag, User
from users.serializers import CompleteUserDetailSerializer, UserImageSerializer, UserSerializer, MyTokenObtainPairSerializer
from api_config.utils.cloudinary_utils import delete_image, upload_image


@api_view(["POST"])
@parser_classes([MultiPartParser])
def register(req):
    """
        Get user details, and create user if the user doesn't exist.
    """

    # check if the user already exists based on email
    # accepts form-data
    try:
        userFromDB = get_user_model().objects.get(
            email__exact=req.data.get("email", None)
        )
        return Response(status=400, data={"error": {"message": "User already exists"}})
    except User.DoesNotExist:
        pass

    user_serializer = UserSerializer(data=req.data)

    # if the data is serialized successfully, save the user and send response
    if user_serializer.is_valid():
        user = get_user_model().objects.create_user(**user_serializer.validated_data)
       
        # upload user profile & cover images.
        uploaded_profile_image = req.data.get("profile_image", None)
        uploaded_cover_image = req.data.get("cover_image", None)
        imagesList = []

        # Format images to save it in data.
        if uploaded_profile_image is not None:
            profile_image = upload_image(req.data.get("profile_image", None), "user-images/")
            profile_image['user'] = user.id
            profile_image['filename'] = profile_image['public_id']
            profile_image['type'] = 'profile'
            imagesList.append(profile_image)
        
        if uploaded_cover_image is not None:
            cover_image = upload_image(req.data.get("cover_image", None), "user-images/")
            cover_image['user'] = user.id
            cover_image['filename'] = cover_image['public_id']
            cover_image['type'] = 'cover'
            imagesList.append(cover_image)


        # serialize images and save to DB.
        user_image_serializer = UserImageSerializer(data=imagesList, many=True)
        if user_image_serializer.is_valid():
            user_image_serializer.save()      

        # get user interests and save it.
        user_interests = req.data.getlist("interests", None)
        if user_interests is not None:
            allowed_interests = Tag.objects.filter(text__in=user_interests)
            user.interests.add(*allowed_interests)

        return Response(data={"message": "User successfully registered"}, status=200)
    return Response(status=400, data={"error": {"message": user_serializer.errors}})

# Get user profile
@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def user_controller(req, **kwargs):
    # get user id
    user_id = kwargs['user_id']

    # get corresponding user, return error if not found
    user_qs = User.objects.prefetch_related("books", "interests", "wishlist", "images")
    user = get_object_or_404(user_qs, pk=user_id) 
    
    # Get user profile.
    if req.method == 'GET':
        user_serializer = CompleteUserDetailSerializer(user)
        return Response({'data': user_serializer.data })

    # Edit user profile.
    elif req.method == 'PUT':
        # Only same user can edit their profile
        if user_id != req.user.id:
            return Response(data={ 'error': {"message": 'Unauthorized'} }, status=401)

        user_serializer = UserSerializer(user, data=req.data, partial=True)

        if user_serializer.is_valid():
            user = user_serializer.save()

            # get uploaded user profile & cover images.
            uploaded_profile_image = req.data.get("profile_image", None)
            uploaded_cover_image = req.data.get("cover_image", None)
            imagesList = []

            # If user decides to delete profile image and cover image (or) uploads new images, delete old images.
            if (req.data.get('delete_profile_image', '') in ['True', 'true', 1, '1']) or uploaded_profile_image:
                a = user.images.filter(type__exact = 'profile')
                if len(a) > 0:
                    delete_image(a[0].filename)
                    a.delete()
            if (req.data.get('delete_cover_image', '') in ['True', 'true', 1, '1']) or uploaded_cover_image:
                b = user.images.filter(type__exact = 'cover')
                if len(b) > 0:
                    delete_image(b[0].filename)
                    b.delete()

            # If new profile image is uploaded, replace with new image.
            if uploaded_profile_image is not None:
                profile_image = upload_image(req.data.get("profile_image", None), "user-images/")
                profile_image['user'] = user.id
                profile_image['filename'] = profile_image['public_id']
                profile_image['type'] = 'profile'
                imagesList.append(profile_image)
            
            # If new cover image is uploaded, replace with new image.
            if uploaded_cover_image is not None:
                cover_image = upload_image(req.data.get("cover_image", None), "user-images/")
                cover_image['user'] = user.id
                cover_image['filename'] = cover_image['public_id']
                cover_image['type'] = 'cover'
                imagesList.append(cover_image) 


            # serialize images and save to DB.
            user_image_serializer = UserImageSerializer(data=imagesList, many=True)
            if user_image_serializer.is_valid():
                user_image_serializer.save()

            # Get user interests and save it.
            user_interests = req.data.getlist("interests", None)
            user.interests.clear()
            if user_interests is not None:
                allowed_interests = Tag.objects.filter(text__in = user_interests)
                user.interests.add(*allowed_interests)


            return Response(data={"data" :{"message": "User successfully updated"}}, status=200)
        return Response(status=400, data={"error": {"message": user_serializer.errors}})


# Custom JWToken view
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer