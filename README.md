# Simple YouTube downloader

Download your favorite YouTube videos easily from only the URL. Created with [Pytube](https://pytube.io/en/latest/)

# How to use

When executed, the program asks you the URL of the video you want to download. The URL has to begin with *https://www.youtube.com* to continue or else it asks you again.
Then you need to wait for the video to be downloaded. That's it!
The videos are downloaded directly into the project folder where the main.py is. If you download the same video (same name) 2 times it will automatically overwrite the previous one.

# How to install

### Windows

 * Installing Pytube

Open the Terminal and run the following:

```sh
pip install pytube
```

 * Installing ffmpeg

watch this video to install ffmpeg on your computer -> [here](https://www.youtube.com/watch?v=DMEP82yrs5g&ab_channel=Infinetsoftsolutions) (the video is not mine)

Then open the Terminal and run the following:

```sh
pip install ffmpeg-python
```

### Mac

 * Installing Pytube

Open the Terminal and run the following:

```sh
pip3 install pygame
```

* Installing ffmpeg

watch this video to install ffmpeg on your computer -> [here](https://www.youtube.com/watch?v=nmrjRqEIgGc&ab_channel=DavidHelmuth) (the video is not mine)

Then open the Terminal and run the following:

```sh
pip3 install ffmpeg-python
```
# What can be done to make it better

 * make a simple UI with Tkinter ( I am working on it ).
 * being able to download multiple videos like a download queue.
 * being able to choose to download only the audio (for music for example ).
 * being able to select different resolutions for the video.
