from api_config.cloudinary_config import *

# Utilty functions to work with cloudinary
def upload_image(image, folder_name):
    """
      Upload a single 'image' to cloud under 'folder_name'.
      
      Params:
        image --> single 'image' to upload
        folder_name --> folder under which 'image' is stored in cloud
    """
    

    res = cloudinary.uploader.upload(
        image, **cloudinary_media_upload_options, folder="books-api/" + folder_name
    )
    return res


def upload_multiple_book_images(images, book, folder_name, number_of_images_to_upload=4):
    """
     Upload multiple 'images' to cloud under 'folder_name'.
     
     Params:
        images --> list of images (type: list of 'bytes')
        book --> book to which 'images' belong
        folder_name --> folder under which 'images' are stored in cloud
        number_of_images_to_upload --> number of images allowed to upload to cloud
    """

    allImages = []
    for image in images[:number_of_images_to_upload]:
        # upload each image to cloud.
        image_upload_response = upload_image(image, folder_name)
        imageData = {
            "book": book.id,
            "url": image_upload_response["secure_url"],
            "filename": image_upload_response["public_id"],
        }
        allImages.append(imageData)
    return allImages

def delete_image(public_id):
    """
       Delete a 'image' from cloud with 'public_id'

       Params:
         public_id --> i.e., 'filename' of the image to identify it uniquely.
    """
    res = cloudinary.uploader.destroy(public_id)
    return res

def delete_multiple_images(images):
    """
       Delete multiple 'images' from cloud.

       Params:
         images --> list of 'Image' object to delete images from cloud and DB.
    """
    
    for image in images:
        delete_image(image.filename)