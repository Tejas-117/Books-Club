from django.core.mail import send_mail
from decouple import config

def get_email_body(book, seller, buyer, user_type, status):
   """
      Get email body based on user_type and status
   """
   
   if user_type == 'seller':
      email_body = f'You {status} offer from \'{buyer.first_name + " " + buyer.last_name}\' for book \'{book.title}\'. \n'

      # if offer is accepted, then add buyer details
      if status == 'accepted':
         email_body = email_body + f'Buyer email: {buyer.email}.'
      return email_body
   else:
      email_body = f'Your book offer for \'{book.title}\' is {status} by \'{seller.first_name + " " + seller.last_name}\'. \n'

      # if offer is accepted, then add seller details
      if status == 'accepted':
         email_body = email_body + f'Seller email: {seller.email}'
      return email_body

def send_email(book, seller, buyer, user_type, status):
   recipient = buyer
   if user_type == 'seller':
      recipient = seller

   email_status = send_mail(
      subject = 'Status of book offer',
      message = get_email_body(book, seller, buyer, user_type, status),
      from_email = config('EMAIL_USER'), 
      recipient_list = [recipient.email],
      fail_silently = False
   )

   return email_status