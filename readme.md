# StableDifussion Generator Service

## Pre requisites
The AWS EC2 g5.xlarge machine shoudl have at least 50gb of storage and run Ubuntu 22
First update all packages by running
```
sudo apt update
sudo apt upgrade
```
Then install all the build essentials for the NVIDIA driver installation
```
sudo apt install build-essential
```
After that, download the NVIDIA CUDA 11.8 and Driver installation script and run it
```
wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_520.61.05_linux.run
sudo sh cuda_11.8.0_520.61.05_linux.run
```
This installation process will ask you to first write `accept` and then select `install`.
After the installation is done, you will need to add CUDA to the PATH environment variables. To do this, open the `.bashrc` file and add the following at the end of the file
```
export PATH="/usr/local/cuda-11.8/bin:$PATH"
export LD_LIBRARY_PATH="/usr/local/cuda-11.8/lib64:$LD_LIBRARY_PATH"
```
After that, force a reload of bash by running
```
source .bashrc
```
This should do for the CUDA installation, to confirm that the installation was succesful run the following command
```
nvcc --version
```

AWS Ubuntu 22 does not come with python virtual environments installed, to install it first confirm which version of python is intalled.
```
python3 --version
```
If 3.10 is installed, then install the venv package accordingly by running
```
sudo apt install python3.10-venv
```

## Installation
To install just run 
```
sh install.sh
```
it will install all the python dependencies and generate a `sd-gen.service` file.

After running the `install.sh` copy your `model.safetensors` model into the model folder.

copy the generated `sd-gen.service` file to `/etc/systemd/system`
```
sudo cp sd-gen.service /etc/systemd/system/
```
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
or by looking through the service log using
```
sudo journalctl -u sd-gen -n 50 -f
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
```
sudo rm /etc/systemd/system/sd-gen.service
```