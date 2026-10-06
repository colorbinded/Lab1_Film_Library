from exceptions import InvalidFilmDataError, InvalidRatingError


class Country:
    def __init__(self, country_id: int, name: str):
        self.id = country_id
        self.name = name

    def get_name(self) -> str:
        return self.name


class Genre:
    def __init__(self, genre_id: int, name: str, description: str):
        self.id = genre_id
        self.name = name
        self.description = description

    def get_info(self) -> str:
        return f"{self.name}: {self.description}"


class Director:
    def __init__(
            self,
            director_id: int,
            name: str,
            birth_year: int,
            country: Country
    ):
        self.id = director_id
        self.name = name
        self.birth_year = birth_year
        self.country = country

    def get_info(self) -> str:
        return f"{self.name}, {self.birth_year}"


class Actor:
    def __init__(
            self,
            actor_id: int,
            name: str,
            birth_year: int,
            country: Country
    ):
        self.id = actor_id
        self.name = name
        self.birth_year = birth_year
        self.country = country

    def get_info(self) -> str:
        return f"{self.name}, {self.birth_year}"


class Studio:
    def __init__(
            self,
            studio_id: int,
            name: str,
            country: Country
    ):
        self.id = studio_id
        self.name = name
        self.country = country

    def get_info(self) -> str:
        return f"{self.name} ({self.country.name})"


class Film:
    def __init__(
            self,
            film_id: int,
            title: str,
            year: int,
            duration: int,
            description: str,
            genre: Genre,
            director: Director,
            actors: list[Actor],
            studio: Studio,
            countries: list[Country]
    ):
        if not title.strip():
            raise InvalidFilmDataError(
                "Название фильма не может быть пустым."
            )

        if year <= 0:
            raise InvalidFilmDataError(
                "Год выпуска должен быть положительным."
            )

        if duration <= 0:
            raise InvalidFilmDataError(
                "Продолжительность должна быть положительной."
            )

        self.id = film_id
        self.title = title
        self.year = year
        self.duration = duration
        self.description = description
        self.genre = genre
        self.director = director
        self.actors = actors
        self.studio = studio
        self.countries = countries

    def get_info(self) -> str:
        return (
            f"{self.title} ({self.year}), "
            f"{self.duration} мин., "
            f"жанр: {self.genre.name}"
        )

    def update(
            self,
            title: str,
            year: int,
            duration: int,
            description: str
    ) -> None:
        if not title.strip():
            raise InvalidFilmDataError(
                "Название фильма не может быть пустым."
            )

        if year <= 0:
            raise InvalidFilmDataError(
                "Год выпуска должен быть положительным."
            )

        if duration <= 0:
            raise InvalidFilmDataError(
                "Продолжительность должна быть положительной."
            )

        self.title = title
        self.year = year
        self.duration = duration
        self.description = description


class User:
    def __init__(self, user_id: int, name: str, email: str):
        self.id = user_id
        self.name = name
        self.email = email

    def get_info(self) -> str:
        return f"{self.name} ({self.email})"


class Rating:
    def __init__(
            self,
            value: float,
            date: str,
            film: Film,
            user: User
    ):
        if not 1 <= value <= 10:
            raise InvalidRatingError(
                "Оценка должна быть от 1 до 10."
            )

        self.value = value
        self.date = date
        self.film = film
        self.user = user

    def set_value(self, value: float) -> None:
        if not 1 <= value <= 10:
            raise InvalidRatingError(
                "Оценка должна быть от 1 до 10."
            )

        self.value = value

    def get_value(self) -> float:
        return self.value


class Review:
    def __init__(
            self,
            review_id: int,
            text: str,
            date: str,
            film: Film,
            user: User
    ):
        self.id = review_id
        self.text = text
        self.date = date
        self.film = film
        self.user = user

    def edit(self, text: str) -> None:
        self.text = text

    def get_text(self) -> str:
        return self.text


class Watchlist:
    def __init__(self, watchlist_id: int, name: str):
        self.id = watchlist_id
        self.name = name
        self.films: list[Film] = []

    def add_film(self, film: Film) -> None:
        if film not in self.films:
            self.films.append(film)

    def remove_film(self, film: Film) -> None:
        if film in self.films:
            self.films.remove(film)

    def get_films(self) -> list[Film]:
        return self.films


class Collection:
    def __init__(
            self,
            collection_id: int,
            name: str,
            description: str
    ):
        self.id = collection_id
        self.name = name
        self.description = description
        self.films: list[Film] = []

    def add_film(self, film: Film) -> None:
        if film not in self.films:
            self.films.append(film)

    def remove_film(self, film: Film) -> None:
        if film in self.films:
            self.films.remove(film)

    def get_films(self) -> list[Film]:
        return self.films
