from tkinter import *
from tkinter import filedialog
import subprocess, json, os

app =Tk()
app.title("YouTube Downloader Plus")
app.geometry("800x200")
app.minsize(width=700, height=150)
app.maxsize(width=1000, height=2000)



###on start#######################
def set_download_location():
    global downloads_location
    new_location = filedialog.askdirectory(title="Select Download Folder")

    if new_location:
        downloads_location = new_location
        settings["download_location"] = downloads_location

        with open(settings_path, 'w') as f:
            json.dump(settings, f, indent=4)

        downloads_location_info.config(text=downloads_location)


directory = os.path.dirname(os.path.abspath(__file__))
settings_path = os.path.join(directory, "settings.json")

default_settings = {
    "download_location": ""
}

if not os.path.exists(settings_path):
    print("No settings file detected. Creating one...")
    with open(settings_path, 'w') as f:
        json.dump(default_settings, f, indent=4)



with open(settings_path, 'r') as settings_file:
    settings = json.load(settings_file)

downloads_location = settings["download_location"]

if downloads_location=="":
    app.after(100, set_download_location)



###functions#######################
def search():
    url = url_input.get().split("?si=")[0].split("&list=")[0].replace("https://www.youtube.com/watch?v=", "").replace("https://youtu.be/", "")
    subprocess.run(["yt-dlp", "-F", website + url], text=True)

def download():
    if downloads_location!="":
        url = url_input.get().split("?si=")[0].split("&list=")[0].replace("https://www.youtube.com/watch?v=", "").replace("https://youtu.be/", "")
        format = format_input.get()
        name = name_input.get()

        if name!="":
            if "." not in name:
                name = name + ".%(ext)s"
            else:
                print("Custom extension provided. File may not open or work properly.")
        else:
            print("No name provided. Title from site will be used.")

        #os.chdir(downloads_location)
        print("Video will be saved as:", name)
        subprocess.run(["yt-dlp", "-f", format, *(["-o", name] if name!="" else []), website + url], cwd=downloads_location, shell=True, text=True)
        #os.chdir(directory)
    else:
        print("Set a downlaods location first!")




###elements#######################
website = 'https://www.youtube.com/watch?v='

frame1 = Frame(app)
frame1.pack(side=LEFT, fill=Y, expand=True)
subframe1 = Frame(frame1)
subframe1.pack(side=LEFT, expand=True)
url_input_label = Label(subframe1, text="Video URL/UID:").pack()
url_input = Entry(subframe1); url_input.pack()
search_button = Button(subframe1, text="Search", command=search).pack(padx=10, pady=10)

frame2 = Frame(app)
frame2.pack(side=LEFT, fill=Y, expand=True)
subframe2 = Frame(frame2)
subframe2.pack(side=LEFT, expand=True)
format_input_label = Label(subframe2, text="Arguments for format(1+2):").pack()
format_input = Entry(subframe2); format_input.pack()
name_label = Label(subframe2, text="File Name").pack()
name_input = Entry(subframe2); name_input.pack()
download_button = Button(subframe2, text="Download", command=download).pack(padx=10, pady=10)

frame3 = Frame(app)
frame3.pack(side=LEFT, fill=Y, expand=True)
subframe3 = Frame(frame3)
subframe3.pack(side=LEFT, expand=True)
downloads_location_label = Label(subframe3, text="Downloads location:").pack()
downloads_location_info = Label(subframe3, text=downloads_location, bg="whitesmoke", width=20, wraplength=150); downloads_location_info.pack()
change_button = Button(subframe3, text="Change location", command=set_download_location).pack(padx=10, pady=10)


app.mainloop()