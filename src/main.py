from pathlib import Path

from exceptions import (
    DuplicateFilmError,
    FilmNotFoundError,
    InvalidFilmDataError,
)
from json_handler import load_from_json, save_to_json
from library import Library
from models import (
    Actor,
    Collection,
    Country,
    Director,
    Film,
    Genre,
    Rating,
    Review,
    Studio,
    User,
    Watchlist,
)
from xml_handler import load_from_xml, save_to_xml

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
JSON_FILE = DATA_DIR / "films.json"
XML_FILE = DATA_DIR / "films.xml"


def create_demo_library() -> Library:
    """создает библиотеку с начальными фильмами"""

    usa = Country(1, "США")
    uk = Country(2, "Великобритания")
    sci_fi = Genre(
        1,
        "Фантастика",
        "Фильмы о космосе, будущем и научных открытиях.",
    )
    action = Genre(
        2,
        "Боевик",
        "Фильмы с большим количеством динамичных сцен.",
    )
    director_nolan = Director(
        1,
        "Кристофер Нолан",
        1970,
        uk,
    )
    actor_mcconaughey = Actor(
        1,
        "Мэттью Макконахи",
        1969,
        usa,
    )
    actor_bale = Actor(
        2,
        "Кристиан Бэйл",
        1974,
        uk,
    )
    studio_warner = Studio(
        1,
        "Warner Bros.",
        usa,
    )
    film_1 = Film(
        1,
        "Интерстеллар",
        2014,
        169,
        "Группа исследователей отправляется "
        "в космос для поиска нового дома "
        "для человечества.",
        sci_fi,
        director_nolan,
        [actor_mcconaughey],
        studio_warner,
        [usa, uk],
    )
    film_2 = Film(
        2,
        "Тёмный рыцарь",
        2008,
        152,
        "Бэтмен противостоит Джокеру.",
        action,
        director_nolan,
        [actor_bale],
        studio_warner,
        [usa, uk],
    )
    user_1 = User(
        1,
        "Иван",
        "ivan@mail.ru",
    )
    user_2 = User(
        2,
        "Анна",
        "anna@mail.ru",
    )
    rating_1 = Rating(
        10,
        "2026-10-06",
        film_1,
        user_1,
    )
    rating_2 = Rating(
        9,
        "2026-10-06",
        film_2,
        user_2,
    )
    review_1 = Review(
        1,
        "Отличный фильм! Очень интересный сюжет.",
        "2026-10-06",
        film_1,
        user_1,
    )
    review_2 = Review(
        2,
        "Один из лучших фильмов о Бэтмене.",
        "2026-10-06",
        film_2,
        user_2,
    )
    watchlist_1 = Watchlist(
        1,
        "Посмотреть вечером",
    )
    watchlist_1.add_film(film_1)

    watchlist_2 = Watchlist(
        2,
        "Фильмы на выходные",
    )
    watchlist_2.add_film(film_2)
    collection_1 = Collection(
        1,
        "Любимые фильмы",
        "Фильмы, которые хочется пересматривать.",
    )
    collection_1.add_film(film_1)
    collection_1.add_film(film_2)

    library = Library()

    library.add_film(film_1)
    library.add_film(film_2)

    library.add_user(user_1)
    library.add_user(user_2)

    library.add_rating(rating_1)
    library.add_rating(rating_2)

    library.add_review(review_1)
    library.add_review(review_2)

    library.add_collection(collection_1)

    library.add_watchlist(watchlist_1)
    library.add_watchlist(watchlist_2)

    return library


def print_films(library: Library) -> None:
    """выводит список фыильмов"""

    films = library.get_films()

    if not films:
        print("\nБиблиотека фильмов пуста.")
        return

    print("\n=== СПИСОК ФИЛЬМОВ ===")

    for film in films:
        print(
            f"ID: {film.id} | "
            f"{film.title} ({film.year}) | "
            f"{film.duration} мин. | "
            f"Жанр: {film.genre.name}"
        )


