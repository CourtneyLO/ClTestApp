import factory
from faker import Faker
from django.core.files.uploadedfile import SimpleUploadedFile

from users.models import UserModel


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserModel

    name = factory.Faker('first_name')
    username = factory.Faker('first_name')
    profile_picture = SimpleUploadedFile("test_image.jpg", b"")
