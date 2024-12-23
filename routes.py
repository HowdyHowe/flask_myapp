from flask import Flask
from flask import jsonify, request
from flask_mail import Mail, Message
import mysql.connector
import requests
import re
import ast
import json
import string
import random

TMDB_API_KEY = '8ec214ca2f44667feb8e5c68310e814e'
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
OMDB_KEY = '53c68d6c'

conndb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Toba_2002",
    database="reckomov"
)

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USERNAME'] = 'amiruddinstr@gmail.com'
app.config['MAIL_PASSWORD'] = 'jkjvqgnaxynwirgs'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)


def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def email_validation(email):
    pattern = r"@gmail\.|@yahoo\."
    return re.search(pattern, email) is not None


all_genres = [28, 12, 16, 35, 80, 99, 18, 10751, 14, 36,
              27, 10402, 9648, 10749, 878, 10770, 53, 10752, 37]


@app.route("/", methods=["GET"])
def test():
    return "tes"


@app.route("/user_signin", methods=['POST'])
def user_signin():
    try:
        data = request.get_json()
        email = str(data.get('email'))
        username = data.get('username')
        password = data.get('password')
        password_conf = data.get('confirm_password')
        if not email or not username or not password or not password_conf:
            return "failed", 400
        if len(password) < 8:
            return "failed", 404
        if password != password_conf:
            return "failed", 401
        if not email_validation(email):
            return "failed", 403
        cursor = conndb.cursor(dictionary=True)
        cursor.execute(
            'SELECT *  FROM akun_user WHERE email=%s;', (email,))
        mycur = cursor.fetchall()
        if mycur:
            return "failed", 402
        else:
            # id_data = email[0:3] + password[0:3]
            id_data = id_generator()
            cursor.execute('INSERT INTO data_film_user (id_data) VALUES (%s);',
                           (id_data,))
            cursor.execute('INSERT INTO akun_user (email, password, username, id_data) VALUES (%s, %s, %s, %s);',
                           (email, password, username, id_data))
            conndb.commit()
            return "berhasil", 202
    except Exception as error:
        print(error)
        return "failed", 400


@app.route("/user_login", methods=['POST'])
def user_login():
    try:
        cursor = conndb.cursor(dictionary=True)
        data = request.get_json()
        email = data.get('email')
        pas = data.get('password')
        if not email_validation(email):
            return "failed", 402

        cursor.execute(
            'SELECT * FROM akun_user WHERE email=%s AND password=%s;', (email, pas))
        user = cursor.fetchone()
        if not email or not pas:
            return "failed", 400
        if not user:
            return "failed", 401
        if user['email'] == email and user['password'] == pas:
            return "success", 201
    except:
        return "failed", 400


@app.route("/user_update", methods=['POST'])
def user_update():
    cursor = conndb.cursor(dictionary=True)
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    cursor.execute(
        "SELECT * FROM akun_user WHERE email = %s", (email,))
    user = cursor.fetchone()

    if not username or not password:
        return "failed", 400

    if user["username"] == username and user["password"] == password:
        return "failed", 401
    if len(password) < 8:
        return "failed", 402

    cursor.execute("UPDATE akun_user SET username = %s, password = %s WHERE email = %s",
                   (username, password, email))
    if cursor.rowcount == 0:
        return "failed", 403

    conndb.commit()
    return "success", 201


@app.route('/userforget', methods=["POST"])
def user_forget():
    data = request.get_json()
    email = data.get("email")
    cursor = conndb.cursor(dictionary=True)
    if not email:
        return "failed", 400
    # try:
    cursor.execute(
        "SELECT password FROM akun_user WHERE email = %s", (email,))
    em = cursor.fetchone()
    mes = Message(subject="Lupa Sandi",
                  sender="myapp@gmail.com", recipients=[email,])
    mes.body = f"Jangan bagikan email ini pada siapapun!. Kata sandi anda adalah {
        em["password"]}"
    mail.send(mes)
    return "success", 202
    # except:
    #     return "failed", 401


