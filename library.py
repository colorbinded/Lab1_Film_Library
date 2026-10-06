from exceptions import FilmNotFoundError, DuplicateFilmError
from models import (
    Film,
    Collection,
    Watchlist,
    User,
    Rating,
    Review
)


class Library:
    def __init__(self):
        self.films: list[Film] = []
        self.collections: list[Collection] = []
        self.watchlists: list[Watchlist] = []
        self.users: list[User] = []
        self.ratings: list[Rating] = []
        self.reviews: list[Review] = []

    def add_film(self, film: Film) -> None:
        if self.find_film(film.id) is not None:
            raise DuplicateFilmError(
                f"Фильм с ID {film.id} уже существует."
            )

        self.films.append(film)

    def get_films(self) -> list[Film]:
        return self.films

    def find_film(self, film_id: int) -> Film | None:
        for film in self.films:
            if film.id == film_id:
                return film

        return None

    def update_film(
            self,
            film_id: int,
            title: str,
            year: int,
            duration: int,
            description: str
    ) -> None:
        film = self.find_film(film_id)

        if film is None:
            raise FilmNotFoundError(
                f"Фильм с ID {film_id} не найден."
            )

        film.update(
            title,
            year,
            duration,
            description
        )

    def delete_film(self, film_id: int) -> None:
        film = self.find_film(film_id)

        if film is None:
            raise FilmNotFoundError(
                f"Фильм с ID {film_id} не найден."
            )

        self.films.remove(film)

    def add_user(self, user: User) -> None:
        self.users.append(user)

    def get_users(self) -> list[User]:
        return self.users

    def add_rating(self, rating: Rating) -> None:
        self.ratings.append(rating)

    def get_ratings(self) -> list[Rating]:
        return self.ratings

    def add_review(self, review: Review) -> None:
        self.reviews.append(review)

    def get_reviews(self) -> list[Review]:
        return self.reviews

    def add_collection(
            self,
            collection: Collection
    ) -> None:
        self.collections.append(collection)

    def get_collections(self) -> list[Collection]:
        return self.collections

    def add_watchlist(
            self,
            watchlist: Watchlist
    ) -> None:
        self.watchlists.append(watchlist)

    def get_watchlists(self) -> list[Watchlist]:
        return self.watchlists
