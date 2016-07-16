import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

links = ["https://www.zomato.com/bangalore/empire-restaurant-koramangala-5th-block", "https://www.zomato.com/bangalore/truffles-koramangala-5th-block", "https://www.zomato.com/bangalore/meghana-foods-koramangala-5th-block", "https://www.zomato.com/bangalore/a-hole-lotta-love-cafe-koramangala-5th-block", "https://www.zomato.com/bangalore/sultans-of-spice-koramangala-5th-block", "https://www.zomato.com/bangalore/stoner-koramangala-5th-block", "https://www.zomato.com/bangalore/buff-buffet-buff-koramangala-5th-block", "https://www.zomato.com/bangalore/tim-tai-koramangala-5th-block", "https://www.zomato.com/bangalore/kopper-kadai-koramangala-5th-block", "https://www.zomato.com/bangalore/the-black-pearl-koramangala-5th-block", "https://www.zomato.com/bangalore/om-made-cafe-koramangala-5th-block", "https://www.zomato.com/bangalore/gillys-restobar-koramangala-5th-block", "https://www.zomato.com/bangalore/the-boozy-griffin-koramangala-5th-block", "https://www.zomato.com/bangalore/happy-brew-koramangala-5th-block", "https://www.zomato.com/bangalore/berryd-alive-koramangala-5th-block", "https://www.zomato.com/bangalore/bonsouth-koramangala-5th-block", "https://www.zomato.com/bangalore/over-the-top-terrace-lounge-koramangala-5th-block", "https://www.zomato.com/bangalore/anand-sweets-and-savouries-koramangala-5th-block", "https://www.zomato.com/bangalore/le-charcoal-koramangala-5th-block", "https://www.zomato.com/bangalore/cup-o-joe-koramangala-5th-block", "https://www.zomato.com/bangalore/dhide-cafe-koramangala-5th-block", "https://www.zomato.com/bangalore/kritunga-restaurant-koramangala-5th-block", "https://www.zomato.com/bangalore/tandoor-hut-koramangala-5th-block", "https://www.zomato.com/bangalore/hotel-junior-kuppanna-koramangala-5th-block", "https://www.zomato.com/bangalore/asia-kitchen-by-mainland-china-koramangala-5th-block", "https://www.zomato.com/bangalore/hunan-koramangala-5th-block", "https://www.zomato.com/bameys", "https://www.zomato.com/bangalore/chianti-koramangala-5th-block", "https://www.zomato.com/bangalore/dice-n-dine-koramangala-5th-block", "https://www.zomato.com/bangalore/bathinda-junction-koramangala-5th-block"]

all_rest = []
for link in links:
  print(link)
  driver = webdriver.Chrome(executable_path="/home/a2/chromedriver")
  driver.get(link+"/reviews")
  wait = WebDriverWait(driver, 15)
  wait.until(EC.visibility_of_element_located((By.ID, "selectors")))
  all_reviews_script = "document.getElementById('selectors').getElementsByTagName('a')[1].click()"
  load_script = "document.getElementsByClassName('load-more bold ttupper tac cursor-pointer fontsize2')[0].click()"
  review_div_script = "document.getElementsByClassName('ui segments res-review-body res-review clearfix js-activity-root item-to-hide-parent stupendousact')"
  review_script = ".getElementsByClassName('ui segment clearfix')[0]"
  review_and_follow_count_script = ".getElementsByClassName('grey-text fontsize5 nowrap')[0].innerHTML"
  timestamp_script = ".getElementsByTagName('time')[0].getAttribute('datetime')"
  rating_script = ".getElementsByClassName('ttupper')[0].getAttribute('aria-label')"
  text_script = ".getElementsByClassName('rev-text')[0].textContent"
  likes_script = ".getElementsByClassName('left mr5 ui tiny labeled button js-btn-thank')[0].textContent"
  comments_script = ".getElementsByClassName('left ui tiny labeled button comment-btn-to')[0].textContent"
  lat_long_script = "document.getElementsByClassName('mtop0')[0].getAttribute('href')"
  topics_script = "document.getElementsByClassName('res-info-estabs grey-text fontsize3')[0].textContent"
  name_script = "document.getElementsByClassName('ui large header left')[0].textContent"
  driver.execute_script(all_reviews_script)
  # now all reviews tab is open
  while(1):
    try:
      driver.execute_script(load_script)
      time.sleep(2)
    except:
      break
  # all loaded now.
  reviews_list_all = []
  for i in range(len(driver.execute_script("return "+review_div_script))):
    # print(i)
    temp_review_dict = {}
    try:
      temp_review_dict["review_and_follow"] = driver.execute_script("return "+review_div_script+"["+str(i)+"]"+review_script+review_and_follow_count_script).strip().split()
      temp_review_dict["review_and_follow"] = temp_review_dict["review_and_follow"][0], temp_review_dict["review_and_follow"][-2]
    except:
      temp_review_dict["review_and_follow"] = ""
    try:
      temp_review_dict["timestamp"] = driver.execute_script("return "+review_div_script+"["+str(i)+"]"+review_script+timestamp_script)
    except:
      temp_review_dict["timestamp"] = ""
    try:
      temp_review_dict["rating"] = driver.execute_script("return "+review_div_script+"["+str(i)+"]"+review_script+rating_script)
    except:
      temp_review_dict["rating"] = ""
    try:
      temp_review_dict["text"] = driver.execute_script("return "+review_div_script+"["+str(i)+"]"+review_script+text_script).strip()[5:].strip()
    except:
      temp_review_dict["text"] = ""
    try:
      temp_review_dict["likes"] = driver.execute_script("return "+review_div_script+"["+str(i)+"]"+review_script+likes_script).strip()[4:].strip()
    except:
      temp_review_dict["likes"] = ""
    try:
      temp_review_dict["comments"] = driver.execute_script("return "+review_div_script+"["+str(i)+"]"+review_script+comments_script).strip()[7:].strip()
    except:
      temp_review_dict["comments"] = ""
    temp_review_dict["source"] "zomato"
    reviews_list_all.append(temp_review_dict)
  #for location
  driver.get(link+'/maps')
  time.sleep(2)
  rest_dict = {}
  try:
    lat_long = driver.execute_script("return "+lat_long_script)
  except:
    lat_long = ""
  rest_dict['lat_long']=lat_long.strip()
  #for topics
  try:
    topics = driver.execute_script("return "+topics_script)
    rest_dict['topics']=topics.strip().split(',')
  except:
    topics = ""
    rest_dict['topics']=topics
  try:
    name = driver.execute_script("return "+name_script)
    rest_dict['name']=name.strip()
  except:
    rest_dict['name']=""
  rest_dict['reviews']=reviews_list_all
  all_rest.append(rest_dict)
  with open('data.txt', 'w') as outfile:
    json.dump(all_rest, outfile)
  driver.quit()

with open('data.txt', 'w') as outfile:
  json.dump(all_rest, outfile)