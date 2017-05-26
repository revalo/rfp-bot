from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pyotp
import time

def submit_rfp(kerb_user, kerb_password, duo_secret, duo_count, rfp_name, cost_object, gl_number, items):
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

	# Create lines
	for _ in xrange(len(items) - 1):
		driver.find_element_by_id('addLine').click()

	# Fill lines
	for index, item in enumerate(items):
		date_box = driver.find_element_by_name('rfpDocument.lineItems[%i].serviceDate' % index)
		account_box = driver.find_element_by_name('rfpDocument.lineItems[%i].glAccount.glAccountNumber' % index)
		cost_object_box = driver.find_element_by_name('rfpDocument.lineItems[%i].costObject.costObjectNumber' % index)
		amount_box = driver.find_element_by_name('rfpDocument.lineItems[%i].amount' % index)
		notes_box = driver.find_element_by_name('rfpDocument.lineItems[%i].explanation' % index)

		date_box.send_keys(item.date.strftime("%m/%d/%Y"))
		account_box.send_keys(gl_number)
		cost_object_box.send_keys(cost_object)
		amount_box.send_keys(str(item.get_amount()))
		notes_box.send_keys(item.notes)

	time.sleep(100) # Debug
	driver.close()
