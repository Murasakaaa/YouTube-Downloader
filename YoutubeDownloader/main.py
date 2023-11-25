# YouTube downloader -> can't download age restricted video bcause you have to log in to ytb
# module pyutbe

from pytube import YouTube

url = "https://www.youtube.com/watch?v=Rd8ap3GcAyA&ab_channel=Gawx2"


def on_download_progress(stream, chunk, bytes_remaining):
    """take the filesize - bytes remaining, convert it to percents
    and show the percentage of download progress"""

    bytes_downloaded = stream.filesize - bytes_remaining
    percent = bytes_downloaded * 100 / stream.filesize
    print(f"Download Progress: {int(percent)}%")


youtube_video = YouTube(url)

youtube_video.register_on_progress_callback(on_download_progress)  # calls the function when download progress

print("Video title:", youtube_video.title)  # show the title of the video
print("Views:", youtube_video.views)  # show the number of views of the video

print("Streams")
for stream in youtube_video.streams.fmt_streams:  # show all the streams of the video
    print(" ", stream)

# stream = youtube_video.streams.get_by_itag(18) # for a specific stream
stream = youtube_video.streams.get_highest_resolution()  # to get the stream with the highest res
print("Downloading...")

stream.download()  # downloading the stream
print("finished")

