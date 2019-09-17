import tempfile
from django.test import override_settings
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model
from .models import Product
from faker import Factory
import uuid
import random
import io
from PIL import Image
from django.core.files import File

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler  = api_settings.JWT_ENCODE_HANDLER
User = get_user_model()
faker = Factory.create()

admin_user_password = uuid.uuid4()
MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(
    MEDIA_ROOT=MEDIA_ROOT,
    # FILE_UPLOAD_HANDLERS=TemporaryFileUploadHandler
)
class MarketAPITestCaseSetUp( APITestCase ):

    def setUp( self ):
        self.create_users( 5 )
        self.create_products( 100 )

    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = f"{ faker.word() }.png"
        file.seek(0)
        return File(file)

    def login_user( self ):
        user_obj = User.objects.first()
        payload = payload_handler( user_obj )
        token_rsp = encode_handler( payload )
        self.client.credentials( HTTP_AUTHORIZATION='JWT ' + token_rsp )

    def create_users( self, amount ):
        for _ in range( amount ):
            user = User( username=faker.name(), email=faker.email(), first_name=faker.name() )
            user.set_password( admin_user_password )
            user.save()

    def create_products(self, amount):
        users = User.objects.all()
        for _ in range( amount ):
            product = Product(
                user=random.choice( users ),
                title=faker.text()[:50] if len( faker.text() ) > 50 else faker.text(),
                description=faker.text()[:100] if len( faker.text() ) > 100 else faker.text(),
                features=faker.text()[:100] if len(faker.text()) > 100 else faker.text(),
                img=self.generate_photo_file(), )
            product.save()


def test_case_overview( func ):
    def wrapper( *args, **kwargs ):
        fname = func.__name__
        print( f'\n=== TESTCASE [{ fname.upper() }]' )
        func( *args, **kwargs )
        print(f'=== TESTCASE END [{ fname.upper() }]')

    return wrapper

