import validators


def validate(check_url):
    errors = []
    if not check_url:
        errors.append("URL не должен быть пустым")
    if not validators.url(check_url):
        errors.append("URL некорректный")
    if len(check_url) > 255:
        errors.append("URL превышает 255 символов")
    return errors