@app.route('/homepage', methods=["GET"])
def homepage():
    random_num = random.randrange(1, 500)
    categories = {}
    endpoints = {
        'trending': f"{TMDB_BASE_URL}/trending/movie/week?api_key={TMDB_API_KEY}&include_adult=false",
        'new_releases': f"{TMDB_BASE_URL}/movie/now_playing?api_key={TMDB_API_KEY}&include_adult=false",
        'top_rated': f"{TMDB_BASE_URL}/movie/top_rated?api_key={TMDB_API_KEY}&include_adult=false",
        'upcoming': f"{TMDB_BASE_URL}/movie/upcoming?api_key={TMDB_API_KEY}&page=1&include_adult=false",
        'recommendation': f"{TMDB_BASE_URL}/discover/movie?api_key={TMDB_API_KEY}&sort_by=vote_average.desc&with_genres=28&include_adult=false&page={random_num}"
    }

    def ambil(resultnum, categ, ur):
        response = requests.get(ur)
        response.raise_for_status()
        result = response.json()['results']
        categories[categ] = result[:resultnum]

    for category, url in endpoints.items():
        if category == 'trending':
            ambil(10, category, url)
        elif category == 'new_releases':
            ambil(10, category, url)
        elif category == 'top_rated':
            ambil(10, category, url)
        elif category == 'upcoming':
            ambil(10, category, url)
        elif category == 'recommendation':
            ambil(10, category, url)
    return jsonify(categories)


@app.route("/allinfopage/<section>", methods=['GET'])
def allinfo(section):
    # try:
    cursor = conndb.cursor()
    # data = request.get_json()
    # email = data.get("email")

    random_num = random.randrange(1, 500)
    categories = {}

    cursor.execute('SELECT data_film_user.preferensi, data_film_user.id_data FROM akun_user INNER JOIN data_film_user ON akun_user.id_data = data_film_user.id_data WHERE akun_user.email="toba@gmail.com"')
    preference_data = cursor.fetchone()
    print(preference_data)
    genre_list = ast.literal_eval(preference_data[0])

    if not genre_list:
        genre_list = random.sample(all_genres, 2)

    genre = '| '.join(map(str, genre_list))
    print(genre)

    endpoints = {
        'trending': f"{TMDB_BASE_URL}/trending/movie/week?api_key={TMDB_API_KEY}",
        'new_releases': f"{TMDB_BASE_URL}/movie/now_playing?api_key={TMDB_API_KEY}",
        'top_rated': f"{TMDB_BASE_URL}/movie/top_rated?api_key={TMDB_API_KEY}",
        'upcoming': f"{TMDB_BASE_URL}/movie/upcoming?api_key={TMDB_API_KEY}&page=1",
        'recommendation': f"{TMDB_BASE_URL}/discover/movie?api_key={TMDB_API_KEY}&sort_by=vote_average.desc&with_genres={genre}&include_adult=false&page={random_num}"
    }

    def ambil(resultnum, categ, ur):
        response = requests.get(ur)
        response.raise_for_status()
        result = response.json()['results']
        categories[categ] = result[:resultnum]

    for category, url in endpoints.items():
        if category == section:
            ambil(20, category, url)

    return jsonify(categories)


@app.route("/filmpage/<id_film>/<title>", methods=['GET'])
def filmpage(id_film, title):
    list_cast = []
    dict_omdb = {}
    scrap_title = title.replace(" ", "+")
    # request api
    omdb_req = requests.get(
        f"http://www.omdbapi.com/?t={scrap_title}&plot=full&apikey={OMDB_KEY}")
    omdb_res = omdb_req.json()
    film_req = requests.get(
        f'{TMDB_BASE_URL}/movie/{id_film}?api_key={TMDB_API_KEY}')
    film_res = film_req.json()
    credits_req = requests.get(
        f'{TMDB_BASE_URL}/movie/{id_film}/credits?api_key={TMDB_API_KEY}')
    credits_res = credits_req.json()

    # olah data
    for i, k in omdb_res.items():
        if i == "Rated":
            dict_omdb[f"{i}"] = k
        if i == "Ratings":
            if len(k) == 1:
                continue
            else:
                dict_omdb[f"{i}"] = k
        if i == "Awards":
            dict_omdb[f"{i}"] = k
        if i == "Metascore":
            dict_omdb[f"{i}"] = k
        if i == "imdbRating":
            dict_omdb[f"{i}"] = k
        if i == "imdbVotes":
            dict_omdb[f"{i}"] = k

    max_cast_members = 5
    limited_cast = credits_res['cast'][:max_cast_members]
    for i in limited_cast:
        list_cast.append(i['name'])

    result = {
        'film': [film_res],
        'credits': list_cast,
        'rating': [dict_omdb]
    }
    print(result)
    return result


