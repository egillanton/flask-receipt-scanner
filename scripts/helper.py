import base64
from werkzeug.utils import secure_filename

# Allowed extensions for the incoming payload
ALLOWED_IMAGE_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
ALLOWED_OTHER_EXTENSIONS = set(['pdf'])
ALLOWED_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS.union(ALLOWED_OTHER_EXTENSIONS)


def is_valid_file_type(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def is_image(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


def convert_and_save_base64(b64_string, file_name):
    """
    Convert base64 string to image and save
    """
    try:
        with open(file_name, "wb") as fh:
            fh.write(base64.decodebytes(b64_string.encode()))
    except:
        print('Unable to save image')


def file2img(file_path):
    image_path = ''
    # TODO: Check file extension
    # Import for example a pdf to image converting library and use
    return image_path
