# hass-custom-components
A collection of custom components for Home Assistant:


# Camera
Custom camera components

## Sighthound
A camera component that displays people and faces detected by [this Sighthound custom_component](https://github.com/robmarkcole/HASS-Sighthound).
Since image_processing components can take a while to process an image, the best way to get this up and running is by using a local_file camera.
My current image_processing flow is the following:

RTSP camera > local_file camera > Sighthound image_processing > Sighthound camera

A snapshot is taken using the camera.snapshot service whenever motion is detected and the image is saved under /images/latest.jpg. A local_file camera is set up displaying this latest.jpg image. Whenever a new snapshot is created, the image_processing.scan service for Sighthound is called. This Sighthound camera component will update automatically, drawing the detected people and faces over the latest snapshot image and displaying that.

### Example integration

```
camera:
- platform: sighthound
  camera: camera.livingroom_latest
  processor: image_processing.sighthound_livingroom_latest
  name: Sighthound
  classifier: ''
```

## Tensorflow
A camera component that displays objects detected by [the Tensorflow component](https://www.home-assistant.io/components/image_processing.tensorflow/). This component will draw detected objects, using different colors for different object types.
Since image_processing components can take a while to process an image, the best way to get this up and running is by using a local_file camera.
My current image_processing flow is the following:

RTSP camera > local_file camera > Tensorflow image_processing > Tensorflow camera

A snapshot is taken using the camera.snapshot service whenever motion is detected and the image is saved under /images/latest.jpg. A local_file camera is set up displaying this latest.jpg image. Whenever a new snapshot is created, the image_processing.scan service for Tensorflow is called. This Tensorflow camera component will update automatically, drawing the detected people and faces over the latest snapshot image and displaying that.

Note: An easier way to get this done is by using the file_out parameter of the Tensorflow component. This will automatically save an image of the camera with detected objects drawn over it. This can then be displayed using a local_image camera.
Example config:
```
image_processing:
- platform: tensorflow
    source:
      - entity_id: camera.camera
    model:
      graph: /config/tensorflow/frozen_inference_graph.pb
    file_out: '/images/tensorflow.jpg'
```

## Full screen issue
One issue I've run into and haven't been able to solve yet is that no image gets displayed when clicking on the camera. One workaround I've found is adding another generic camera, using the image of the sighthound camera:

```
camera:
- platform: generic
  name: Livingroom Sighthound
  still_image_url: >
    {{ 'https://HASS_URL.duckdns.org:8123'+states.camera.sighthound.attributes.entity_picture }}
```


# Scripts
The following scripts are included:
* export_gps.py
* plot.py

## export_gps.py
This script can be used to export latitude, longitude, timestamp and name into a csv file. It can be used to frequently save location data and then plot it onto a map using the plot.py script.
The script can be called the following way:

`python export_gps.py -t 37.766956 -o -122.438481 -d '2018-12-07T19:32:43.589+0200' -p PERSON_NAME`

This will create a new file or edit an existing file called DATE+PERSON_NAME+_gps.csv

### Use with Home Assistant
This export script can be used with Home Assistant. Since it includes some additional python packages, we can't just use a python_script and instead have to use a shell_command:

`shell_command:   export_gps: "python /path/to/export_gps.py -t {{states.device_tracker.DEVICE_NAME.attributes.latitude}} -o {{states.device_tracker.DEVICE_NAME.attributes.longitude}} -d '{{states.device_tracker.DEVICE_NAME.attributes.timestamp}}' -p PERSON_NAME" `

Note that the device tracker needs to include latitude and longitude attributes. You can now create an automation that calls this script whenever the device_tracker changes, or create a new flow in Node-Red.

## plot.py
The plog script can be used to plot location data in a .csv file onto google maps using [gmplot](https://github.com/vgm64/gmplot). This will generate a HTML file that can be displayed in a browser.

The script can be called this way:
`python plot.py -p PERSON_NAME`

## Use with Home Assistant
Similar to the export script, this script can be called using a shell_command. But first you'll need to install the gmplot package using `pip install gmplot`. If you're running in Docker you'll have to run this command inside the docker container.

The shell_command could look something like this:
`plot_person: "python /path/to/plot.py -p person"`

To display the generated html file, you can use an iframe panel:
```
panel_iframe:   
  gps:     
    title: 'GPS'     
    url: '/local/person_gps.html'
```

or an iframe lovelace card:
```
- id: person_gps_iframe         
  type: iframe         
  url: /local/person_gps.html
```

