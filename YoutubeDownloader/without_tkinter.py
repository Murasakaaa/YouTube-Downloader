# YouTube downloader -> can't download age restricted video bcause you have to log in to yt
from pytubefix import YouTube
import os
import ffmpeg

base_ytb_url = "https://www.youtube.com"

# check if the url begin with "https://www.youtube.com"
# if not then it shows an error and ask you the url again
# Also if the url is only "https://www.youtube.com", it will ask you the url again
def get_video_url_from_user():

    while True:
        u = input("url of the video you want to download: ")
        if u == base_ytb_url:  # if the url is YouTube's url it is not working
            print(".")
        elif u.lower().startswith(base_ytb_url):  # if u[:len(base_ytb_url)] == base_ytb_url:
            return u
        print("The url is not valid. You have to enter a YouTube url.")

# asks the user to choose between downloading a mp3 or a mp4
# if the user enter another number than the one for the choice it asks again
def choice():
    while True:
        choice = int(input("mp3(1) or mp4(2)?: "))
        if choice == 1 or choice == 2:
            return choice
        print('enter correct choice')

def dl_video():
    url = get_video_url_from_user()  # asks the user for the video url
    vid = YouTube(url)
    print("Video title: ", vid.title)  # show the title of the video
    c = choice()    # asks the user to choose between mp3 or mp4
    if c == 1:
        print('downloading...')
        stream = vid.streams.filter(only_audio=True).order_by('abr').desc()  # filters the audio streams
        vid_stream = stream[0]      # choose the best audio stream
        print(vid_stream)
        vid.register_on_progress_callback(on_download_progress)
        vid_stream.download(mp3=True)  # download the audio stream
        print('finished')

    if c == 2:
        vid.register_on_progress_callback(on_download_progress)
        streams = vid.streams.filter(progressive=False, file_extension='mp4', type="video").order_by('resolution').desc()  # filters the video streams
        video_stream = streams[0]   # choose the best video stream

        streams = vid.streams.filter(progressive=False, file_extension='mp4', type="audio").order_by('abr').desc()  # filters the audio streams
        audio_stream = streams[0]  # choose the best audio stream
        print("Video downloading...")
        video_stream.download("video")  # downloading the video part in the "video" folder
        print("finished")

        print("")

        print("Audio downloading...")
        audio_stream.download("audio")  # downloading the audio part in the "audio" folder
        print("finished")

        print("")

        # --- Combining the two files into 1 video with audio ---
        # ffmpeg can't use streams as it is a pytube thing, so it uses filenames
        audio_filename = os.path.join("audio", video_stream.default_filename)
        video_filename = os.path.join("video", video_stream.default_filename)
        output_filename = video_stream.default_filename

        print("Creating the final file...")
        ffmpeg.output(ffmpeg.input(audio_filename), ffmpeg.input(video_filename), output_filename, vcodec="copy",acodec="copy", loglevel="quiet").run(overwrite_output=True)
        print("finished")

        print("")

        # removes the separated parts
        print('Deleting temporary files...')
        os.remove(audio_filename)
        os.remove(video_filename)
        print('finished')

# show the progress
def on_download_progress(stream, chunk, bytes_remaining):
    """take the filesize - bytes remaining, convert it to percents
    and show the percentage of download progress"""

    bytes_downloaded = stream.filesize - bytes_remaining
    percent = bytes_downloaded * 100 / stream.filesize
    print(f"Download Progress: {int(percent)}%")

dl_video()
