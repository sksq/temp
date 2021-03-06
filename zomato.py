import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
# To install selenium: pip install selenium


def get_info(identifier, time_sleep=2):
    """ Main function called to get text and image photo_url
        Identifier is the class name of rows in the page (found by inspect elements); for our case: 'row','alt'
        time_sleep is the time delay between two calls (two wordmarks), in seconds, default:2, increase if IP Banned or slow net(if same row repeats itself)
        returns list, append it to main list for a particular page
    """
    print '\t', identifier
    len_script = "return document.getElementsByClassName('"+identifier+"').length"
    iterator_count = driver.execute_script(len_script)
    dict_list = []
    for i in range(iterator_count):
        click_script = "document.getElementsByClassName('"+identifier+"')["+str(i)+"].getElementsByTagName('a')[0].click()"
        driver.execute_script(click_script)
        wait1 = WebDriverWait(driver, 10)
        wait1.until(EC.visibility_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_LblDetails")))
        application_left_script = "return document.getElementsByClassName('"+identifier+"')["+str(i)+"].getElementsByTagName('span')[6].innerText"
        application_left = driver.execute_script(application_left_script)
        found_it = False
        times = 0
        print '\t\tfetching application data'
        while(not found_it):
            time.sleep(time_sleep)
            times+=1
            application_right_script = "return document.getElementById('ctl00_ContentPlaceHolder1_PnlDetails').getElementsByTagName('td')[3].innerText"
            application_right = driver.execute_script(application_right_script).split()[0]
            found_it = application_right==application_left
            print '\t\t\tfetch attempt{0}: left=>{1} right=>{2} {3}'.format(times, application_left,application_right,found_it)
        content_script = "return document.getElementById('ctl00_ContentPlaceHolder1_PnlDetails').getElementsByTagName('td')"
        table_cells = [table_cell.text.encode('ascii','ignore') for table_cell in driver.execute_script(content_script)]
        table_cells_iterator = iter(table_cells)
        tmp_data = {table_cell:next(table_cells_iterator) for table_cell in table_cells_iterator}
        print '\t\t', "[{0} of {1}]".format(i,iterator_count-1), tmp_data['Word Mark']
        try:
            photo_script = "return document.getElementsByClassName('"+identifier+"')["+str(i)+"].getElementsByTagName('img')[0].src"
            tmp_photo = driver.execute_script(photo_script)
        except:
            tmp_photo = ""
        dict_list.append({'text':tmp_data, 'photo':tmp_photo.encode('ascii','ignore'), 'phrase':tell_phrase, 'class':tell_class})
    return dict_list

driver = webdriver.Chrome(executable_path="/home/a2/chromedriver")
driver.get('https://www.zomato.com/bangalore/truffles-st-marks-road/reviews')

wait = WebDriverWait(driver, 15)
wait.until(EC.visibility_of_element_located((By.ID, "selectors")))
loadMore = driver.find_element_by_id("ctl00_ContentPlaceHolder1_TBWordmark")

for idx1,tell_phrase in enumerate(tell_phrases):
    for idx2,tell_class in enumerate(tell_classes):
        print "[{0} of {1}] [{2} of {3}]".format(idx1,len1,idx2,len2), "opening main page"
        try:
            print '\t main page opened'
            print '\t', tell_phrase, tell_class
            print '\t', 'entering query strings'
            inputClass = driver.find_element_by_id("ctl00_ContentPlaceHolder1_TBClass")
            inputWords.send_keys(tell_phrase)
            inputClass.send_keys(tell_class)
            enter_script = "document.getElementById('ctl00_ContentPlaceHolder1_BtnSearch').click()"
            driver.execute_script(enter_script)
        except:
            print '\t', 'error with opening home page', '\a'
            continue

        print '\t', 'waiting for content to be loaded'
        try:
            wait1 = WebDriverWait(driver, 15)
            wait1.until(EC.visibility_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_MGVSearchResult")))
            print '\t', 'search result loaded'
            data = get_info('row') + get_info('alt')    #give time_sleep here if you want to change
        except:
            print '\t', 'No Records Found', '\a'
            try:
                alert = driver.switch_to_alert()
                alert.accept()
            except:
                print '\t', 'couldnt switch to alert'
            continue
        try:
            len3 = len(data)-1
            print '\t', 'saving images'
            # image saved as Word_Mark-Appl_No.png
            for idx3,word_mark in enumerate(data):
                photo_url = word_mark['photo']
                if photo_url:
                    photo_name = word_mark['text']['Word Mark']+'-'+word_mark['text']['Appl. No.'].split()[0]
                    print '\t\t', "[{0} of {1}]".format(idx3,len3), 'saving', photo_name
                    driver.get(photo_url)
                    driver.save_screenshot(photo_name+'.png')
        except:
            print '\t', 'Error with images', '\a'
            continue
        complete_data+=data
        
        # Temporary JSON file - overwritten (not appended)
        with open('data.txt', 'w') as outfile:
            json.dump(complete_data, outfile)
driver.quit()


# HEADER [Phrase search,Class Number,Word Mark,Proprietor,Appl. No.,Appl. Date,Status,Journal No.,Journal Date,Used Since,Valid Upto,Goods & Services Description,Image Url]
# Appending to csv file
with open('data.csv', 'a') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerows([[x['phrase'],x['class'],x['text']['Word Mark'],x['text']['Proprietor'],x['text']["Appl. No."].split()[0],x['text']["Appl. Date"],x['text']['Status'],x['text']["Journal No."].split('    ')[0],x['text']["Journal No."].split(':')[-1],x['text']['Used Since'].split('    ')[0],x['text']['Used Since'].split(':')[-1],x['text']['Goods & Services Description'],x['photo']] for x in complete_data])