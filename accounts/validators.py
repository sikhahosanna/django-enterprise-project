from django.core.exceptions import ValidationError
from PIL import Image


def validate_image_file(image):
    """
    Validate uploaded image files.

    Validates:
    - Filename
    - File type
    - File size
    - Actual image content
    """

    if not image.name:
        raise ValidationError(
            "Filename is required."
        )

    allowed_types = [
        "image/jpeg",
        "image/png",
        "image/jpg",
    ]

    if image.content_type not in allowed_types:
        raise ValidationError(
            "Only JPG, JPEG and PNG files are allowed."
        )

    if image.size > 5 * 1024 * 1024:
        raise ValidationError(
            "Image size should be less than 5MB."
        )

    try:
        image.seek(0)

        img = Image.open(image)
        img.verify()

    except Exception:
        raise ValidationError(
            "Invalid image file."
        )

    finally:
        image.seek(0)

    return image


def validate_image_upload(image):
    """
    Validate basic image upload requirements.

    Validates:
    - Filename
    - File type
    - File size
    """

    if not image.name:
        raise ValidationError(
            "Filename is required."
        )

    allowed_types = [
        "image/jpeg",
        "image/jpg",
        "image/png",
    ]

    if image.content_type not in allowed_types:
        raise ValidationError(
            "Only JPG, JPEG and PNG files are allowed."
        )

    if image.size > 5 * 1024 * 1024:
        raise ValidationError(
            "Image size should be less than 5MB."
        )

    return image


def validate_required(value, field_name):
    """
    Validate that a required value is provided.
    """

    if value is None or str(value).strip() == "":
        raise ValidationError(
            f"{field_name} is required."
        )

    return value


def validate_positive_amount(value):
    """
    Validate that an amount is greater than zero.
    """

    if value is None or value <= 0:
        raise ValidationError(
            "Amount must be greater than zero."
        )

    return value


def validate_status(value, allowed_statuses):
    """
    Validate that a status belongs to the allowed status list.
    """

    if value not in allowed_statuses:
        raise ValidationError(
            f"Invalid status: {value}"
        )

    return value