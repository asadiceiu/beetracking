import pafy
import sys

'''
This script downloads youtube video from youtube. You have to supply the url of the video
Usage: >> python ytdownloader.py <url>

But first, you have to install paffy and youtube_dl using pip

pip install paffy youtube_dl

'''

if __name__=="__main__":
    print(sys.argv)
    if len(sys.argv)<2:
        print("Usage: python pafycheck.py <youtubeurl>")
    else:
        
        url = sys.argv[1] #'https://www.youtube.com/watch?v=VnrfPgAqbY8'

        video = pafy.new(url)

        print("Title: ", video.title)
        print("Duration: ", video.duration)
        print("Likes: ", video.likes, "Dislikes: ",video.dislikes)

        bestVideo = video.getbest()
        bestVideo.download(quiet=False)