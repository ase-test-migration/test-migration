# iOS environment
from appium import webdriver

# cap.setCapability('automationName' , 'XCUITest');
# cap.setCapability('xcodeOrgId', '5FLNFHR2L3');  //substitute with yours
# cap.setCapability('udid', 'bdf8ac24c06288f44ac43ebe32b2c23e6e49b7e2');
# cap.setCapability('xcodeSigningId', 'iPhone Developer');
# cap.setCapability('platformName', 'iOS');
# cap.setCapability('deviceName', 'Someone’s iPhone');

desired_caps = {
    'platformName': 'iOS',
    'xcodeOrgId': '5FLNFHR2L3',
    'automationName': 'xcuitest',
    'deviceName': 'Someone\'s iPhone',
    'udid': 'bdf8ac24c06288f44ac43ebe32b2c23e6e49b7e2'
}

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
print(driver.desired_capabilities)
print(driver.session_id)
driver.back()
img_data = driver.get_screenshot_as_base64()
with open("imageToSave.png", "wb") as fh:
    fh.write(img_data)
