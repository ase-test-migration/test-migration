## Run Migration
* Start Appium server.
* Run using **python3**, make sure you have the correct connection config in [main.py](main.py) 
  ```
  python3 main.py theRecordedTestcaseToRun.json
  ```
* After a successful extraction of the testcase specified. You can now use migrator.py in the corresponding folder to do test migration.
  * To migrate extracted **iOS** testcases to **Android**, Run:
      ```
      python3 python-android/migrator.py python-ios/theExtractedTestCaseFolder
      ```
  * To migrate extracted **Android** testcases to **iOS**, Run:
      ```
      python3 python-ios/migrator.py python-android/theExtractedTestCaseFolder
      ```
## Run static matching for fidelity data
Remember to add the state numbers (Line 306) for states you want to do static matching in **static_matching_runner.py**.
```
python3 static_matching_runner.py python-android/TESTCASENAME python-ios/TESTCASENAME TESTCASENAME
```

## Run Layout Capture for current view

* Run Appium server.
* Change connection capabilities in [layout_tree.py](layout_tree.py) to reflect your device.
* Uncomment L529-L542(Android), L428-L442(iOS) in [layout_tree.py](layout_tree.py) 
* Run using **python3** by running *python3 layout_tree.py name_of_the_output*.
* When running, the current window on the connected device will be captured.
* The output is in the [pngs](pngs) directory. Each crop is given in original color and in grayscale one.