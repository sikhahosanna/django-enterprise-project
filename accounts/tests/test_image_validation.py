from io import BytesIO

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase
from PIL import Image

from accounts.validators import validate_image_file


class ImageValidationTests(SimpleTestCase):

    def make_png_upload(self):
        buffer = BytesIO()
        Image.new("RGB", (2, 2), color="red").save(
            buffer, format="PNG"
        )
        return SimpleUploadedFile(
            "valid.png",
            buffer.getvalue(),
            content_type="image/png",
        )

    def test_valid_png_is_accepted(self):
        upload = self.make_png_upload()
        result = validate_image_file(upload)
        self.assertIs(result, upload)

    def test_corrupted_image_is_rejected(self):
        upload = SimpleUploadedFile(
            "broken.png",
            b"not a real image",
            content_type="image/png",
        )
        with self.assertRaises(ValidationError):
            validate_image_file(upload)

    def test_unsupported_mime_type_is_rejected(self):
        upload = SimpleUploadedFile(
            "image.gif",
            b"GIF89a",
            content_type="image/gif",
        )
        with self.assertRaises(ValidationError):
            validate_image_file(upload)

    def test_file_over_5mb_is_rejected(self):
        upload = SimpleUploadedFile(
            "large.png",
            b"x" * (5 * 1024 * 1024 + 1),
            content_type="image/png",
        )
        with self.assertRaises(ValidationError):
            validate_image_file(upload)
