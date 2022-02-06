from flask import Flask, render_template,redirect,url_for,flash,session,request
from werkzeug.utils import secure_filename
from datetime import date, datetime
import os,re

import json1,search_algorithm, send_email


if os.getcwd().split("\\")[-1] != "youtube clone": # os.getcwd() gets the folder the file runs on
    try:
        os.chdir("youtube clone") # change the diractory it works on to discord bot(now it start it from the "games and projects" directory)
    except: # can cause a error if it starts it from the folder
        pass

app = Flask(__name__)
app.name = "youtube clone"
app.secret_key = "y0utub3 cl0n3 @%^&*()_"

users = json1.reload_users()

videos = json1.reload_videos()
videos_by_genres = {}
existing_genres = None
def set_videos_by_genres():
    global existing_genres
    for video in videos:
        video_info = videos[video]
        video_info["id"] = video
        try:
            videos_by_genres[video_info["genre"]].append(video_info)
        except:
            videos_by_genres[video_info["genre"]] = [video_info]
    existing_genres1 = 'all family&action&comedy&drama&horror&science fiction&science&school related&collage related&sport&Tv related&movies related&movies&Tv shows&under 1 minute&garden&18+&16+&12+&5+'
    existing_genres1 = existing_genres1.split("&")
    for genre in existing_genres1:
        if genre not in videos_by_genres:
            videos_by_genres[genre] = []
    existing_genres = existing_genres1
set_videos_by_genres()
def append_video_to_by_genres(video_id):
    video_id = str(video_id)
    video_info = videos[video_id]
    video_info["id"] = video_id
    try:
        videos_by_genres[video_info["genre"]].append(video_info)
    except:
        videos_by_genres[video_info["genre"]] = [video_info]

#get_date datetime.now().strftime("%m/%d/%Y, %H:%M:%S")


@app.route("/home", methods=["POST","GET"])
@app.route("/", methods=["POST","GET"])
def home():
    login = False
    icon_color = None
    username = None
    first_letter = None
    try:
        username = session["username"]
        if session["login"] == True:
            login = True
            icon_color = users[username]["icon color"]
            first_letter = username[0].upper()
    except: pass

    videos_to_show1 = list(videos)[:100] # first 100
    videos_to_show = [[]] # all of the first 100 videos that need to be show(in lists of 4)
    for id in videos_to_show1:
        append_dict = videos[id]
        append_dict["id"] = id
        videos_to_show[-1].append(append_dict)
        if len(videos_to_show[-1]) >= 4:
            videos_to_show.append([])
    videos_by_genres_new = {}
    for genre in videos_by_genres:
        videos_by_genres_new[genre] = [[]]
    for genre in videos_by_genres:
        for video in videos_by_genres[genre]:
            videos_by_genres_new[genre][-1].append(video)
            if len(videos_by_genres_new[genre][-1]) >= 4:
                videos_by_genres_new[genre].append([])


    if request.method == "POST":
        to_search = request.form["to search"]
        if to_search == "": # if didnt fill the search input it just stays in the same url
            return render_template("home.html", login = login, icon_color=icon_color, first_letter = first_letter,
        all_videos_category = videos_to_show, all_videos_by_genre = videos_by_genres_new, genres = existing_genres)
        else: # will search
            videos_titles = {}
            videos_ids = []
            for id in videos:
                videos_titles[videos[id]["title"]] = id
                videos_ids.append(id)
            passed_titles,passed_titles_ids = search_algorithm.search(to_search,videos_titles) # the titles that passed the algorithm
            searched_videos = []
            for id in passed_titles_ids:
                append_dict = videos[id]
                append_dict["id"] = id
                searched_videos.append(append_dict)
            
            return render_template("show search results.html", login = login, icon_color=icon_color, first_letter = first_letter,
                                    searched=to_search, videos_info=searched_videos)
    else:
        return render_template("home.html", login = login, icon_color=icon_color, first_letter = first_letter,
        all_videos_category = videos_to_show, all_videos_by_genre = videos_by_genres_new, genres = "&".join(existing_genres))

