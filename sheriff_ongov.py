from collections import OrderedDict
from records_class import Record
import pickle
from datetime import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


def main():
    while True:
        driver = webdriver.Firefox()
        driver.set_window_size(1600, 800)
        driver.implicitly_wait(5) # waits for elements for 5 seconds
        driver.get('http://sheriff.ongov.net/lookup')
        try:
            try:
                frame = WebDriverWait(driver, 10).until(
                        EC.frame_to_be_available_and_switch_to_it(0)
                    )
            finally:
                    collect_data(driver)
        except:
            driver.quit()
            pass
        else:
            driver.quit()
            break

def collect_data(driver):
    # finds all letter-links on first page of lookup
    # has to be convoluted because driver objects aren't consistent after
    # navigating between pages

    data = OrderedDict()
    # output = open('output.txt', 'w')

    for x in range(26):
        letters = driver.find_elements_by_class_name("commandLink")
        letters[x].click()

        #on results page for particular letter
        try:
            pages = driver.find_element_by_xpath('//*[@id="form1:table1:statistics1"]/span')

            previous_was_match = False
            continuation = False
            for page in range(1, int(pages.text.split(' ')[-1]) + 1):

                input_box = driver.find_element_by_xpath('//*[@id="form1:table1:goto1__pagerGoText"]')
                input_box.clear()
                input_box.send_keys(page)
                go_button = driver.find_element_by_xpath('//*[@id="form1:table1:goto1__pagerGoButton"]')
                go_button.click()

                # collect all data on this page
                entries = driver.find_elements_by_xpath('//*[@id="form1:table1"]/tbody/tr')
                for tr in entries:
                    fields = tr.find_elements_by_xpath('.//td')[1:] #first td is always empty
                    # if there is a note about the name
                    offset = len(fields) - 11
                    # if the name is empty -> continuation of previous entry
                    if fields[offset + 2].text != '' and int(fields[offset + 2].text) >= 18:
                        previous_was_match = False
                        continuation = False
                        continue
                    elif fields[offset + 1].text == '' and (not previous_was_match):
                        previous_was_match = False
                        continuation = False
                        continue
                    else:
                        if (fields[offset + 1].text == '' and previous_was_match) or continuation:
                            print('extended record')
                            record = prev_record
                            record.cell.append(fields[offset + 3].text)
                            record.offense.append(fields[offset + 4].text)
                            record.court_name.append(fields[offset + 5].text)
                            record.court_date.append(fields[offset + 6].text)
                            record.agency.append(fields[offset + 7].text)
                            record.bond.append(fields[offset + 8].text)
                            record.bail.append(fields[offset + 9].text)
                            record.bail_remarks.append(fields[offset + 10].text)
                        else:
                            print('found new matching record' + fields[0].text)
                            previous_was_match = True
                            continuation = False
                            # make record and enter it into OrderedDict
                            record = Record(fields[0].text) # make record object with name
                            record.ICN = fields[offset + 1].text
                            record.age = fields[offset + 2].text
                            record.cell.append(fields[offset + 3].text)
                            record.offense.append(fields[offset + 4].text)
                            record.court_name.append(fields[offset + 5].text)
                            record.court_date.append(fields[offset + 6].text)
                            record.agency.append(fields[offset + 7].text)
                            record.bond.append(fields[offset + 8].text)
                            record.bail.append(fields[offset + 9].text)
                            record.bail_remarks.append(fields[offset + 10].text)
                            prev_record = record


                        data[record.name] = record
                        prev_record = record

                    if 'continued on next page**' in fields[0].text:
                        continuation = True


        except NoSuchElementException:
            print('no such element, crawling one and only page')
            previous_was_match = False
            continuation = False

            entries = driver.find_elements_by_xpath('//*[@id="form1:table1"]/tbody/tr')
            for tr in entries:
                fields = tr.find_elements_by_xpath('.//td')[1:] #first td is always empty
                # if there is a note about the name
                offset = len(fields) - 11
                # if the name is empty -> continuation of previous entry
                if 'continued on next page**' in fields[0].text:
                    continuation = True
                    continue
                if fields[offset + 2].text != '' and int(fields[offset + 2].text) >= 18:
                    previous_was_match = False
                    continuation = False
                    continue
                if fields[offset + 1].text == '' and (not previous_was_match):
                    previous_was_match = False
                    continuation = False
                    continue
                else:
                    if (fields[offset + 1].text == '' and previous_was_match) or continuation:
                        continuation = False
                        record = prev_record
                        record.cell.append(fields[offset + 3].text)
                        record.offense.append(fields[offset + 4].text)
                        record.court_name.append(fields[offset + 5].text)
                        record.court_date.append(fields[offset + 6].text)
                        record.agency.append(fields[offset + 7].text)
                        record.bond.append(fields[offset + 8].text)
                        record.bail.append(fields[offset + 9].text)
                        record.bail_remarks.append(fields[offset + 10].text)
                    else:
                        print('found new matching record' + fields[0].text)
                        previous_was_match = True
                        continuation = False
                        # make record and enter it into OrderedDict
                        record = Record(fields[0].text) # make record object with name
                        record.ICN = fields[offset + 1].text
                        record.age = fields[offset + 2].text
                        record.cell.append(fields[offset + 3].text)
                        record.offense.append(fields[offset + 4].text)
                        record.court_name.append(fields[offset + 5].text)
                        record.court_date.append(fields[offset + 6].text)
                        record.agency.append(fields[offset + 7].text)
                        record.bond.append(fields[offset + 8].text)
                        record.bail.append(fields[offset + 9].text)
                        record.bail_remarks.append(fields[offset + 10].text)

                    data[record.name] = record
                    prev_record = record

                continuation = False


        print(data)
        # reset to first lookup page
        driver.get('http://sheriff.ongov.net/lookup')
        driver.switch_to_frame(0)

    # output.close()
    pickle_name = str(date.today()) + '.p'
    pickle.dump( data, open( pickle_name, "wb" ) )

def imports():
    from collections import OrderedDict
    from records_class import Record
    import pickle
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC




if __name__ == "__main__":
    main()
