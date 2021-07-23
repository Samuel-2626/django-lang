from django.core.management.base import BaseCommand

from ...models import Course


class Command(BaseCommand):
    help = 'Add courses to the Database'

    def handle(self, *args, **options):

        for _ in range(5):
            if _ == 0:
                Course.objects.create(
                    title='Test-Driven Development with Python, Flask, and Docker',
                    description='In this course, you\'ll learn how to set up a development environment with Docker in order to build and deploy a microservice powered by Python and Flask. You\'ll also apply the practices of Test-Driven Development with pytest as you develop a RESTful API.',
                    date='2021-07-17',
                    price=30.00
                )
            elif _ == 1:
                Course.objects.create(
                    title='Building Your Own Python Web Framework',
                    description='In this course, you\'ll learn how to develop your own Python web framework to see how all the magic works beneath the scenes in Flask, Django, and the other Python-based web frameworks.',
                    date='2021-03-02',
                    price=25.00
                )
            elif _ == 2:
                Course.objects.create(
                    title='Developing a Real-Time Taxi App with Django Channels and Angular',
                    description='Learn how to create a ride-sharing app with Django Channels, Angular, and Docker. Along the way, you\'ll learn how to manage client/server communication with Django Channels, control flow and routing with Angular, and build a RESTful API with Django REST Framework.',
                    date='2020-12-17',
                    price=40.00
                )
            elif _ == 3:
                Course.objects.create(
                    title='Learn Vue by Building and Deploying a CRUD App',
                    description='This course is focused on teaching the fundamentals of Vue by building and testing a web application using Test-Driven Development (TDD).',
                    date='2021-06-28',
                    price=40.00
                )
            else:
                Course.objects.create(
                    title='The Definitive Guide to Celery and Django',
                    description='Learn how to add Celery to a Django application to provide asynchronous task processing.',
                    date='2021-04-05',
                    price=30.00
                )

        print('Completed!!! Check your database.')


""" Source: from TestDriven.io """
