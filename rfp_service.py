from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pyotp
import time
import pdfkit

def submit_rfp(kerb_user, kerb_password, duo_secret, duo_count, rfp_name, cost_object, gl_number, receivers_name, items):
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

    driver.find_element_by_class_name('saveAction').click()

    # Upload receipts
    upload = driver.find_element_by_id('upload')
    upload.send_keys(items[0].filename)
    driver.find_element_by_xpath('/html/body/div[3]/div[3]/button[2]').click()

    for index, item in enumerate(items):
        if index == 0:
            continue
        driver.find_element_by_class_name('attachReceipts').click()
        upload = driver.find_element_by_id('upload')
        upload.send_keys(item.filename)
        driver.find_element_by_xpath('/html/body/div[3]/div[3]/button[2]').click()

    # Send to someone
    driver.find_element_by_class_name('sendToAction').click()
    driver.find_element_by_name('recipientName').send_keys(receivers_name)
    driver.find_element_by_class_name('searchForRecipient').click()

    # Assumes a single row is returned
    # FIXME Might be a really bad thing

    # Send it weee
    driver.find_element_by_class_name('sendToAction').click()
    pdfkit.from_string(driver.page_source, 'rfp_confirm.pdf')

    # time.sleep(100) # Debug
    driver.close()

    
