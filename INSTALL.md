# How it works
## Dependencies
In order to run MAPIT you will need to install the following dependecies:

-   opencv_python==4.5.1.48
-   nltk==3.5
-   numpy==1.20.1
-   scipy==1.6.0
-   lxml==4.5.2
-   editdistance==0.5.3
-   matplotlib==3.3.4
-   Send2Trash==1.5.0
-   pytesseract==0.3.4
-   selenium==3.141.0
-   imageio==2.9.0
-   pandas==1.2.1
-   networkx==2.4
-   gensim==3.8.3
-   Appium_Python_Client==1.1.0
-   Pillow==8.2.0
-   pycurl==7.43.0.6
-   pypng==0.0.20
-   scikit_learn==0.24.1

## How to run
You will need to download and extract the GoogleNews-vectors-negative300.bin to data folder in order for the code to work. The pre-trained vectors could be downloaded [here](https://github.com/mmihaltz/word2vec-GoogleNews-vectors).

You will also need to install appium on your computer and mobile device. Please refer to appium's website for instructions. The appium service should be running for the tool to work properly (The appium server on your machine should be listening on port 4723).

In order for the migration and matching to work properly you will need to set the width of your device screen (Android & iOS) in image_matching/similarity_calculator.py file.

For a test recorded on iOS navigate to ``/python-ios`` and:
>For generating its corresponding test on MAPIT's internal representation run ``iosTestToJson.py “arg1: appname-abbreviation” “arg2: testname"``
>For running source data extraction run  ``main.py “arg:name of the test on MAPIT's internal format"``

For a test recorded on Android navigate to ``/python-android`` and:
>For generating its corresponding test on MAPIT's internal representation run ``andTestToJson.py “arg1: appname-abbreviation” “arg2: testname"``
>For running source data extraction run  ``main.py “arg:name of the test on MAPIT's internal format"``

For running the migration from one platform to another you should run its corresponding ``migrator.py`` file while the source data is extracted and the device on target platform is running.

