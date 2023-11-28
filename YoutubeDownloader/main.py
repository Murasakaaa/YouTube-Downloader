# YouTube downloader -> can't download age restricted video bcause you have to log in to ytb
# module pyutbe

from pytube import YouTube

url = "https://www.youtube.com/watch?v=Rd8ap3GcAyA&ab_channel=Gawx2"


# check if the url begin with "https://www.youtube.com"
# if not then it shows an error and ask you the url again
# Also if the url is only "https://www.youtube.com", it will ask you the url again

base_ytb_url = "https://www.youtube.com"
'''while True:
    url = input("url of the video you want to download: ")
    # if url[:len(base_ytb_url)] == base_ytb_url:
    if url == base_ytb_url:
        print(".")
    elif url.lower().startswith(base_ytb_url):
        break
    print("The url is not valid. You have to enter a YouTube url.")
'''

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

print("")
print("CHOICE OF RES")
streams = youtube_video.streams.filter(progressive=True, file_extension='mp4')
index = 1
for stream in streams:  # show all the streams of the video
    print(f'{index} - {stream.resolution}')
    index +=1

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



itag = streams[res_num_int-1].itag

# print("itag: ", itag)

stream = youtube_video.streams.get_by_itag(itag)  # for a specific stream
# stream = youtube_video.streams.get_highest_resolution()  # to get the stream with the highest res
print("Downloading...")

stream.download()  # downloading the stream
print("finished")
