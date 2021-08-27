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

In order for the migration and matching to work properly you will need to set the width of your device screen (Android & iOS) in ``image_matching/similarity_calculator.py`` file.

For a test recorded on iOS navigate to ``/python-ios`` and:
>For generating its corresponding test on MAPIT's internal representation run: 
> >``iosTestToJson.py “arg1: appname-abbreviation” “arg2: testname"``
> ------------------------------
> >The test in internal representation can be found on ``/python-ios/test_ios_app-aabrivation_test-index``. For instance, if a search test for chrome app is the second test recorded for this app, the internal test translation output for it would be on ``/python-ios/test_ios_chrome_2.json``
>
>For running source data extraction run:
> >``main.py “arg:name of the test on MAPIT's internal format"``
> -------------------------------------
> >The output can be found in ``/python-ios/appname-abbreviation-testname`` as an example the output for a search test on chrome app can be found on ``/python-ios/chrome-search``.

For a test recorded on Android navigate to ``/python-android`` and:
>For generating its corresponding test on MAPIT's internal representation run: 
>> ``andTestToJson.py “arg1: appname-abbreviation” “arg2: testname"``
>------------------
> > The test in internal representation can be found on ``/python-android/test_android_app-aabrivation_test-index``. For instance, if a search test for chrome app is the second test recorded for this app, the internal test translation output for it would be on ``/python-android/test_android_chrome_2.json``
> 
>For running source data extraction run :
> >``main.py “arg:name of the test on MAPIT's internal format"``
> The output can be found in ``/python-android/appname-abbreviation-testname``
>  as an example the output for a search test on chrome app can be found on ``/python-android/chrome-search``.

For running the migration from one platform to another you should run its corresponding ``migrator.py`` file while the source data is extracted and the device on target platform is running. 
For transferring a test from Android to iOS the migrator on ``/python-ios/migrator.py`` and for transferring the  a test from iOS to Android the migrator on ``/python-android/migrator.py`` should be used. The argument for running this phase would be the output of the previous phase.
 For instance, in order to transfer the chrome search test from Android to iOS the following command can be used in the root directory:
>``/python-ios/migrator.py /python-android/chrome-search``

For transferring the same test on the other direction we can use:
>``/python-android/migrator.py /python-ios/chrome-search``

In order to run the static matching for evaluating the event mapping accuracy we use the ``static_matching_runner``. the following command should be executed from the root directory:
> static_matching_runner.py "arg1: extracted states from android" "arg2: extracted  states from iOS"

For example the command to run static matching for firefox search test would be:
> static_matching_runner.py /python-android/firefox-search /python-ios/firefox-search

Since the ``static_matching_runner`` script map and compare each of the states separately, make sure to configure the under-test states on the script as instructed on the demo video. The results of the static matching can be found on ``/static-out`` directory under the directory with their corresponding test name. 
