import xml.etree.ElementTree as ET

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


def add_text(
        parent: ET.Element,
        tag: str,
        value
) -> ET.Element:
    element = ET.SubElement(parent, tag)
    element.text = str(value)

    return element


def get_text(
        element: ET.Element | None,
        tag: str
) -> str:
    if element is None:
        return ""

    child = element.find(tag)

    if child is None or child.text is None:
        return ""

    return child.text


def country_to_xml(
        parent: ET.Element,
        country: Country,
        tag: str = "country"
) -> ET.Element:
    country_element = ET.SubElement(
        parent,
        tag
    )

    add_text(
        country_element,
        "id",
        country.id
    )

    add_text(
        country_element,
        "name",
        country.name
    )

    return country_element


def film_to_xml_element(
        film: Film
) -> ET.Element:
    film_element = ET.Element("film")

    add_text(
        film_element,
        "id",
        film.id
    )

    add_text(
        film_element,
        "title",
        film.title
    )

    add_text(
        film_element,
        "year",
        film.year
    )

    add_text(
        film_element,
        "duration",
        film.duration
    )

    add_text(
        film_element,
        "description",
        film.description
    )

    genre_element = ET.SubElement(
        film_element,
        "genre"
    )

    add_text(
        genre_element,
        "id",
        film.genre.id
    )

    add_text(
        genre_element,
        "name",
        film.genre.name
    )

    add_text(
        genre_element,
        "description",
        film.genre.description
    )

    director_element = ET.SubElement(
        film_element,
        "director"
    )

    add_text(
        director_element,
        "id",
        film.director.id
    )

    add_text(
        director_element,
        "name",
        film.director.name
    )

    add_text(
        director_element,
        "birth_year",
        film.director.birth_year
    )

    country_to_xml(
        director_element,
        film.director.country
    )

    actors_element = ET.SubElement(
        film_element,
        "actors"
    )

    for actor in film.actors:
        actor_element = ET.SubElement(
            actors_element,
            "actor"
        )

        add_text(
            actor_element,
            "id",
            actor.id
        )

        add_text(
            actor_element,
            "name",
            actor.name
        )

        add_text(
            actor_element,
            "birth_year",
            actor.birth_year
        )

        country_to_xml(
            actor_element,
            actor.country
        )

    studio_element = ET.SubElement(
        film_element,
        "studio"
    )

    add_text(
        studio_element,
        "id",
        film.studio.id
    )

    add_text(
        studio_element,
        "name",
        film.studio.name
    )

    country_to_xml(
        studio_element,
        film.studio.country
    )

    countries_element = ET.SubElement(
        film_element,
        "countries"
    )

    for country in film.countries:
        country_to_xml(
            countries_element,
            country
        )

    return film_element


def film_from_xml_element(
        element: ET.Element
) -> Film:
    countries = []

    countries_element = element.find(
        "countries"
    )

    if countries_element is not None:
        for country_element in countries_element.findall(
                "country"
        ):
            countries.append(
                Country(
                    int(get_text(country_element, "id")),
                    get_text(country_element, "name")
                )
            )

    genre_element = element.find("genre")
    if genre_element is None:
        raise ValueError("В XML отсутствует жанр фильма.")

    genre = Genre(
        int(get_text(genre_element, "id")),
        get_text(genre_element, "name"),
        get_text(genre_element, "description")
    )

    director_element = element.find(
        "director"
    )
    if director_element is None:
        raise ValueError("В XML отсутствует режиссёр фильма.")

    director_country_element = (
        director_element.find("country")
    )
    if director_country_element is None:
        raise ValueError("В XML отсутствует страна режиссёра.")

    director = Director(
        int(get_text(director_element, "id")),
        get_text(director_element, "name"),
        int(get_text(
            director_element,
            "birth_year"
        )),
        Country(
            int(get_text(
                director_country_element,
                "id"
            )),
            get_text(
                director_country_element,
                "name"
            )
        )
    )

    actors = []

    actors_element = element.find(
        "actors"
    )

    if actors_element is not None:
        for actor_element in actors_element.findall(
                "actor"
        ):
            country_element = actor_element.find(
                "country"
            )
            if country_element is None:
                raise ValueError("В XML отсутствует страна актёра.")

            actors.append(
                Actor(
                    int(get_text(actor_element, "id")),
                    get_text(actor_element, "name"),
                    int(get_text(
                        actor_element,
                        "birth_year"
                    )),
                    Country(
                        int(get_text(
                            country_element,
                            "id"
                        )),
                        get_text(
                            country_element,
                            "name"
                        )
                    )
                )
            )

    studio_element = element.find(
        "studio"
    )
    if studio_element is None:
        raise ValueError("В XML отсутствует студия фильма.")

    studio_country = studio_element.find(
        "country"
    )
    if studio_country is None:
        raise ValueError("В XML отсутствует страна студии.")

    studio = Studio(
        int(get_text(studio_element, "id")),
        get_text(studio_element, "name"),
        Country(
            int(get_text(
                studio_country,
                "id"
            )),
            get_text(
                studio_country,
                "name"
            )
        )
    )

    return Film(
        int(get_text(element, "id")),
        get_text(element, "title"),
        int(get_text(element, "year")),
        int(get_text(element, "duration")),
        get_text(element, "description"),
        genre,
        director,
        actors,
        studio,
        countries
    )


