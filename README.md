# Image-Recognition
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