from celery import shared_task
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


@shared_task
def create_appointment_mail(visitor_name,client_email,date,gm,additional_visitors,subject,message):
    try:
        from_email = "mastikipathshala828109@gmail.com"
        
        # Correct template_path and render the HTML template with the provided data
        template_path = 'mail_templates/appointment-confirmation-email.html'
        context = {
            'visitor_name': visitor_name,
            'message':message,
            'client_email':client_email,
            'date':date,
            'gm':gm,
            'additional_visitors':additional_visitors,
        }
        
        # Render the HTML template to a string
        message = render_to_string(template_path, context)
        
        to = client_email
        
        # Create an email message object and attach the HTML message
        msg = EmailMultiAlternatives(subject, '', from_email, [to])
        msg.attach_alternative(message, 'text/html')
        try:
            msg.send()
        except Exception as e:
            print("Error sending email:", e)
            raise Exception("Problem sending email check password")
        
    except Exception as e:
        print("Error sending email:", e)
        raise Exception("Problem sending email")