def save_to_xml(
        library: Library,
        filename: str
) -> None:
    """Сохраняет всю библиотеку в XML."""

    root = ET.Element("library")

    films_element = ET.SubElement(
        root,
        "films"
    )

    for film in library.get_films():
        films_element.append(
            film_to_xml_element(film)
        )

    users_element = ET.SubElement(
        root,
        "users"
    )

    for user in library.get_users():
        user_element = ET.SubElement(
            users_element,
            "user"
        )

        add_text(
            user_element,
            "id",
            user.id
        )

        add_text(
            user_element,
            "name",
            user.name
        )

        add_text(
            user_element,
            "email",
            user.email
        )

    ratings_element = ET.SubElement(
        root,
        "ratings"
    )

    for rating in library.get_ratings():
        rating_element = ET.SubElement(
            ratings_element,
            "rating"
        )

        add_text(
            rating_element,
            "value",
            rating.value
        )

        add_text(
            rating_element,
            "date",
            rating.date
        )

        add_text(
            rating_element,
            "film_id",
            rating.film.id
        )

        add_text(
            rating_element,
            "user_id",
            rating.user.id
        )

    reviews_element = ET.SubElement(
        root,
        "reviews"
    )

    for review in library.get_reviews():
        review_element = ET.SubElement(
            reviews_element,
            "review"
        )

        add_text(
            review_element,
            "id",
            review.id
        )

        add_text(
            review_element,
            "text",
            review.text
        )

        add_text(
            review_element,
            "date",
            review.date
        )

        add_text(
            review_element,
            "film_id",
            review.film.id
        )

        add_text(
            review_element,
            "user_id",
            review.user.id
        )

    collections_element = ET.SubElement(
        root,
        "collections"
    )

    for collection in library.get_collections():
        collection_element = ET.SubElement(
            collections_element,
            "collection"
        )

        add_text(
            collection_element,
            "id",
            collection.id
        )

        add_text(
            collection_element,
            "name",
            collection.name
        )

        add_text(
            collection_element,
            "description",
            collection.description
        )

        films_element = ET.SubElement(
            collection_element,
            "films"
        )

        for film in collection.get_films():
            add_text(
                films_element,
                "film_id",
                film.id
            )

    watchlists_element = ET.SubElement(
        root,
        "watchlists"
    )

    for watchlist in library.get_watchlists():
        watchlist_element = ET.SubElement(
            watchlists_element,
            "watchlist"
        )

        add_text(
            watchlist_element,
            "id",
            watchlist.id
        )

        add_text(
            watchlist_element,
            "name",
            watchlist.name
        )

        films_element = ET.SubElement(
            watchlist_element,
            "films"
        )

        for film in watchlist.get_films():
            add_text(
                films_element,
                "film_id",
                film.id
            )

    tree = ET.ElementTree(root)

    ET.indent(
        tree,
        space="    "
    )

    tree.write(
        filename,
        encoding="utf-8",
        xml_declaration=True
    )


