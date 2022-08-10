from multiprocessing.managers import ListProxy
import uuid

import ffmpeg as ff
import pandas as pd
from lxml import etree as et
import watcher.mv as movie
import numpy as np



def process_file(video_file):
  """
  Process a video file into a dataframe
  """
  # Read metadata
  params = ff.probe(video_file)
  format = params["format"]

  ## Get interesting data
  start_time = format["start_time"]
  duration = format["duration"]
  end_time = float(start_time) + float(duration)

  metadata = {
        "timecode_in":str(start_time),
	      "duration":duration,
        "timecode_out":str(end_time),
	      "path": video_file,
        "file":  video_file,
        "uuid": str(uuid.uuid4())
	     }
  # movie.edit_clips(video_file)
  df = pd.DataFrame(data=metadata, index=[video_file])
  mediafiles = df.iloc[0]
  #print("mediafiles! = %",mediafiles)
  dictOfMoviesFiles = df.to_dict()
  listOfClip = list(dictOfMoviesFiles['file'])
  
  prepConcatenate(listOfClip)
  
  #listOfMoviesFiles = list(dictOfMoviesFiles.items)
  # listOfMoviesFiles = list(dictOfMoviesFiles['file'])
  #print(listOfMoviesFiles)
  #listOfClips = []
  #for i in listOfMoviesFiles: 
   # listOfClips.append(i)
    #print(listOfClips)
  #movie.edit_clips(listOfMoviesFiles)
  #print(listOfClips)
  # print(listOfMoviesFiles)
  # print(df[metadata["file"]])
  
  return df

####### - Prepare for Concatenation - ########
def prepConcatenate(clips):
  for items in clips:
    movie.movieclips.append(items)
    #print(movie.movieclips)
    movie.edit_clips(movie.movieclips)
    return movie.movieclips

def to_xml(name, df):
  root = et.Element("VantagePlayList")
  name_entry = et.SubElement(root, "Name")
  name_entry.text = name
  ## Add files
  files_to_xml(df, root)
  edl_root = et.SubElement(root, "EDL")
  ## Add edl
  create_edl_xml(df, edl_root)
  return et.tostring(root, encoding="utf-8", pretty_print=True)

def files_to_xml(df, root):
  """
  Convert dataframe into XML
  """

  def row_xml(row):
    """
    Create a new row
    """
    attrs = {}
    for attr in ["uuid", "path"]:
      attrs[attr] = row[attr]
    et.SubElement(root, "File", attrs)

  df.apply(row_xml, axis=1)

def create_edl_xml(df, root):
  """
  Create the edl
  <Edit ...attrs>
  </Edit>
  """
  def row_xml(row):
    edit_attrs = {"type":"file", "sequence":"0"}
    for attr in ["timecode_in", "timecode_out", "uuid"]:
      edit_attrs[attr] = str(row[attr])
    edit_attrs["file"] = edit_attrs["uuid"]
    del edit_attrs["uuid"]
    edit_entry = et.SubElement(root, "Edit", edit_attrs)
    channels_entry = et.SubElement(edit_entry, "ChannelMap")

    channels =    [
          {"source": str(1), "output": str(1)},
          {"source": str(2), "output": str(2)}
        ]
    for i, chan in enumerate(channels):
      channel_entry = et.SubElement(channels_entry, "Channel")

      entry = et.SubElement(channel_entry, "Source")
      entry.text = channels[i]["source"]
      entry = et.SubElement(channel_entry, "Output")
      entry.text = channels[i]["output"]

  df.apply(row_xml, axis=1)


"""


"""

"""
    Channel 1:
    Source -> Index:1
    Output -> Stream 1
    CHannel 2:
    Source -> Index:2
    Output -> Stream 2
    Source -> Index:3
    Output -> Stream 1
    CHannel 2:
    Source -> Index:4
    Output -> Stream 4
    
"""