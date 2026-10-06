class LibraryError(Exception):
    """Базовое исключение библиотеки фильмов."""
    pass


class FilmNotFoundError(LibraryError):
    """Фильм не найден."""
    pass


class DuplicateFilmError(LibraryError):
    """Фильм с таким ID уже существует."""
    pass


class InvalidRatingError(LibraryError):
    """Некорректная оценка фильма."""
    pass


class InvalidFilmDataError(LibraryError):
    """Некорректные данные фильма."""
    pass
