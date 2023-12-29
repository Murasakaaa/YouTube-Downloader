# YouTube downloader -> can't download age restricted video bcause you have to log in to ytb
# module pytube

from pytube import YouTube
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

def get_video_itag_from_user(streams):
    print("CHOICE OF RES")

    index = 1
    for stream in streams:  # show all the streams of the video
        print(f'{index} - {stream.resolution}')
        index += 1
    # We make sure the user is entering the right number
    while True:
        res_num = input("Choose a resolution: ")
        if res_num == "":
            print("Error. Please enter a number.")
        else:
            try:
                res_num_int = int(res_num)
            except:
                print("Error. Please enter a number.")
            else:
                if not 1 <= res_num_int <= len(streams):
                    print(f'Error. You have to enter a number between 1 and {len(streams)}')
                else:
                    break

    itag = streams[res_num_int - 1].itag
    return itag

url = get_video_url_from_user()

def on_download_progress(stream, chunk, bytes_remaining):
    """take the filesize - bytes remaining, convert it to percents
    and show the percentage of download progress"""

    bytes_downloaded = stream.filesize - bytes_remaining
    percent = bytes_downloaded * 100 / stream.filesize
    print(f"Download Progress: {int(percent)}%")


youtube_video = YouTube(url)

youtube_video.register_on_progress_callback(on_download_progress)  # calls the function when download progress
print("")
print("Video title:", youtube_video.title)  # show the title of the video
print("Views:", youtube_video.views)  # show the number of views of the video
print("")

streams = youtube_video.streams.filter(progressive=False, file_extension='mp4', type="video").order_by('resolution').desc()
video_stream = streams[0]

streams = youtube_video.streams.filter(progressive=False, file_extension='mp4', type="audio").order_by('abr').desc()
audio_stream = streams[0]

# -----
# itag = get_video_itag_from_user(streams)
# stream = youtube_video.streams.get_by_itag(itag)  # for a specific stream
# -----

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
ffmpeg.output(ffmpeg.input(audio_filename), ffmpeg.input(video_filename), output_filename, vcodec="copy", acodec="copy", loglevel="quiet").run(overwrite_output=True)
print("finished")

print("")

print('Deleting temporary files...')
os.remove(audio_filename)
os.remove(video_filename)
print('finished')