def return_user_videos(user):
    # returns a list with more lists(max long = 4) that has the dicts of the videos
    # [  [video_dict,video_dict,video_dict,video_dict], [video_dict,video_dict,video_dict,video_dict]  ]
    every_list_length = 4
    user_videos_ids = users[user]["videos uploaded"]
    videos_list = [[]]
    for id in user_videos_ids:
        append_dict = videos[id]
        append_dict["id"] = id
        if len(videos_list[-1]) < every_list_length:
            videos_list[-1].append(append_dict)
        else:
            videos_list.append([append_dict])
    if len(videos_list[-1]) < 4:
        in_how_much = 4 - len(videos_list[-1])
        for a in range(in_how_much):
            videos_list[-1].append({})

    return videos_list

@app.route("/show page/<user>", methods=["POST","GET"])
def show_user_page(user):
    login = False
    icon_color = None
    username = None
    first_letter = None
    try:
        username = session["username"]
        if session["login"] == True:
            login = True
            icon_color = users[username]["icon color"]
            first_letter = username[0].upper()
    except: 
        flash("You must login before seeing other users pages")
        return redirect(url_for("login"))
    if username == user:
        return redirect(url_for("my_page"))
    
    if user not in users:
        error = "Username does not exist"
        return render_template("show page.html", login = login, icon_color=icon_color, first_letter = first_letter, error=error)
        

    if request.method == "POST":
        to_search = request.form["to search"]
        if to_search == "": # if didnt fill the search input it just stays in the same url
            subed = user in users[username]["subscribe to"]
            return redirect(request.url)
        else: # will search
            videos_titles = {}
            videos_ids = []
            for id in videos:
                videos_titles[videos[id]["title"]] = id
                videos_ids.append(id)
            passed_titles,passed_titles_ids = search_algorithm.search(to_search,videos_titles) # the titles that passed the algorithm
            searched_videos = []
            for id in passed_titles_ids:
                append_dict = videos[id]
                append_dict["id"] = id
                searched_videos.append(append_dict)
            
            return render_template("show search results.html", login = login, icon_color=icon_color, first_letter = first_letter,
                                    searched=to_search, videos_info=searched_videos)
    else:
        user_videos = return_user_videos(user)
        subed = user in users[username]["subscribe to"]
        subs = len(users[user]["subscribers"])
        return render_template("show page.html", login = login, icon_color=icon_color, first_letter = first_letter,user=user, user_videos=user_videos,
                            subed=subed, subs=subs)

@app.route("/sub/<user>")
def sub(user):
    username = None
    try:
        username = session["username"]
    except: 
        flash("You must login before doing anything")
        return redirect(url_for("login"))

    try:
        users[username]["subscribe to"].append(user)
        users[user]["subscribers"].append(username)
        json1.save_users(users)
    except: pass
    return redirect(url_for("show_user_page", user=user))
@app.route("/unsub/<user>")
def unsub(user):
    username = None
    try:
        username = session["username"]
    except: 
        flash("You must login before doing anything")
        return redirect(url_for("login"))
    
    try:
        users[username]["subscribe to"].remove(user)
        users[user]["subscribers"].remove(username)
        json1.save_users(users)
    except: pass
    return redirect(url_for("show_user_page", user=user))

@app.route("/my page", methods=["POST","GET"])
def my_page():
    login = False
    icon_color = None
    username = None
    first_letter = None
    try:
        username = session["username"]
        if session["login"] == True:
            login = True
            icon_color = users[username]["icon color"]
            first_letter = username[0].upper()
    except:
        flash("You must login before seeing your page")
        return redirect(url_for("login"))
    
    if request.method == "POST":
        to_search = request.form["to search"]
        if to_search == "": # if didnt fill the search input it just stays in the same url
            return redirect(request.url)
        else: # will search
            videos_titles = {}
            videos_ids = []
            for id in videos:
                videos_titles[videos[id]["title"]] = id
                videos_ids.append(id)
            passed_titles,passed_titles_ids = search_algorithm.search(to_search,videos_titles) # the titles that passed the algorithm
            searched_videos = []
            for id in passed_titles_ids:
                append_dict = videos[id]
                append_dict["id"] = id
                searched_videos.append(append_dict)
            
            return render_template("show search results.html", login = login, icon_color=icon_color, first_letter = first_letter,
                                    searched=to_search, videos_info=searched_videos)
    else:
        user_videos = return_user_videos(username)
        subs = len(users[username]["subscribers"])
        return render_template("my page.html", login = login, icon_color=icon_color, first_letter = first_letter, user_videos=user_videos, subs=subs)

