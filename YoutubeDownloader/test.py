from pytubefix import YouTube
import os
import ffmpeg

url = "https://www.youtube.com/watch?v=R4WyNWL83IU&ab_channel=StayTrueToTheGizzame"

vid = YouTube(url)

def video_stream_choice(vid):
    choice = int(input("audio(1) or video(2)?: "))
    if 0 < choice < 3:
        if choice == 1:
            stream = vid.streams.filter(only_audio=True).order_by('abr').desc()
            vid_stream = stream[0]
            print(vid_stream)
            vid.register_on_progress_callback(on_download_progress)
            vid_stream.download(mp3=True)

        if choice == 2:
            streams = vid.streams.filter(progressive=False, file_extension='mp4', type="video").order_by(
                'resolution').desc()
            video_stream = streams[0]

            streams = vid.streams.filter(progressive=False, file_extension='mp4', type="audio").order_by(
                'abr').desc()
            audio_stream = streams[0]

            vid.register_on_progress_callback(on_download_progress)

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
            ffmpeg.output(ffmpeg.input(audio_filename), ffmpeg.input(video_filename), output_filename, vcodec="copy",
                          acodec="copy", loglevel="quiet").run(overwrite_output=True)
            print("finished")

            print("")

            print('Deleting temporary files...')
            os.remove(audio_filename)
            os.remove(video_filename)
            print('finished')


def on_download_progress(stream, chunk, bytes_remaining):
    """take the filesize - bytes remaining, convert it to percents
    and show the percentage of download progress"""

    bytes_downloaded = stream.filesize - bytes_remaining
    percent = bytes_downloaded * 100 / stream.filesize
    print(f"Download Progress: {int(percent)}%")

print("Video title:", vid.title)  # show the title of the video
print("Views:", vid.views)  # show the number of views of the video
print("")

video_stream_choice(vid)




