# StableDifussion Generator Service
## Installation
To install just run `sh install.sh`
it will install all the python dependencies and generate a `sd-gen.service` file.

copy the generated `sd-gen.service` file to `/etc/systemd/system`
and then run:
```
sudo systemctl enable sd-gen
sudo systemctl daemon-reload
sudo systemctl start sd-gen
```
You can then check if the service is running using
```
sudo systemctl | grep running
```

## Execution
When the service loads it automatically checks if the model is there an has been unpacked or not. 

If there is no `model.safetensors` inside the model folder the service will stop. 

If the model is there and it has not been unpacked it will unpack it automatically. It it has been already unpacked it will just load it.

After the model has been loaded, the service will check the input folder and queue all the images it finds in the folder for processing. 

Whenever a new image is placed inside the input folder, it will get queued for processing.

## Processing
Once an image gets taken from the queue it will automatically resize the image to the closes 768px and generate as many images as indicated in the batch param of the `config.ini` file.

For each input image a new folder inside the output folder will be generated containing the source image, the resized source image and the generated images. 

## Updating the config
To change parameters in the config file you can change the file accordingly and then restart the service using
```
sudo systemctl restart sd-gen
```

## Uninstall
To uninstall the service just stop the service 
```
sudo systemctl stop sd-gen
```
and remove the `/etc/systemd/system/sd-gen.service` file.