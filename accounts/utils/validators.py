def validate_required_fields(
    data,
    required_fields,
):
    for field in required_fields:

        if field not in data or data.get(field) is None:
            return f"{field} is required."

    return None


def validate_coordinates(
    latitude,
    longitude,
):
    try:
        latitude = float(latitude)
        longitude = float(longitude)

    except (ValueError, TypeError):
        return False

    if not -90 <= latitude <= 90:
        return False

    if not -180 <= longitude <= 180:
        return False

    return True