@app.route("/search/<keyword>", methods=['GET'])
def searchfilm(keyword):
    print(keyword)
    tmdb_req = requests.get(
        f"{TMDB_BASE_URL}/search/movie?query={keyword}&api_key={TMDB_API_KEY}&include_adult=false")
    tmdb_res = tmdb_req.json()['results']
    print(tmdb_res)
    return tmdb_res


@app.route("/favorit/post", methods=['POST'])
def postfavorit():
    data = request.get_json()
    id_film = data.get('id_film')
    email = data.get('email')
    cursor = conndb.cursor(dictionary=True)
    print(data)
    cursor.execute('SELECT data_film_user.favorit_film, data_film_user.id_data FROM akun_user INNER JOIN data_film_user ON akun_user.id_data = data_film_user.id_data WHERE akun_user.email=%s', (email,))
    datalist = cursor.fetchone()
    edit = datalist['favorit_film']
    if edit == None:
        return "None", 400
    if edit:
        nowlist = ast.literal_eval(edit)
        for i in nowlist:
            if id_film == i:
                return "failed", 401
        nowlist.append(id_film)
        jsonlist = json.dumps(nowlist)

        cursor.execute(
            'UPDATE data_film_user SET favorit_film = %s WHERE id_data = %s', (
                jsonlist, datalist['id_data'])
        )
        conndb.commit()
        return "success", 201
    else:
        return "failed", 404


@app.route("/favorit/get/<email>", methods=['GET'])
def getfavorit(email):
    filmlist = []
    cursor = conndb.cursor(dictionary=True)
    cursor.execute('SELECT data_film_user.favorit_film, data_film_user.id_data FROM akun_user INNER JOIN data_film_user ON akun_user.id_data = data_film_user.id_data WHERE akun_user.email=%s', (email,))
    datalist = cursor.fetchone()
    try:
        edit = datalist['favorit_film']
        if edit == None:
            return "None", 400
        if edit:
            nowlist = ast.literal_eval(edit)
            for i in nowlist:
                getdata = f'{TMDB_BASE_URL}/movie/{i}?api_key={TMDB_API_KEY}'
                req = requests.get(getdata)
                res = req.json()
                filmlist.append(res)
        return jsonify(filmlist)
    except Exception as error:
        print(error)
        return "failed", 400


@app.route("/favorite/delete", methods=['POST'])
def deletefavorite():
    cursor = conndb.cursor(dictionary=True)
    data = request.get_json()
    email = data.get("email")
    id_film = data.get("id_film")

    cursor.execute('SELECT data_film_user.favorit_film, data_film_user.id_data FROM akun_user INNER JOIN data_film_user ON akun_user.id_data = data_film_user.id_data WHERE akun_user.email=%s', (email,))
    datalist = cursor.fetchone()
    edit = datalist['favorit_film']

    if edit:
        nowlist = ast.literal_eval(edit)
        nowlist.remove(id_film)
        jsonlist = json.dumps(nowlist)

        cursor.execute(
            'UPDATE data_film_user SET favorit_film = %s WHERE id_data = %s', (
                jsonlist, datalist['id_data'])
        )

        conndb.commit()
        return "success", 201
    else:
        return "failed", 401


