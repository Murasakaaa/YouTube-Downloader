import tkinter as tk
from tkinter import ttk
from pytubefix import YouTube
import os
import ffmpeg

# create the window
window = tk.Tk()
window.title('YTDownloader')
window.geometry('240x280')
window.resizable(width=False, height=False)

choice = 0
def audio_only():
    """set the user choice on 1 for audio choice"""
    global choice
    choice = 1
    current_choice.config(text="Current choice: mp3")
    label4.config(text='')

def normal_vid():
    """set the user choice on 2 for video choice"""
    global choice
    choice = 2
    current_choice.config(text="Current choice: mp4")
    label4.config(text='')

def dl_video():
    process(choice)

def process(choice):
    """gets the url the user entered and download the correct format according to the user choice"""
    url = enter_url.get()
    vid = YouTube(url)
    label2.config(text=f"title: {vid.title}")   # shows video title
    label3.config(text=f"views: {vid.views}")   # shows video's number of views
    c = choice
    if c == 1:
        progress['value'] = 0
        stream = vid.streams.filter(only_audio=True).order_by('abr').desc()  # filters the audio streams
        vid_stream = stream[0]  # choose the best audio stream
        print(vid_stream)
        progress['value'] = 50
        vid.register_on_progress_callback(on_download_progress)
        vid_stream.download(mp3=True)   # download the audio stream
        print('finished')
        progress['value'] = 100

    if c == 2:
        progress['value'] = 0
        progress['value'] = 10
        vid.register_on_progress_callback(on_download_progress)
        streams = vid.streams.filter(progressive=False, file_extension='mp4', type="video").order_by('resolution').desc()   # filters the video streams
        video_stream = streams[0]   # choose the best video stream
        streams = vid.streams.filter(progressive=False, file_extension='mp4', type="audio").order_by('abr').desc()  # filters the audio streams
        audio_stream = streams[0]   # choose the best audio stream

        progress['value'] = 30
        print("Video downloading...")
        video_stream.download("video")  # downloading the video part in the "video" folder
        print("finished")

        progress['value'] = 50
        print("Audio downloading...")
        audio_stream.download("audio")  # downloading the audio part in the "audio" folder
        print("finished")

        # --- Combining the two files into 1 video with audio ---
        # ffmpeg can't use streams as it is a pytube thing, so it uses filenames
        audio_filename = os.path.join("audio", video_stream.default_filename)
        video_filename = os.path.join("video", video_stream.default_filename)
        output_filename = video_stream.default_filename
        progress['value'] = 70
        print("Creating the final file...")
        ffmpeg.output(ffmpeg.input(audio_filename), ffmpeg.input(video_filename), output_filename, vcodec="copy",acodec="copy", loglevel="quiet").run(overwrite_output=True)
        print("finished")
        progress['value'] = 80

        # removes the separated parts
        progress['value'] = 85
        print('Deleting temporary files...')
        progress['value'] = 90
        os.remove(audio_filename)
        progress['value'] = 95
        os.remove(video_filename)
        print('finished')
        progress['value'] = 100
    if c == 0:
        label4.config(text="don't forget to choose the video format")
def on_download_progress(stream, chunk, bytes_remaining):
    """take the filesize - bytes remaining, convert it to percents
    and show the percentage of download progress"""

    bytes_downloaded = stream.filesize - bytes_remaining
    percent = bytes_downloaded * 100 / stream.filesize
    print(f"Download Progress: {int(percent)}%")

window.columnconfigure(0, weight=2)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)
window.columnconfigure(5, weight=2)
window.columnconfigure(6, weight=2)
# widgets
label0 = ttk.Label(text='mp3 or mp4?')
label0.grid(row=0, column=0, pady=5, padx=5, sticky='w')

# buttons to choose to download audio only or normal videos
audio_choice = ttk.Button(window, text="mp3",command=audio_only)
audio_choice.grid(row=1,column=0, pady=5, padx=5)

video_choice = ttk.Button(window, text="mp4",command=normal_vid)
video_choice.grid(row=1,column=1, pady=5, padx=5)

# show the last choice you made with the buttons above
current_choice = ttk.Label(window,text="Current choice : ")
current_choice.grid(column=0, row=2, columnspan=3, sticky='w')

ttk.Separator(window, orient='horizontal').place(x=0, y=85, relwidth=1)


label1 = ttk.Label(text="Video link:")
label1.grid(column=0, row=3, pady=5, padx=5, sticky='w')

# this is where you enter the video url
enter_url = ttk.Entry(window)
enter_url.grid(column=0, row=4, pady=5, padx=5)

# download button
dl_button = ttk.Button(window, text='download', command=dl_video)
dl_button.grid(column=1, row=4, pady=5, padx=5)

# video infos
# title
label2 = ttk.Label(text="title: ")
label2.grid(column=0, row=5, padx=5, sticky='w', columnspan=3)
# number of views
label3 = ttk.Label(text="views: ")
label3.grid(column=0, row=6, padx=5, sticky='w', columnspan=3)

# download status
progress = ttk.Progressbar(window, orient='horizontal', length=200, mode='determinate')
progress.place(x=20, y=200)

# if the user enter an url without choosing the format it says it here
label4 = ttk.Label(window, text='')
label4.place(x=20, y=240)

# run
window.mainloop()
