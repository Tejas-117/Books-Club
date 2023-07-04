from rest_framework import serializers

from offers.models import Offer
from books.serializers import BookSerializer
from users.serializers import UserSerializer


class OfferPostSerializer(serializers.ModelSerializer):
    """
        Deserialize 'offer' data.
    """

    class Meta:
        model = Offer
        fields = "__all__"


class OfferRecievedSerializer(serializers.ModelSerializer):
    """
        Serialize 'Offer' instances.
    """

   # Serializer: fields returned: all fields with their details fetched.

    buyer = UserSerializer()
    posted_book = BookSerializer()
    exchange_book = BookSerializer()

    class Meta:
        model = Offer
        fields = "__all__"


class OfferPostedSerializer(serializers.ModelSerializer):
    """
    Serialize 'Offer' instances.
    """
    
   # Serializer: fields returned: all fields with their details fetched. Buyer info is replaced by seller info. 
   
    seller = serializers.SerializerMethodField("get_seller")
    posted_book = BookSerializer()
    exchange_book = BookSerializer()

    class Meta:
        model = Offer
        fields = ["posted_book", "exchange_book", "for_purchase", "price", "description", "seller", "status"]

    def get_seller(self, offer):
        seller_obj = offer.get_seller()
        seller = UserSerializer(seller_obj).data 
        return seller