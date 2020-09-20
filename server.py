from bottle import HTTPError, request, route, run

import finder as fdr


def valid_year(year):
    """
    Функция проверяющая валидность введенного года, наличие 4 цифр и принадлежность к int
    """
    if year is not None:
        if year.isdigit() and len(year) == 4:
            return True
        else:
            return False
    else:
        return False


def valid_data(artist, album, genre):
    """
    Функция проверяющая, заполнены ли все данные об альбоме
    """
    if (artist is not None) and (album is not None) and (genre is not None):
        return True
    else:
        return False


# Функция обработчик GET-запросов:
@route("/albums/<artist>")
def albums(artist):
    albums_list = fdr.find_artist(artist)
    # Производим поиск по артисту в базе данных
    if not albums_list:
        message = f"Альбомов {artist} не найдено"
        result = HTTPError(404, message)
    # Если артист находится, выводим результат со списком его альбомов
    else:
        album_names = [album.album for album in albums_list]
        number_of_albums = len(album_names)
        result = f"Найдено всего альбомов {artist} - {number_of_albums}. Список альбомов: "
        result += ", ".join(album_names)
    return result


# Функция обработчик POST-запросов:
@route("/albums", method="POST")
def albums():
    new_album = {
        "year": request.forms.get("year"),
        "artist": request.forms.get("artist"),
        "genre": request.forms.get("genre"),
        "album": request.forms.get("album")
        }
    albums_list = fdr.find_album(new_album["album"])
    album_names = [album.album for album in albums_list]
    album_title = new_album["album"]
    album_artist = new_album["artist"]
    album_genre = new_album["genre"]
    album_year = new_album["year"]
    # Проводим проверку, есть ли альбом в базе данных, если есть выводим обо этом сообщение
    if album_title in album_names:
        message = f"Альбом {album_title} уже есть в базе альбомов"
        result = HTTPError(409, message)
    else:
        # Проверям правильно ли внесена дата и данные об альбоме, если проходит проверку сохраняем в БД
        if valid_year(album_year) and valid_data(album_artist, album_title, album_genre):
            result = fdr.save(new_album)
        # Если проверку не проходит, выводим соответствующую ошибку
        elif valid_data(album_artist, album_title, album_genre) and not valid_year(album_year):
            message = f"Дата альбома {album_title} введена некорректно. Введите год в формате YYYY."
            result = HTTPError(409, message)
        else:
            message = "Данные введены некорректно, проверьте внесены ли данные 'artist', 'album', 'genre'"
            result = HTTPError(409, message)
    return result
        

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