def load_from_xml(
        filename: str
) -> Library:
    """Загружает всю библиотеку из XML."""

    library = Library()

    try:
        tree = ET.parse(filename)
        root = tree.getroot()

    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"Файл XML не найден: {filename}"
        ) from error

    except ET.ParseError as error:
        raise ValueError(
            f"Некорректный формат XML: {filename}"
        ) from error

    try:

        films_element = root.find("films")

        if films_element is not None:
            for film_element in films_element.findall("film"):
                library.add_film(
                    film_from_xml_element(
                        film_element
                    )
                )

        users_by_id = {}

        users_element = root.find("users")

        if users_element is not None:
            for user_element in users_element.findall(
                    "user"
            ):
                user = User(
                    int(get_text(user_element, "id")),
                    get_text(user_element, "name"),
                    get_text(user_element, "email")
                )

                library.add_user(user)
                users_by_id[user.id] = user

        ratings_element = root.find("ratings")

        if ratings_element is not None:
            for rating_element in ratings_element.findall(
                    "rating"
            ):
                film = library.find_film(
                    int(
                        get_text(
                            rating_element,
                            "film_id"
                        )
                    )
                )
                if film is None:
                    raise ValueError(
                        "В XML указана несуществующая оценка фильма."
                    )

                user = users_by_id[
                    int(
                        get_text(
                            rating_element,
                            "user_id"
                        )
                    )
                ]

                rating = Rating(
                    float(
                        get_text(
                            rating_element,
                            "value"
                        )
                    ),
                    get_text(
                        rating_element,
                        "date"
                    ),
                    film,
                    user
                )

                library.add_rating(rating)

        reviews_element = root.find("reviews")

        if reviews_element is not None:
            for review_element in reviews_element.findall(
                    "review"
            ):
                film = library.find_film(
                    int(
                        get_text(
                            review_element,
                            "film_id"
                        )
                    )
                )
                if film is None:
                    raise ValueError(
                        "В XML указан отзыв о несуществующем фильме."
                    )

                user = users_by_id[
                    int(
                        get_text(
                            review_element,
                            "user_id"
                        )
                    )
                ]

                review = Review(
                    int(
                        get_text(
                            review_element,
                            "id"
                        )
                    ),
                    get_text(
                        review_element,
                        "text"
                    ),
                    get_text(
                        review_element,
                        "date"
                    ),
                    film,
                    user
                )

                library.add_review(review)

        collections_element = root.find(
            "collections"
        )

        if collections_element is not None:
            for collection_element in (
                    collections_element.findall(
                        "collection"
                    )
            ):
                collection = Collection(
                    int(
                        get_text(
                            collection_element,
                            "id"
                        )
                    ),
                    get_text(
                        collection_element,
                        "name"
                    ),
                    get_text(
                        collection_element,
                        "description"
                    )
                )

                films_element = collection_element.find(
                    "films"
                )

                if films_element is not None:
                    for film_id_element in (
                            films_element.findall("film_id")
                    ):
                        film = library.find_film(
                            int(film_id_element.text or "")
                        )

                        if film is not None:
                            collection.add_film(film)

                library.add_collection(collection)

        watchlists_element = root.find(
            "watchlists"
        )

        if watchlists_element is not None:
            for watchlist_element in (
                    watchlists_element.findall(
                        "watchlist"
                    )
            ):
                watchlist = Watchlist(
                    int(
                        get_text(
                            watchlist_element,
                            "id"
                        )
                    ),
                    get_text(
                        watchlist_element,
                        "name"
                    )
                )

                films_element = watchlist_element.find(
                    "films"
                )

                if films_element is not None:
                    for film_id_element in (
                            films_element.findall("film_id")
                    ):
                        film = library.find_film(
                            int(film_id_element.text or "")
                        )

                        if film is not None:
                            watchlist.add_film(film)

                library.add_watchlist(watchlist)

    except (KeyError, TypeError, ValueError) as error:
        raise ValueError(
            f"Некорректные данные в XML: {error}"
        ) from error

    return library