@app.route("/sub to")
def show_who_user_subscribe_to():
    login = False
    icon_color = None
    username = None
    first_letter = None
    try:
        username = session["username"]
        if session["login"] == True:
            login = True
            icon_color = users[username]["icon color"]
            first_letter = username[0].upper()
    except:
        flash("You must login before doing anything")
        return redirect(url_for("login"))

    subed_to = users[username]["subscribe to"]
    sub_to_dict = {}
    for user in subed_to:
        sub_to_dict[user] = {
            "color":users[user]["icon color"],
            "subscribers":len(users[user]["subscribers"]),
        }
    return render_template("subscribe_to.html", login = login, icon_color=icon_color, first_letter = first_letter,subed_to = sub_to_dict)

@app.route("/my videos", methods=["POST","GET"])
def my_videos():
    login = False
    icon_color = None
    username = None
    first_letter = None
    user_videos = []
    try:
        username = session["username"]
        if session["login"] == True:
            login = True
            icon_color = users[username]["icon color"]
            first_letter = username[0].upper()
            for id in users[username]["videos uploaded"]:
                video = videos[id]
                video["id"] = id
                user_videos.append(video)
    except Exception as e: # didnt login
        flash("You must login before seeing your videos")
        return redirect(url_for("login"))

    if request.method == "POST":
        to_search = request.form["to search"]
        if to_search == "": # if didnt fill the search input it just stays in the same url
            return render_template("my videos.html", login = login, icon_color=icon_color, first_letter = first_letter)
        else: # will search
            videos_titles = {}
            videos_ids = []
            for id in videos:
                videos_titles[videos[id]["title"]] = id
                videos_ids.append(id)
            passed_titles,passed_titles_ids = search_algorithm.search(to_search,videos_titles) # the titles that passed the algorithm
            searched_videos = []
            for id in passed_titles_ids:
                append_dict = videos[id]
                append_dict["id"] = id
                searched_videos.append(append_dict)
            
            return render_template("show search results.html", login = login, icon_color=icon_color, first_letter = first_letter,
                                    searched=to_search, videos_info=searched_videos)

    return render_template("my videos.html", login = login, icon_color=icon_color, first_letter = first_letter, user_videos = user_videos)

@app.route("/del video/<id>")
def del_video(id):
    username = None
    try:
        username = session["username"]
    except Exception as e: # didnt login
        flash("You must login before deliting a video")
        return redirect(url_for("login"))
    
    post_user = videos[id]["uploader"]
    if post_user == username:
        users[username]["videos uploaded"].remove(id)
        video_info = videos[id]
        video_info["id"] = id
        videos_by_genres[videos[id]["genre"]].remove(video_info)
        videos.pop(id)
        try:
            os.remove(f"static\\videos\\{id}.mp4")
        except:pass
        json1.save_users(users)
        json1.save_videos(videos)
        return redirect(url_for("my_videos"))
    else:
        return redirect(url_for("home"))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {"mp4"}
def change_filename(filepath):
    # change the filename and returns the new id
    try:
        id = int(list(videos)[-1])+1
    except: id = 1
    os.rename(filepath,"static//videos//"+ str(id) + '.mp4')
    return id,"videos//"+ str(id) + '.mp4'
