from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pyotp
import time

def submit_rfp(kerb_user, kerb_password, duo_secret, duo_count, rfp_name, items):
	driver = webdriver.Chrome()
	main_window = driver.current_window_handle

	driver.get("https://atlas.mit.edu/atlas/Main.action?tab=home&sub=group_my_reimburse")
	if "Touchstone@MIT" in driver.title:
		# Auth
		username_box = driver.find_element_by_name("j_username")
		username_box.clear(); username_box.send_keys(kerb_user)

		password_box = driver.find_element_by_name("j_password")
		password_box.clear(); password_box.send_keys(kerb_password)

		password_box.send_keys(Keys.RETURN)

		driver.switch_to_frame(driver.find_element_by_id("duo_iframe"))
		bypass_button = driver.find_elements_by_class_name("auth-button")[1]
		bypass_button.click()

		# Generate OTP
		hotp = pyotp.HOTP(duo_secret)
		passcode = hotp.at(duo_count)

		passcode_box = driver.find_element_by_name("passcode")
		passcode_box.clear(); passcode_box.send_keys(passcode)
		bypass_button.click()

		driver.switch_to_default_content()

	driver.implicitly_wait(10)
	request_rfp_link = driver.find_element_by_link_text("Request a Reimbursement for Me")
	driver.execute_script("openApplication('rfp_rfr_ss', this);") # Prevent new tab stuff :O

	rfp_name_box = driver.find_element_by_name("rfpDocument.shortDescription")
	rfp_name_box.clear(); rfp_name_box.send_keys(rfp_name)
	driver.implicitly_wait(0)

	time.sleep(100) # Debug
	driver.close()