def print_film_details(film: Film) -> None:
    """выводит инфу о конкретном фильме"""

    countries = ", ".join(
        country.name
        for country in film.countries
    )

    print("\n=== ИНФОРМАЦИЯ О ФИЛЬМЕ ===")
    print(f"ID: {film.id}")
    print(f"Название: {film.title}")
    print(f"Год: {film.year}")
    print(f"Продолжительность: {film.duration} мин.")
    print(f"Описание: {film.description}")

    print("\n--- ЖАНР ---")
    print(f"Название: {film.genre.name}")
    print(f"Описание: {film.genre.description}")

    print("\n--- РЕЖИССЁР ---")
    print(f"Имя: {film.director.name}")
    print(f"Год рождения: {film.director.birth_year}")
    print(f"Страна: {film.director.country.name}")

    print("\n--- АКТЁРЫ ---")

    if film.actors:
        for actor in film.actors:
            print(
                f"- {actor.name}, "
                f"{actor.birth_year}, "
                f"{actor.country.name}"
            )
    else:
        print("Актёры не указаны.")

    print("\n--- СТУДИЯ ---")
    print(f"Название: {film.studio.name}")
    print(f"Страна: {film.studio.country.name}")

    print("\n--- СТРАНЫ ФИЛЬМА ---")
    print(countries)


def input_positive_int(prompt: str) -> int:
    """для проверки на положительное число"""

    value = int(input(prompt))
    if value <= 0:
        raise ValueError(
            "Значение должно быть положительным."
        )
    return value


def input_non_empty(prompt: str) -> str:
    """для поверки на пустую строку"""

    value = input(prompt).strip()
    if not value:
        raise ValueError(
            "Значение не может быть пустым."
        )
    return value


def add_film_menu(library: Library) -> None:
    """добавляет фильм (чеерз менюшку)"""

    try:
        print("\n=== ДОБАВЛЕНИЕ ФИЛЬМА ===")
        film_id = input_positive_int(
            "Введите ID фильма: "
        )
        title = input_non_empty(
            "Введите название фильма: "
        )
        year = input_positive_int(
            "Введите год выпуска: "
        )
        duration = input_positive_int(
            "Введите продолжительность в минутах: "
        )
        description = input_non_empty(
            "Введите описание фильма: "
        )

        print("\n--- ИНФОРМАЦИЯ О ЖАНРЕ ---")
        genre_name = input_non_empty(
            "Название жанра: "
        )
        genre_description = input_non_empty(
            "Описание жанра: "
        )
        genre = Genre(
            film_id,
            genre_name,
            genre_description,
        )

        print("\n--- СТРАНА РЕЖИССЁРА ---")
        director_country_name = input_non_empty(
            "Страна режиссёра: "
        )
        director_country = Country(
            film_id,
            director_country_name,
        )

        print("\n--- ИНФОРМАЦИЯ О РЕЖИССЁРЕ ---")
        director_name = input_non_empty(
            "Имя режиссёра: "
        )
        director_birth_year = input_positive_int(
            "Год рождения режиссёра: "
        )
        director = Director(
            film_id,
            director_name,
            director_birth_year,
            director_country,
        )

        print("\n--- АКТЁРЫ ---")
        actors = []
        actors_count = input_positive_int(
            "Сколько актёров добавить: "
        )

        for number in range(1, actors_count + 1):
            print(f"\nАктёр №{number}")

            actor_name = input_non_empty(
                "Имя актёра: "
            )
            actor_birth_year = input_positive_int(
                "Год рождения актёра: "
            )
            actor_country_name = input_non_empty(
                "Страна актёра: "
            )
            actor_country = Country(
                film_id * 100 + number,
                actor_country_name,
            )
            actor = Actor(
                film_id * 100 + number,
                actor_name,
                actor_birth_year,
                actor_country,
            )
            actors.append(actor)

        print("\n--- СТРАНЫ ПРОИЗВОДСТВА ---")
        countries = []
        countries_count = input_positive_int(
            "Сколько стран указать: "
        )
        for number in range(1, countries_count + 1):
            country_name = input_non_empty(
                f"Название страны №{number}: "
            )
            country = Country(
                film_id * 1000 + number,
                country_name,
            )
            countries.append(country)

        print("\n--- СТУДИЯ ---")
        studio_name = input_non_empty(
            "Название студии: "
        )
        studio_country_name = input_non_empty(
            "Страна студии: "
        )
        studio_country = Country(
            film_id * 2000,
            studio_country_name,
        )
        studio = Studio(
            film_id,
            studio_name,
            studio_country,
        )
        film = Film(
            film_id,
            title,
            year,
            duration,
            description,
            genre,
            director,
            actors,
            studio,
            countries,
        )
        library.add_film(film)

        print("\nФильм успешно добавлен!")
        print_film_details(film)

    except ValueError as error:
        print(f"\nОшибка ввода: {error}")

    except InvalidFilmDataError as error:
        print(f"\nОшибка данных фильма: {error}")

    except DuplicateFilmError as error:
        print(f"\nОшибка: {error}")


