from decouple import config
import cloudinary

# Cloudinary credentials
cloudinary_config = cloudinary.config(
    cloud_name = config("CLOUDINARY_CLOUD_NAME"),
    api_key = config("CLOUDINARY_API_KEY"),
    api_secret = config("CLOUDINARY_API_SECRET_KEY"),
)

# Cloudinary media upload options
cloudinary_media_upload_options = {
    "unique_filename": True,
    "resource_type": "auto",
}

import cloudinary.uploader
import cloudinary.api