# @app.route("/bookmark/email/<email>", methods=['GET'])
# def bookmark(email):
#     cursor = conndb.cursor(dictionary=True)
#     # cursor.execute('SELECT id_data FROM akun_user WHERE email=%s', (email,))
#     # em = cursor.fetchone()
#     cursor.execute(
#         'SELECT data_film_user.bookmark_film FROM akun_user INNER JOIN data_film_user ON akun_user.id_data = data_film_user.id_data WHERE akun_user.email=%s', (email,))
#     id_data = cursor.fetchone()
#     if id_data['bookmark_film'] != None:
#         cursor.close()
#         id_data = None
#         return "success", 204
#     if id_data == None:
#         cursor.close()
#         id_data = None
#         return "None", 404


@app.route("/bookmark/post", methods=['POST'])
def postbookmark():
    try:
        data = request.get_json()
        id_film = data.get('id_film')
        email = data.get('email')
        cursor = conndb.cursor(dictionary=True)
        cursor.execute('SELECT data_film_user.bookmark_film, data_film_user.id_data FROM akun_user INNER JOIN data_film_user ON akun_user.id_data = data_film_user.id_data WHERE akun_user.email=%s', (email,))
        datalist = cursor.fetchone()
        edit = datalist['bookmark_film']
        print(edit)
        if edit == None:
            return "None", 400
        if edit:
            nowlist = ast.literal_eval(edit)
            for i in nowlist:
                if id_film == i:
                    print(i)
                    return "failed", 401
            nowlist.append(id_film)
            jsonlist = json.dumps(nowlist)

            cursor.execute(
                'UPDATE data_film_user SET bookmark_film = %s WHERE id_data = %s', (
                    jsonlist, datalist['id_data'])
            )
            conndb.commit()
            print("berhasil")
            return "success", 201
        else:
            return "failed", 404
    except:
        return "failed", 404


@app.route("/bookmark/get/<email>", methods=['GET'])
def getbookmark(email):
    filmlist = []
    cursor = conndb.cursor(dictionary=True)
    cursor.execute('SELECT data_film_user.bookmark_film, data_film_user.id_data FROM akun_user INNER JOIN data_film_user ON akun_user.id_data = data_film_user.id_data WHERE akun_user.email=%s', (email,))
    datalist = cursor.fetchone()
    try:
        edit = datalist['bookmark_film']
        if edit == None:
            return "None", 400
        if edit:
            nowlist = ast.literal_eval(edit)
            for i in nowlist:
                getdata = f'{TMDB_BASE_URL}/movie/{i}?api_key={TMDB_API_KEY}'
                req = requests.get(getdata)
                res = req.json()
                filmlist.append(res)
        return jsonify(filmlist)
    except:
        return "failed", 400


@app.route("/bookmark/delete", methods=['POST'])
def deletebookmark():
    cursor = conndb.cursor(dictionary=True)
    data = request.get_json()
    email = data.get("email")
    id_film = data.get("id_film")

    cursor.execute('SELECT data_film_user.bookmark_film, data_film_user.id_data FROM akun_user INNER JOIN data_film_user ON akun_user.id_data = data_film_user.id_data WHERE akun_user.email=%s', (email,))
    datalist = cursor.fetchone()
    edit = datalist['bookmark_film']
    print(edit)

    if edit:
        nowlist = ast.literal_eval(edit)
        nowlist.remove(id_film)
        jsonlist = json.dumps(nowlist)

        cursor.execute(
            'UPDATE data_film_user SET bookmark_film = %s WHERE id_data = %s', (
                jsonlist, datalist['id_data'])
        )

        conndb.commit()
        print("berhasil")
        return "success", 201
    else:
        return "failed", 401


@app.route("/newuser/checking", methods=['POST'])
def checking():
    data = request.get_json()
    email = data.get('email')
    cursor = conndb.cursor(dictionary=True)
    cursor.execute('SELECT data_film_user.preferensi FROM akun_user INNER JOIN data_film_user ON akun_user.id_data = data_film_user.id_data WHERE akun_user.email=%s', (email,))
    datalis3 = cursor.fetchone()
    edit3 = datalis3['preferensi']
    if edit3 == None:
        return "new", 201
    return "pass", 200


