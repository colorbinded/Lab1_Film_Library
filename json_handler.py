import json

from models import (
    Country,
    Genre,
    Director,
    Actor,
    Studio,
    Film,
    User,
    Rating,
    Review,
    Watchlist,
    Collection
)

from library import Library


def country_to_dict(country: Country) -> dict:
    return {
        "id": country.id,
        "name": country.name
    }


def country_from_dict(data: dict) -> Country:
    return Country(
        data["id"],
        data["name"]
    )


def film_to_dict(film: Film) -> dict:
    return {
        "id": film.id,
        "title": film.title,
        "year": film.year,
        "duration": film.duration,
        "description": film.description,

        "genre": {
            "id": film.genre.id,
            "name": film.genre.name,
            "description": film.genre.description
        },

        "director": {
            "id": film.director.id,
            "name": film.director.name,
            "birth_year": film.director.birth_year,
            "country": country_to_dict(
                film.director.country
            )
        },

        "actors": [
            {
                "id": actor.id,
                "name": actor.name,
                "birth_year": actor.birth_year,
                "country": country_to_dict(
                    actor.country
                )
            }
            for actor in film.actors
        ],

        "studio": {
            "id": film.studio.id,
            "name": film.studio.name,
            "country": country_to_dict(
                film.studio.country
            )
        },

        "countries": [
            country_to_dict(country)
            for country in film.countries
        ]
    }


def film_from_dict(data: dict) -> Film:
    countries = [
        country_from_dict(country)
        for country in data["countries"]
    ]

    genre_data = data["genre"]

    genre = Genre(
        genre_data["id"],
        genre_data["name"],
        genre_data["description"]
    )

    director_data = data["director"]

    director = Director(
        director_data["id"],
        director_data["name"],
        director_data["birth_year"],
        country_from_dict(
            director_data["country"]
        )
    )

    actors = []

    for actor_data in data["actors"]:
        actors.append(
            Actor(
                actor_data["id"],
                actor_data["name"],
                actor_data["birth_year"],
                country_from_dict(
                    actor_data["country"]
                )
            )
        )

    studio_data = data["studio"]

    studio = Studio(
        studio_data["id"],
        studio_data["name"],
        country_from_dict(
            studio_data["country"]
        )
    )

    return Film(
        data["id"],
        data["title"],
        data["year"],
        data["duration"],
        data["description"],
        genre,
        director,
        actors,
        studio,
        countries
    )


def save_to_json(
        library: Library,
        filename: str
) -> None:
    """Сохраняет всю библиотеку в JSON."""

    data = {
        "films": [
            film_to_dict(film)
            for film in library.get_films()
        ],

        "users": [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
            for user in library.get_users()
        ],

        "ratings": [
            {
                "value": rating.value,
                "date": rating.date,
                "film_id": rating.film.id,
                "user_id": rating.user.id
            }
            for rating in library.get_ratings()
        ],

        "reviews": [
            {
                "id": review.id,
                "text": review.text,
                "date": review.date,
                "film_id": review.film.id,
                "user_id": review.user.id
            }
            for review in library.get_reviews()
        ],

        "collections": [
            {
                "id": collection.id,
                "name": collection.name,
                "description": collection.description,
                "film_ids": [
                    film.id
                    for film in collection.get_films()
                ]
            }
            for collection in library.get_collections()
        ],

        "watchlists": [
            {
                "id": watchlist.id,
                "name": watchlist.name,
                "film_ids": [
                    film.id
                    for film in watchlist.get_films()
                ]
            }
            for watchlist in library.get_watchlists()
        ]
    }

    with open(
            filename,
            "w",
            encoding="utf-8"
    ) as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


def load_from_json(
        filename: str
) -> Library:
    """Загружает всю библиотеку из JSON."""

    library = Library()

    try:
        with open(
                filename,
                "r",
                encoding="utf-8"
        ) as file:
            data = json.load(file)

    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"Файл JSON не найден: {filename}"
        ) from error

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Некорректный формат JSON: {filename}"
        ) from error

    try:

        for film_data in data["films"]:
            library.add_film(
                film_from_dict(film_data)
            )

        users_by_id = {}

        for user_data in data["users"]:
            user = User(
                user_data["id"],
                user_data["name"],
                user_data["email"]
            )

            library.add_user(user)
            users_by_id[user.id] = user

        for rating_data in data["ratings"]:
            film = library.find_film(
                rating_data["film_id"]
            )
            if film is None:
                raise ValueError(
                    "В JSON указана оценка несуществующего фильма."
                )

            user = users_by_id[
                rating_data["user_id"]
            ]

            rating = Rating(
                rating_data["value"],
                rating_data["date"],
                film,
                user
            )

            library.add_rating(rating)

        for review_data in data["reviews"]:
            film = library.find_film(
                review_data["film_id"]
            )
            if film is None:
                raise ValueError(
                    "В JSON указан отзыв о несуществующем фильме."
                )

            user = users_by_id[
                review_data["user_id"]
            ]

            review = Review(
                review_data["id"],
                review_data["text"],
                review_data["date"],
                film,
                user
            )

            library.add_review(review)

        for collection_data in data["collections"]:
            collection = Collection(
                collection_data["id"],
                collection_data["name"],
                collection_data["description"]
            )

            for film_id in collection_data["film_ids"]:
                film = library.find_film(film_id)

                if film is not None:
                    collection.add_film(film)

            library.add_collection(collection)

        for watchlist_data in data["watchlists"]:
            watchlist = Watchlist(
                watchlist_data["id"],
                watchlist_data["name"]
            )

            for film_id in watchlist_data["film_ids"]:
                film = library.find_film(film_id)

                if film is not None:
                    watchlist.add_film(film)

            library.add_watchlist(watchlist)

    except KeyError as error:
        raise ValueError(
            f"В JSON отсутствует обязательное поле: {error}"
        ) from error

    except (TypeError, ValueError) as error:
        raise ValueError(
            f"Некорректные данные в JSON: {error}"
        ) from error

    return library