@app.route("/upload video", methods=["POST","GET"])
def upload_video():
    login = False
    icon_color = None
    username = None
    first_letter = None
    try:
        username = session["username"]
        if session["login"] == True:
            login = True
            icon_color = users[username]["icon color"]
            first_letter = username[0].upper()
    except: # didnt login
        flash("You must login before uploading video")
        return redirect(url_for("login"))

    if request.method == "POST":
        try:            
            if 'video file' not in request.files:
                flash("You didn't select a file")
                return redirect(request.url)
            file = request.files['video file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash("You didn't select a file")
                return redirect(request.url)
            if file and allowed_file(file.filename):
                try:
                    title = request.form["title"]
                    if title == "" or len(title) == title.count(" "):
                        flash("You must fill in the title textbox")
                        return redirect(request.url)
                    genre = request.form["genre"]

                    filename = secure_filename(file.filename)
                    file.save(os.path.join("static//videos//"  , filename))
                    id,new_path = change_filename("static//videos//" + filename)
                    users[username]["videos uploaded"].append(str(id))
                    videos[str(id)] = {
                        "uploader":username,
                        "title":title,
                        "uploaded at": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                        "views":0,
                        "genre":genre,
                        "path":new_path,
                        "comments":{}
                    }
                    json1.save_videos(videos)
                    json1.save_users(users)
                    append_video_to_by_genres(id)
                    return redirect(url_for("my_videos"))
                except Exception as e: # didnt put title
                    flash("You didnt fill in the title textbox")
                    return redirect(request.url)
            else:
                flash("You must upload a video not any other file type")
                return redirect(request.url)

        except Exception as e:
            pass
        
        try:
            to_search = request.form["to search"]
            if to_search == "": # if didnt fill the search input it just stays in the same url
                return render_template("home.html", login = login, icon_color=icon_color, first_letter = first_letter)
            else: # will search
                videos_titles = {}
            videos_ids = []
            for id in videos:
                videos_titles[videos[id]["title"]] = id
                videos_ids.append(id)
            passed_titles,passed_titles_ids = search_algorithm.search(to_search,videos_titles) # the titles that passed the algorithm
            searched_videos = []
            for id in passed_titles_ids:
                append_dict = videos[id]
                append_dict["id"] = id
                searched_videos.append(append_dict)
            
            return render_template("show search results.html", login = login, icon_color=icon_color, first_letter = first_letter,
                                    searched=to_search, videos_info=searched_videos)
        except:
            pass

        return redirect(request.url)
    else:
        return render_template("upload video.html", login = login, icon_color=icon_color, first_letter = first_letter)


def get_comments(comments1):
    comments_list = list(comments1)
    comments_list.reverse() # reverse the list so the modern ones will be before the older ones
    new_comments = {}
    for comment in comments_list:
        new_comments[comment] = comments1[comment]
    return new_comments
@app.route("/watch/<id>", methods=["POST","GET"])
def watch_video(id):
    login = False
    icon_color = None
    username = None
    first_letter = None
    try:
        username = session["username"]
        if session["login"] == True:
            login = True
            icon_color = users[username]["icon color"]
            first_letter = username[0].upper()
    except: # didnt login
        flash("You must login before seeing video")
        return redirect(url_for("login"))
    if id not in videos:
        error = "Video does not exists"
        return render_template("watch video.html", login = login, icon_color=icon_color, first_letter = first_letter, error=error)

    if request.method == "POST":
        try:
            comment = request.form["comment"]
            if comment != "":
                try:
                    comment_id = str(int(list(videos[id]["comments"])[-1]) + 1)
                except:
                    comment_id = "1"
                by = username
                post_date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                videos[id]["comments"][comment_id] = {
                    "comment":comment,
                    "by":by,
                    "date":post_date
                }
                json1.save_videos(videos)
        except: pass

        try:
            to_search = request.form["to search"]
        except: return redirect(request.url)
        if to_search == "": # if didnt fill the search input it just stays in the same url
            comments = get_comments(videos[id]["comments"])
            video = videos[id]
            video["id"] = id
            return render_template("watch video.html", login = login, icon_color=icon_color, first_letter = first_letter, video=video, username=username, comments = comments)
        else: # will search
            videos_titles = {}
            videos_ids = []
            for id in videos:
                videos_titles[videos[id]["title"]] = id
                videos_ids.append(id)
            passed_titles,passed_titles_ids = search_algorithm.search(to_search,videos_titles) # the titles that passed the algorithm
            searched_videos = []
            for id in passed_titles_ids:
                append_dict = videos[id]
                append_dict["id"] = id
                searched_videos.append(append_dict)
            
            return render_template("show search results.html", login = login, icon_color=icon_color, first_letter = first_letter,
                                    searched=to_search, videos_info=searched_videos)
    
    videos[id]["views"] += 1
    json1.save_videos(videos)
    video = videos[id]
    video["id"] = id
    comments = get_comments(videos[id]["comments"])

    return render_template("watch video.html", login = login, icon_color=icon_color, first_letter = first_letter, video=video, username=username, comments = comments)
@app.route("/del comment/<video_id>/<id>")
def del_video_comment(video_id,id):
    username = None
    try:
        username = session["username"]
    except: # didnt login
        return redirect(url_for("login"))

    comment = videos[video_id]["comments"][id]
    comment["id"] = id
    if username == comment["by"]:
        videos[video_id]["comments"].pop(id)
        json1.save_videos(videos)
        return redirect(url_for("watch_video", id=video_id))
    else:
        return redirect(url_for("watch_video", id=video_id))

@app.errorhandler(404)
def page_404(e):
    login = False
    icon_color = None
    username = None
    first_letter = None
    try:
        username = session["username"]
        if session["login"] == True:
            login = True
            icon_color = users[username]["icon color"]
            first_letter = username[0].upper()
    except: # didnt login
        return redirect(url_for("login"))
    return render_template("404 page.html", login = login, icon_color=icon_color, first_letter = first_letter)

@app.route("/login", methods=["POST","GET"])
def login():
    login = False
    try:
        if session["login"] == True:
            login = True
            return redirect(url_for("home"))
    except: pass

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "" or password == "":
            flash("You must fill in username and password textboxes")
            return render_template("login.html", login = login, username=username,password=password)
        else:
            try:
                if users[username]["password"] == password:
                    session["login"] = True
                    session["username"] = username
                    json1.save_users(users)
                    return redirect(url_for("home"))
                else:
                    flash("wrong password")
                    return render_template("login.html", login = login, username=username,password=password)
            except:
                flash("username does not exist")
                return render_template("login.html", login = login, username=username,password=password)
    else:
        return render_template("login.html",login = login)

@app.route("/forgot password", methods=["POST","GET"])
def forgot_password():
    if request.method == "POST":
        username = request.form["username"]
        flashed = False
        if username == "" or len(username) == username.count(" "):
            flash("You must fill the username textbox")
            flashed = True
        if username not in users and username != "" and len(username) != username.count(" "):
            flash("The username does not exist")
            flashed = True
        if flashed == False:
            send_email.send(
                users[username]["email"],
                "username: " + username + 
                "\npassword: " + users[username]["password"] + 
                "\nemail: " + users[username]["email"] + 
                "\nuploaded " + str(len(users[username]["videos uploaded"])) + " videos" +
                "\nhas " + str(len(users[username]["subscribers"])) + " subscribers" + 
                "\nsubscribe to " + str(len(users[username]["subscribe to"])) + " people"
            )
            flash("1An email sent to you with your password")
        return redirect(request.url)
    else:
        return render_template("forgot password.html")

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
def check_email(email):
 
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        return "good"
 
    else:
        return "not good"

@app.route("/create user", methods=["POST","GET"])
def create_user():
    login = False
    try:
        if session["login"] == True:
            login = True
            return redirect(url_for("home"))
    except: pass
        
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_confirm = request.form["password confirm"]
        email = request.form["email"]
        icon_color = request.form["icon color"]
        if username == "" or password == "" or password_confirm == "" or email == "":
            flash("you must fill all of the textboxes")
            return render_template("create user.html",login = login,  username=username, password=password, password_confirm=password_confirm,email=email, icon_color=icon_color)
        else:
            if password != password_confirm:
                flash("Your password does not match to password confirm")
                return render_template("create user.html",login = login,  username=username, password=password, password_confirm=password_confirm,email=email, icon_color=icon_color)
            else: # all good(create user)
                if username in users:
                    flash("username is catch")
                    return render_template("create user.html",login = login,  username=username, password=password, password_confirm=password_confirm,email=email, icon_color=icon_color)
                else: # all good
                    if check_email(email) == "not good":
                        flash("Email is not valid")
                        return render_template("create user.html",login = login,  username=username, password=password, password_confirm=password_confirm,email=email, icon_color=icon_color)
                    else:
                        users[username] = {
                            "username":username, 
                            "password":password,
                            "email":email, 
                            "icon color":icon_color,

                            "subscribe to":[], # list with the people he follows after
                            "subscribers":[], # the people that follows him

                            "videos uploaded":[], # ids of the videos he uploaded(not names cause a few videos can have the same name)
                            }
                        session["login"] = True
                        session["username"] = username
                        json1.save_users(users)
                        return redirect(url_for("home"))
    else:
        return render_template("create user.html",login = login)

@app.route("/logout")
def logout():
    try:
        session.pop("login")
        session.pop("username")
    except: pass
    return redirect(url_for("home"))

app.run(debug=True)