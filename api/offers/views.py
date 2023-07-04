from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from books.models import Book
from offers.models import Offer
from offers.serializers import (
    OfferPostedSerializer,
    OfferRecievedSerializer,
    OfferPostSerializer,
)

from api_config.utils.send_email import send_email

@api_view(["GET", "POST"])
# @permission_classes([IsAuthenticated])
def offers_controller(req):
    # authenticated user
    user = req.user

    # GET all the offers associated with the user
    if req.method == "GET":
        get_received_offers = req.query_params.get("received", "false")

        offer_queryset = Offer.objects.prefetch_related(
            "buyer", "posted_book", "exchange_book"
        )

        # GET all offers received by the user.
        if get_received_offers == "true":
            received_offers = offer_queryset.filter(posted_book__user=user.id)

            # serialize retrieved data and send a response
            offers_serializer = OfferRecievedSerializer(received_offers, many=True)
            return Response(
                data={"data": {"offers": offers_serializer.data}}, status=200
            )

        # GET all offers posted by the user.
        else:
            posted_offers = offer_queryset.filter(buyer=user.id)

            # serialize retrieved data and send a response
            offers_serializer = OfferPostedSerializer(posted_offers, many=True)
            return Response(
                data={"data": {"offers": offers_serializer.data}}, status=200
            )

    # POST a offer based on sale/exchange status.
    elif req.method == "POST":
        book_queryset = Book.objects.all()
        req.data["buyer"] = user.id

        # get posted_book details, send error message if not found.
        posted_book = get_object_or_404(
            book_queryset, pk=req.data.get("posted_book", -1)
        )

        # If the buyer == seller, return error
        if user == posted_book.user:
            return Response(
                data={"error": {"message": "Buyer and seller are same, couldn't continue"}},
                status=400,
            )

        # A user can only make one offer to a book.
        previously_made_offers = Offer.objects.filter(
            Q(buyer=user.id), Q(posted_book=posted_book.id)
        )
        if previously_made_offers.count() > 0:
            return Response(
                data={"data": {"message": "Already posted a offer"}}, status=200
            )

        # check sale/exchange status of the posted book.

        # if the book is for sale
        if posted_book.for_sale:
            req.data.pop("exchange_book", None)

            # check if the buyer is trying to buy AND with appropriate price
            if (req.data.get("for_purchase", False)) and (
                req.data.get("price", -1) >= posted_book.price
            ) or (posted_book.price == 0):
                # save offer to DB
                offers_serializer = OfferPostSerializer(data=req.data)
                if offers_serializer.is_valid():
                    offers_serializer.save()
                    return Response(
                        data={"data": {"message": "Successfully saved offer"}},
                        status=200,
                    )
                return Response(data={"error": {"message": offers_serializer.errors}}, status=400)
            else:
                return Response(
                    {"error": {"message": "Couldn't make offer"}}, status=400
                )

        # if the book is for exchange
        else:
            # default values for exchange
            req.data.pop("price", None)
            req.data.pop("for_purchase", None)

            # get exchange_book details, send error message if not found.
            exchange_book_id = req.data.get("exchange_book", -1)
            if exchange_book_id == -1:
                return Response(
                    data={
                        "error": {
                            "message": "Book is for exchange and exchange book not found"
                        }
                    },
                    status=404,
                )

            exchange_book = get_object_or_404(book_queryset, pk=exchange_book_id)

            # if both books are not for exchange OR
            # if exchange_book doesn't belong to the buyer return error.
            if (exchange_book.for_sale != posted_book.for_sale) or (
                exchange_book.user != user
            ):
                return Response({"error": {"message": "Couldn't make offer"}}, status=400)
            else:
                # save offer to DB
                offers_serializer = OfferPostSerializer(data=req.data)
                if offers_serializer.is_valid():
                    offers_serializer.save()
                    return Response(
                        data={"data": {"message": "Successfully saved offer"}},
                        status=200,
                    )
                return Response(data={"error": {"message": offers_serializer.errors}}, status=400)


@api_view(["DELETE", "PUT"])
@permission_classes([IsAuthenticated])
def offer_controller(req, offer_id):
    # authenticated user
    user = req.user

    # 'Offer' Queryset and the relevant offer
    offer_qs = Offer.objects.prefetch_related(
        "buyer", "posted_book", "exchange_book"
    ).all()
    offer = get_object_or_404(offer_qs, pk=offer_id)

    # DELETE a offer
    if req.method == "DELETE":
        # Only a seller or buyer can delete the offer
        if (offer.get_seller().id != user.id) and (offer.buyer.id != user.id):
            return Response(data={"error": {"message": "Forbidden"}}, status=403)
        offer.delete()
        return Response(
            data={"error": {"message": "Successfully deleted offer"}}, status=200
        )

    # UPDATE a offer
    elif req.method == "PUT":
        # Only seller can modify the offer
        if offer.get_seller().id != user.id:
            return Response(data={"error": {"message": "Forbidden"}}, status=403)

        # Seller can only change the status of the book.
        for key in list(req.data.keys()):
            if key != "status":
                del req.data[key]

        # Serialize the updated data and save if valid.
        offer_serializer = OfferPostSerializer(offer, data=req.data, partial=True)

        if offer_serializer.is_valid():
            updated_offer = offer_serializer.save()

            # update both seller and buyer about the offer status
            # send email to 'seller'.
            send_email(offer.posted_book, user, offer.buyer, 'seller', offer.status)
            # send email to 'buyer'
            send_email(offer.posted_book, user, offer.buyer, 'buyer', offer.status)

            return Response(
                data={"data": {"message": "Offer updated successfully", "status": updated_offer.status}}, status=200
            )
        return Response(data={"error": {"message": offer_serializer.errors}}, status=400)