def find_film_menu(library: Library) -> None:
    """ищет фильм"""

    try:
        film_id = input_positive_int(
            "\nВведите ID фильма для поиска: "
        )

        film = library.find_film(film_id)
        if film is None:
            raise FilmNotFoundError(
                f"Фильм с ID {film_id} не найден."
            )
        print_film_details(film)

    except ValueError as error:
        print(f"Ошибка ввода: {error}")

    except FilmNotFoundError as error:
        print(f"Ошибка: {error}")


def update_film_menu(library: Library) -> None:
    """изменяет данные р фильме"""

    try:
        print("\n=== ИЗМЕНЕНИЕ ФИЛЬМА ===")
        film_id = input_positive_int(
            "Введите ID фильма: "
        )
        film = library.find_film(film_id)

        if film is None:
            raise FilmNotFoundError(
                f"Фильм с ID {film_id} не найден."
            )
        title = input(
            f"Новое название [{film.title}]: "
        ).strip()
        year_input = input(
            f"Новый год [{film.year}]: "
        ).strip()
        duration_input = input(
            f"Новая продолжительность "
            f"[{film.duration}]: "
        ).strip()
        description = input(
            f"Новое описание [{film.description}]: "
        ).strip()

        if not title:
            title = film.title

        year = (
            int(year_input)
            if year_input
            else film.year
        )
        duration = (
            int(duration_input)
            if duration_input
            else film.duration
        )
        if not description:
            description = film.description

        library.update_film(
            film_id,
            title,
            year,
            duration,
            description,
        )
        print("Данные фильма успешно изменены.")

    except ValueError as error:
        print(f"Ошибка ввода: {error}")

    except FilmNotFoundError as error:
        print(f"Ошибка: {error}")

    except InvalidFilmDataError as error:
        print(f"Ошибка данных фильма: {error}")


def delete_film_menu(library: Library) -> None:
    """удаляет фильт"""

    try:
        print("\n=== УДАЛЕНИЕ ФИЛЬМА ===")
        film_id = input_positive_int(
            "Введите ID фильма: "
        )
        film = library.find_film(film_id)

        if film is None:
            raise FilmNotFoundError(
                f"Фильм с ID {film_id} не найден."
            )

        confirmation = input(
            f"Удалить фильм «{film.title}»? (y/n): "
        ).strip().lower()

        if confirmation != "y":
            print("Удаление отменено.")
            return

        library.delete_film(film_id)

        library.ratings[:] = [
            rating
            for rating in library.get_ratings()
            if rating.film.id != film_id
        ]
        library.reviews[:] = [
            review
            for review in library.get_reviews()
            if review.film.id != film_id
        ]
        for collection in library.get_collections():
            collection.remove_film(film)

        for watchlist in library.get_watchlists():
            watchlist.remove_film(film)

        print("Фильм успешно удалён.")

    except ValueError as error:
        print(f"Ошибка ввода: {error}")

    except FilmNotFoundError as error:
        print(f"Ошибка: {error}")


def save_json_menu(library: Library) -> None:
    """сохраняет в JSON"""

    try:
        save_to_json(library, JSON_FILE)
        print(
            f"Данные сохранены в {JSON_FILE}."
        )

    except OSError as error:
        print(
            f"Ошибка записи JSON-файла: {error}"
        )


def load_json_menu(library: Library) -> Library:
    """загружает из JSON"""

    try:
        loaded_library = load_from_json(
            JSON_FILE
        )
        print(f"Данные загружены из {JSON_FILE}.")
        return loaded_library

    except FileNotFoundError as error:
        print(f"Файл не найден: {error}")

    except ValueError as error:
        print(f"Ошибка JSON: {error}")

    return library


def save_xml_menu(library: Library) -> None:
    """сохраняет в XML"""

    try:
        save_to_xml(library, XML_FILE)

        print(f"Данные сохранены в {XML_FILE}.")

    except OSError as error:
        print(f"Ошибка записи XML-файла: {error}")


def load_xml_menu(library: Library) -> Library:
    """загружает из XML"""

    try:
        loaded_library = load_from_xml(
            XML_FILE
        )
        print(f"Данные загружены из {XML_FILE}.")

        return loaded_library

    except FileNotFoundError as error:
        print(f"Файл не найден: {error}")

    except ValueError as error:
        print(f"Ошибка XML: {error}")

    return library


