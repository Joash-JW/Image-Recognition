# CZ3004 MDP Image Recognition
This repository contains the codes using in my CZ3004 Multi-disciplinary Project AY2019-20 Semester 2. This repository mainly focuses on the image recognition part as that was the part I was tasked with. Nevertheless, the codes that were used for the Rapsberry Pi are included as well.

## Files
- assets: images used in this repository
- rpi: Contains the codes for the communication between the various subsystems
- src: Contains the codes for the image recognition system
- requirements.txt: dependencies included for the image recognition

## Installation
Running the code below on command prompt or shell will automatically install all the necessary `python` packages needed for the program.
```shell
pip install -r requirements.txt
```

## Running the Program
Make sure to create the following folders/directories:
- `raw` - raw images sent from Raspberry Pi will be saved here. Facilitates debugging.
- `processed` - Images that the program detected will be saved here. You **must** create this as the program will look for images in this directory to plot them out.

After creating these directories, run the following code on command prompt or shell to start listening to images sent from the Raspberry  Pi.
```shell
cd src
python main.py
```

## Dataset
You can download the images that I collected and trained on [here](https://www.kaggle.com/joashjw/mdp2020s1).