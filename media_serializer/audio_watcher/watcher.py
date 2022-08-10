import glob
from argparse import ArgumentParser
from os import listdir
from os.path import abspath, isfile, join
# import numpy

import ffmpeg
import pandas as pd
from watchfiles import watch

import watcher

parser = ArgumentParser(
    description="Watch a directory and construct an XML file",
    add_help=True,
    usage="[options] directory")
parser.add_argument("--name", dest="name", default="leah", help='name of the file')
parser.add_argument("--output", dest="output", default="video.xml", help='video output')
parser.add_argument("--extension", "-e", nargs="*", default=["mp4"], help='extension of the file')
parser.add_argument("directory", metavar="directory", help='directory')

args = parser.parse_args()

extensions = args.extension
directory = abspath(args.directory)
output = abspath(args.output)

clipsArray = []

# First read the files in the directory
existing_files = []
for ext in extensions:
    glob_str = "{}/*.{}".format(directory, ext)
    existing_files.extend(glob.glob(glob_str))

df = pd.DataFrame()
media = df.values
print('media = {}'.format(media))

for f in existing_files:
    file_df = watcher.process_file(f)
    df = pd.concat([df, file_df])

xml = watcher.to_xml(args.name, df)
print(xml.decode('ascii'))

# Todo: Ensure/Test output directory exists

with open(output, 'w') as f:
    f.write(xml.decode("ascii"))

    
# for changes in watch(directory):
    # print(changes)