def print_statistics(library: Library) -> None:
    """выодит подробную статистику"""

    print("\n========================================")
    print("              СТАТИСТИКА")
    print("========================================")

    print(
        f"\nКоличество фильмов: "
        f"{len(library.get_films())}"
    )

    print(
        f"Количество пользователей: "
        f"{len(library.get_users())}"
    )
    print(
        f"Количество оценок: "
        f"{len(library.get_ratings())}"
    )
    print(
        f"Количество отзывов: "
        f"{len(library.get_reviews())}"
    )
    print(
        f"Количество коллекций: "
        f"{len(library.get_collections())}"
    )
    print(
        f"Количество списков просмотра: "
        f"{len(library.get_watchlists())}"
    )

    print("\n=== ПОЛЬЗОВАТЕЛИ ===")
    users = library.get_users()
    if users:
        for user in users:
            print(
                f"ID: {user.id} | "
                f"Имя: {user.name} | "
                f"Email: {user.email}"
            )
    else:
        print("Пользователей нет.")

    print("\n=== ОЦЕНКИ ===")
    ratings = library.get_ratings()
    if ratings:
        for rating in ratings:
            print(
                f"Фильм: {rating.film.title} | "
                f"Пользователь: {rating.user.name} | "
                f"Оценка: {rating.value}/10 | "
                f"Дата: {rating.date}"
            )
    else:
        print("Оценок нет.")

    print("\n=== ОТЗЫВЫ ===")
    reviews = library.get_reviews()
    if reviews:
        for review in reviews:
            print(
                f"ID: {review.id} | "
                f"Фильм: {review.film.title}"
            )
            print(
                f"Пользователь: "
                f"{review.user.name}"
            )
            print(f"Дата: {review.date}")
            print(f"Текст: {review.text}")
            print("-" * 40)
    else:
        print("Отзывов нет.")

    print("\n=== КОЛЛЕКЦИИ ===")
    collections = library.get_collections()
    if collections:
        for collection in collections:
            film_names = ", ".join(
                film.title
                for film in collection.get_films()
            )

            print(
                f"ID: {collection.id} | "
                f"Название: {collection.name}"
            )
            print(
                f"Описание: "
                f"{collection.description}"
            )
            print(
                f"Фильмы: {film_names}"
            )
            print("-" * 40)
    else:
        print("Коллекций нет.")

    print("\n=== СПИСКИ ПРОСМОТРА ===")
    watchlists = library.get_watchlists()
    if watchlists:
        for watchlist in watchlists:
            film_names = ", ".join(
                film.title
                for film in watchlist.get_films()
            )
            print(
                f"ID: {watchlist.id} | "
                f"Название: {watchlist.name}"
            )
            print(
                f"Фильмы: {film_names}"
            )
            print("-" * 40)
    else:
        print("Списков просмотра нет.")


def print_menu() -> None:
    """вывод меню"""

    print(
        "\n"
        "========================================\n"
        "    УЧЁТ ЛИЧНОЙ БИБЛИОТЕКИ ФИЛЬМОВ\n"
        "========================================\n"
        "1. Показать все фильмы\n"
        "2. Добавить фильм\n"
        "3. Найти фильм по ID\n"
        "4. Изменить фильм\n"
        "5. Удалить фильм\n"
        "6. Показать статистику\n"
        "7. Сохранить в JSON\n"
        "8. Загрузить из JSON\n"
        "9. Сохранить в XML\n"
        "10. Загрузить из XML\n"
        "0. Выход\n"
        "========================================"
    )


def main() -> None:

    library = create_demo_library()
    print(
        "Программа учёта личной библиотеки "
        "фильмов запущена."
    )
    print(
        "Созданы демонстрационные данные: "
        f"{len(library.get_films())} фильма, "
        f"{len(library.get_users())} пользователя, "
        f"{len(library.get_reviews())} отзыва."
    )
    while True:
        print_menu()

        choice = input(
            "Выберите действие: "
        ).strip()

        match choice:
            case "1":
                print_films(library)
            case "2":
                add_film_menu(library)
            case "3":
                find_film_menu(library)
            case "4":
                update_film_menu(library)
            case "5":
                delete_film_menu(library)
            case "6":
                print_statistics(library)
            case "7":
                save_json_menu(library)
            case "8":
                library = load_json_menu(library)
            case "9":
                save_xml_menu(library)
            case "10":
                library = load_xml_menu(library)
            case "0":
                print("Работа программы завершена.")
                break
            case _:
                print(
                    "Неизвестный пункт меню. "
                    "Введите число от 0 до 10."
                )

if __name__ == "__main__": #красотулечка
    main()
