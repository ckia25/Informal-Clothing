import cloudinary
import cloudinary.api
from config import config_cloudinary

def main():
    config_cloudinary()
    cloudinary.api.delete_all_resources()

if __name__ == '__main__':
    main()