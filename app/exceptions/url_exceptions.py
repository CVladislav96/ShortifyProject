class ShortnerBaseError(Exception):
    pass


class NoLongUrlFoundError(ShortnerBaseError):
    pass


class SlugAlreadyExistsError(ShortnerBaseError):
    pass