@app.route("/newuser", methods=['POST', 'GET'])
def newuser():
    cursor = conndb.cursor(dictionary=True)
    if request.method == 'GET':
        data = requests.get(
            f'{TMDB_BASE_URL}/genre/movie/list?api_key={TMDB_API_KEY}')
        datajson = data.json()["genres"]
        for genre in datajson:
            genre_id = genre['id']
            movie_url = f"{
                TMDB_BASE_URL}/discover/movie?api_key={TMDB_API_KEY}&with_genres={genre_id}&page=1"
            movie_response = requests.get(movie_url)

            if movie_response.status_code == 200:
                movies = movie_response.json()['results']
                if movies:
                    # Get the first movie poster
                    poster_path = movies[0]['poster_path']
                    poster_url = f"https://image.tmdb.org/t/p/w500{
                        poster_path}"
                    genre['poster_url'] = poster_url  # Add poster URL to genre
                else:
                    # Fallback placeholder if no movies found
                    genre['poster_url'] = 'https://via.placeholder.com/500'
            else:
                genre['poster_url'] = 'https://via.placeholder.com/500'
        return datajson
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        id_genre = data.get('id_genre')
        cursor.execute('SELECT data_film_user.preferensi, data_film_user.id_data FROM akun_user INNER JOIN data_film_user ON akun_user.id_data = data_film_user.id_data WHERE akun_user.email=%s', (email,))
        datalist = cursor.fetchone()
        try:
            edit = datalist['preferensi']
            if edit:
                nowlist = ast.literal_eval(edit)
                for i in nowlist:
                    if id_genre == i:
                        nowlist.remove(i)
                        jsonlist = json.dumps(nowlist)
                        cursor.execute(
                            'UPDATE data_film_user SET preferensi = %s WHERE id_data = %s', (
                                jsonlist, datalist['id_data'])
                        )
                        conndb.commit()
                        return "deleted", 202
                nowlist.append(id_genre)
                jsonlist = json.dumps(nowlist)
                cursor.execute(
                    'UPDATE data_film_user SET preferensi = %s WHERE id_data = %s', (
                        jsonlist, datalist['id_data'])
                )
                conndb.commit()
                return "berhasil", 201
            else:
                st = []
                stjson = json.dumps(st)
                cursor.execute(
                    'UPDATE data_film_user SET preferensi = %s WHERE id_data = %s', (
                        stjson, datalist['id_data'])
                )
                conndb.commit()
                cursor.execute(
                    'UPDATE data_film_user SET favorit_film = %s WHERE id_data = %s', (
                        stjson, datalist['id_data'])
                )
                conndb.commit()
                cursor.execute(
                    'UPDATE data_film_user SET bookmark_film = %s WHERE id_data = %s', (
                        stjson, datalist['id_data'])
                )
                conndb.commit()
                return "None", 203
        except Exception as e:
            print(e)
            return "gagal", 404
            # st = []
            # stjson = json.dumps(st)
            # cursor.execute(
            #     'UPDATE data_film_user SET preferensi = %s WHERE id_data = %s', (
            #         stjson, datalist['id_data'])
            # )
            # conndb.commit()
            # return "None", 203


@app.route("/user_data/<email>", methods=['GET'])
def user_data(email):
    data = []
    cursor = conndb.cursor()
    cursor.execute("SELECT data_film_user.preferensi FROM akun_user INNER JOIN data_film_user ON akun_user.id_data = data_film_user.id_data WHERE akun_user.email=%s", (email,))
    data_preferensi = cursor.fetchone()
    preferensi_list = ast.literal_eval(data_preferensi[0])

    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={
        TMDB_API_KEY}&language=en-US"
    genres = requests.get(url).json().get("genres", [])
    genre_lookup = {genre["id"]: genre["name"] for genre in genres}
    genre_names = []

    for genre_id in preferensi_list:
        genre_names.append(genre_lookup.get(genre_id, "Unknown Genre"))
    cursor.execute(
        "SELECT username, email, password FROM akun_user WHERE email = %s", (email,))
    akun = cursor.fetchone()

    for i in akun:
        data.append(i)
    result = ", ".join(genre_names)
    data.append(result)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
