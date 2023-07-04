from django.core.mail import send_mail
from decouple import config

creds = {
   "email" : "thebookclub.team@gmail.com",
   "password" : "hkjaugfwmhwfjfpp"
}

email_status = send_mail(
   subject = "Testing the google account",
   message = "Hey there from booksclub support team",
   from_email=creds["email"],
   recipient_list = ['tejascs84@gmail.com', 'tejasftw117@gmail.com']
)

print(email_status)