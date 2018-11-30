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
