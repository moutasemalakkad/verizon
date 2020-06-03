import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from apache_beam import window

from google.cloud import pubsub_v1


import json
import os
import time



#### json file (authirzation)
path_service_account = "beam-276623-290ddf0eab0b.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path_service_account


#### topics#####
input_subscription = 'projects/covid-19-279120/subscriptions/beam-raw-data-sub'
output_topic = 'projects/covid-19-279120/topics/cleaned_data'




#######Beam Connfigs#######
# set options
options = PipelineOptions()
options.view_as(StandardOptions).streaming = True



#######Transformation Functions#######

# Json to Python Dic
def to_python_dict(element):
    return json.loads(element)


# get venue value
def get_venue(elements):
  return elements['venue']


# get mode value
def get_mode(elements):
   return elements['mode']

# build tuple
def build_tuple(elements):
  mode = elements['mode']
  geo_hash = elements['geohash']
  return (geo_hash, mode)


# # Transform our Json object to Python Dict
# def to_python_dict(element):
#     return json.loads(element)
#
#
# # get venue
# def get_venue(elements):
#   return elements['venue']
#
# # get mode
# def get_mode(elements):
#    return elements['mode']
#
# # build tuple
# def build_tuple(elements):
#   mode = elements['mode']
#   geo_hash = elements['geohash']
#   return (geo_hash, mode)



###### Pipline Beam (Transforms) ############



# Building a Beam Pipline
p1 = beam.Pipeline(options=options)

attendance_count = (
    p1
    |'read pub_sub' >> beam.io.ReadFromPubSub(subscription=input_subscription)





    # | 'to python dict' >> beam.Map(to_python_dict)

    # | 'Filter offline events' >> beam.Filter(lambda element: element['venue']['mode'] == 'online') # change to offline


    # | 'get venue' >> beam.Map(get_venue)
    # | 'build_tuple' >> beam.Map(build_tuple)



    | 'Write to PubSUb' >> beam.io.WriteToPubSub(output_topic)

)


# running pipline
result = p1.run()
result.wait_until_finish()
