import cloudinary
import os

# Developers must set the relevant environment variables for
# testing locally. For reference:

# Windows:          set SOME_VAR=somevalue
# Mac:              export SOME_VAR=somevalue

'''Configures cloudinary with Matt's account information.
Must run in files that use Cloudinary API, BEFORE
import cloudinary.uploader'''


def config_cloudinary():
    cloudinary.config(
        secure=True,
        cloud_name=os.environ.get('CLOUD_NAME'),
        api_key=os.environ.get('API_KEY'),
        api_secret=os.environ.get('API_SECRET'),
    )
