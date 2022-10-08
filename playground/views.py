import requests
from django.core.mail import EmailMessage, BadHeaderError
from django.shortcuts import render
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from templated_mail.mail import BaseEmailMessage
from rest_framework.views import APIView
from .tasks import notify_customers

# Below is using cahce view
# decorator for implemeting caching


class HelloView(APIView):
    @method_decorator(cache_page(5 * 60))
    def get(self, request):
        response = requests.get('http://httpbin.org/delay/2')
        data = response.json()
        return render(request, 'hello.html', {'name': 'EYR'})


# @cache_page(5 * 60)
# def say_hello(request):

    # try:
    # Sending normal emails
    # send_mail('subj', 'msg', 'from: info@dsm.com', ['esther@dsm.com'])

    # Mailing site admins
    # mail_admins('subject', 'raw message', html_message='html message')

    # Using the EmailMessage() class
    # EmailMessage class gives you more control
    # You can add cc, bcc attach files etc.
    # email = EmailMessage('Subject', "Body", 'eyr@dsm.com',
    #                      ['esther@dsm.com'])
    # email.attach_file('playground/static/images/logo.png')
    # email.send()

    # ///// USING TEMPLATED EMAILS //////
    #     message = BaseEmailMessage(
    #         template_name='emails/mail.html',
    #         context={'name': 'Eyram'}
    #     )
    #     message.send(['esther@dsm.com'])
    # except BadHeaderError:
    #     pass

    # //// RUNNING CELERY TASKS
    # notify_customers.delay('Hello')

    # //////// Simulating a slow service /////////////////
    # requests.get('http://httpbin.org/delay/2')

    # /////// Implementing cachine ////////////////////////////
    # response = requests.get('http://httpbin.org/delay/2')
    # data = response.json()
    # return render(request, 'hello.html', {'name': 'EYR'})
