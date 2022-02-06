import json,os

if os.getcwd().split("\\")[-1] != "youtube clone": # os.getcwd() gets the folder the file runs on
    try:
        os.chdir("youtube clone") # change the diractory it works on to discord bot(now it start it from the "games and projects" directory)
    except: # can cause a error if it starts it from the folder
        pass


users_path = "static/users.json"

def save_users(users):
    # saves in the json file
    what_to_save = {"users":[users]}
    with open(users_path, "w") as file:
        json.dump(what_to_save, file,  indent=4)

def reload_users():
    # returns the users dict
    with open(users_path) as file:
        data = json.load(file)
        data = data["users"][0]
        return data


videos_path = "static/videos.json"

def save_videos(users):
    # saves in the json file
    what_to_save = {"videos":[users]}
    with open(videos_path, "w") as file:
        json.dump(what_to_save, file,  indent=4)

def reload_videos():
    # returns the users dict
    with open(videos_path) as file:
        data = json.load(file)
        data = data["videos"][0]
        return data