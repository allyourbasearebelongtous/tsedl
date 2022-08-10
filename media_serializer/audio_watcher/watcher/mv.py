from moviepy.editor import *
from watcher import *
from watcher.processor import *
import pathlib
import subprocess
import ffmpeg
import sys
from pprint import pprint # for printing Python dictionaries in a human-readable way
from converter import Converter
from tinytag import TinyTag


conv = Converter()


movieclips = []
print("mv.py = %", movieclips)

def edit_clips(video_file):
    print("this is from mv %", video_file)
   
    #probe_file(str(video_file))
    
    clips = []
    for i in video_file:
        #clips = []
        
        #clips.append(i)
        
        #print(video_file)            
        #print("i = %", clips)
        
        ## Set FPS ##
        #video_file.set_fps(30)
        
        
        clipList = [VideoFileClip(c) for c in video_file]
        print(clipList)
        
        videoExt = pathlib.Path(i).suffix
        print(videoExt)
        
        ## add clip fps ##
        for vid in clipList:
            vid.set_fps(29.97)
            print(vid)
            #metad = TinyTag.get(vid)
            #print("Bitrate: " + str(metad.bitrate))
        
    
    if len(clipList) <= len(video_file):
        write_final_clips(clipList)    
        
        
        
    #final_video = concatenate_videoclips(clipList)
    #final_video.write_videofile("/Users/leahlerner/Movies/output.mp4")
    
    
def write_final_clips(final_video):
    final_video = concatenate_videoclips(final_video)
    final_video.write_videofile("/Users/leahlerner/Movies/output.mp4", fps = 29.97)
    
def video_options(video_info):
    videoInfo = subprocess.run("ffmpeg -i %", video_info)
    print(videoInfo)

def ffmpeg_probe(clip):
    # read the audio/video file from the command line arguments
    clipFile = sys.argv[1]
    # uses ffprobe command to extract all possible metadata from the media file
    pprint(ffmpeg.probe(clipFile)["streams"])

def probe_file(filename):
    cmnd = ['ffprobe', '-show_format', '-pretty', '-loglevel', 'quiet', filename]
    p = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(filename)
    out, err =  p.communicate()
    print("==========output==========")
    print(out)
    if err:
        print("========= error ========")
        print(err)
        
def pvc(videoFile):
    info = conv.probe(videoFile)

    convert = conv.convert('test/test1.avi', 'test/test1.mp4', {
        'format': 'mp4',
        'audio': {
            'codec': 'aac',
            'samplerate': 11025,
            'channels': 2
        },
        'video': {
            'codec': 'hevc',
            'width': 1280,
            'height': 720,
            'fps': 29.97
        }})

    for timecode in convert:
        print(f'\rConverting ({timecode:.2f}) ...')


