#!/usr/bin/python3

import os
import sys
import time
import datetime
import threading
import random
import requests
from requests.auth import HTTPDigestAuth
import json

    
##
##  AUTH
def auth_portal(site_url, site_auth_suffix, person_data):
  
  url=site_url+site_auth_suffix
  
  #myResponse = requests.get(url,auth=HTTPDigestAuth(person_data['username'], person_data['password'], data=auth_json), verify=True)
  headers={
    "Content-Type": "application/json;charset=utf-8"
  }
  myResponse = requests.post(url, json=person_data['user'], headers=headers)
  #print (myResponse.status_code)

  # For successful API call, response code will be 200 (OK)
  if(myResponse.ok):
    jData = json.loads(myResponse.content)
    user_token=jData['key']
    print('-- Authentication OK. Token is: ',user_token)
    return user_token
    #print(json.dumps(jData,indent=2))
  else:
    # If response code is not ok (200), print the resulting http error code with description
    print('-- Authentication Error')
    myResponse.raise_for_status()
    return -1

##
##
## POST DATA
def json_value_insert_random(json_value, VALUE_VARIABILITY_AMOUNT):
  new_value={}
  new_v=float(json_value['value'])
  new_value['value']=new_v+VALUE_VARIABILITY_AMOUNT*random.randint(0,int(new_v)) 
  return new_value

def randomise_dataset(data, VALUE_VARIABILITY_AMOUNT):
  data_array=[]
  for (key,value) in data.items():
    json_v=json_value_insert_random(value, VALUE_VARIABILITY_AMOUNT)
    s='{'+json.dumps(key)+': '+json.dumps(json_v)+'}'
    js=json.loads(s)
    data_array.append(js)
  return data_array
  
def post_data(user_token, site_url, site_data_suffix, data):
  
  #data_array=[]
  #for (key,value) in data.items():
  #  json_v=json_value_insert_random(value)
  #  s='{'+json.dumps(key)+': '+json.dumps(json_v)+'}'
  #  js=json.loads(s)
  #  data_array.append(js)
  
  #print('sending: '+json.dumps(data_array,indent=2))

  print('DATE and TIME: ', datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

  print('-- sending: '+json.dumps(data))

  url=site_url+site_data_suffix
  headers={
    "Authorization": "Token "+user_token,
    "Content-Type": "application/json;charset=utf-8"
  }
  
  myResponse = requests.post(url, json=data, headers=headers)
  if(myResponse.ok):
    print('-- Result OK')
  else:
    print('-- Error', myResponse.status_code)
    #myResponse.raise_for_status()

def post_data_vitals(user_token, site_url, site_data_suffix, data):

  print(data)

  blood_pressure={}
  for item in data:
    if 'systolic_blood_pressure' in item:
      blood_pressure['systolic_blood_pressure']=item['systolic_blood_pressure']
    elif 'diastolic_blood_pressure' in item:
      blood_pressure['diastolic_blood_pressure']=item['diastolic_blood_pressure']      
  data.append(blood_pressure)    
      
  print('-- sending: '+json.dumps(data))

  url=site_url+site_data_suffix
  headers={
    "Authorization": "Token "+user_token,
    "Content-Type": "application/json;charset=utf-8"
  }

  myResponse = requests.post(url, json=data, headers=headers)
  if(myResponse.ok):
    print('-- Result OK')
  else:
    print('-- Error', myResponse.status_code)
    #myResponse.raise_for_status()

    
def send_all(user_token, site_url, site_data_suffix, UPDATE_PERIOD, VALUE_VARIABILITY_AMOUNT):
  post_data_vitals(user_token, site_url, site_data_suffix, randomise_dataset(person_data['vitals'], VALUE_VARIABILITY_AMOUNT))
  time.sleep(1)
  post_data(user_token, site_url, site_data_suffix, randomise_dataset(person_data['body'], VALUE_VARIABILITY_AMOUNT))
  time.sleep(1)
  post_data(user_token, site_url, site_data_suffix, randomise_dataset(person_data['physical_activity'], VALUE_VARIABILITY_AMOUNT))
  time.sleep(1)
  post_data(user_token, site_url, site_data_suffix, randomise_dataset(person_data['sleep'], VALUE_VARIABILITY_AMOUNT))
  time.sleep(1)
  post_data(user_token, site_url, site_data_suffix, randomise_dataset(person_data['ambient'], VALUE_VARIABILITY_AMOUNT))
  threading.Timer(UPDATE_PERIOD, send_all, args=(user_token, site_url, site_data_suffix, UPDATE_PERIOD, VALUE_VARIABILITY_AMOUNT)).start()

      
##
## MENU

def menu(user_token, site_url, site_data_suffix, person_data, VALUE_VARIABILITY_AMOUNT, UPDATE_PERIOD):
  print('######################################################')
  print('##       eCare Personna Simulator')
  print('######################################################')
  print()
  print('Person is '+person_data['user']['username'])
  print('-- variability amount:\t',VALUE_VARIABILITY_AMOUNT)
  print('-- auto update period:\t',UPDATE_PERIOD)
  print()
  print('\t1 - Send Vitals')
  print('\t2 - Send Body')
  print('\t3 - Send Activity')
  print('\t4 - Send Sleep')
  print('\t5 - Send Ambient')
  print()
  print('\t6 - Send Specific Value')
  print()
  #print('\t9 - Send Randoms')
  print('\t9 - Send All')
  print()
  print('\t0 - QUIT')
  print()
  inTxt = input("Option>")

  if (inTxt =='0'):
    #sys.exit()
    os._exit(0)
  elif (inTxt =='1'):
    post_data_vitals(user_token, site_url, site_data_suffix, randomise_dataset(person_data['vitals'], VALUE_VARIABILITY_AMOUNT))
  elif (inTxt =='2'):
    post_data(user_token, site_url, site_data_suffix, randomise_dataset(person_data['body'], VALUE_VARIABILITY_AMOUNT))
  elif (inTxt =='3'):
    post_data(user_token, site_url, site_data_suffix, randomise_dataset(person_data['physical_activity'], VALUE_VARIABILITY_AMOUNT))
  elif (inTxt =='4'):
    post_data(user_token, site_url, site_data_suffix, randomise_dataset(person_data['sleep'], VALUE_VARIABILITY_AMOUNT))
  elif (inTxt =='5'):
    post_data(user_token, site_url, site_data_suffix, randomise_dataset(person_data['ambient'], VALUE_VARIABILITY_AMOUNT))
  elif (inTxt =='6'):
    print("--  Properties:  body_temperature,",
          "blood_glucose,",
          "systolic_blood_pressure,", "diastolic_blood_pressure,",
          "heart_rate,", "body_weight,", "body_height,",
          "body_mass_index,", "body_fat_percentage,", "body_water,",
          "body_muscle,", "physical_activity,",
          "physical_activity_intensity,", "step_count,",
          "sleep_duration,", "sleep_deep_duration,", "sleep_light_duration,",
          "ambient_temperature,", "ambient_humidity")
    print("--")
    inPropTxt=input("Insert property>")
    inValueTxt=input("Insert value   >")
    new_value={}
    new_value['value']=inValueTxt 
    new_prop={}
    new_prop[inPropTxt]=new_value 
    post_data(user_token, site_url, site_data_suffix, new_prop)
  elif (inTxt =='9'):
    send_all(user_token, site_url, site_data_suffix, UPDATE_PERIOD, VALUE_VARIABILITY_AMOUNT)
  else:
    print('-- TODO...')
    
  
  
##
##  MAIN

if __name__ == '__main__':

  if len(sys.argv) < 3:
    print("NEED AS INPUT: server_settings person_file. Exiting...")
    exit()

  SETTINGS_FILE=sys.argv[1]
  PERSON_FILE=sys.argv[2]

  print('eCare Loading Settings....')

  # Read Settings
  with open(SETTINGS_FILE) as json_file:  
    settings_data = json.load(json_file)
    print(json.dumps(settings_data,indent=2))
    site_url=settings_data['host']
    site_auth_suffix=settings_data['loginSuffix']
    site_data_suffix=settings_data['userDataSuffix']

  print('eCare Loading Person....')

  # Read Person
  with open(PERSON_FILE) as json_file:  
    person_data = json.load(json_file)
    VALUE_VARIABILITY_AMOUNT = float(person_data['variability_amount'])
    UPDATE_PERIOD = int(person_data['period'])
  
  print('eCare Authenticating....')
  user_token = auth_portal(site_url, site_auth_suffix, person_data)
  
  threading.Timer(UPDATE_PERIOD, send_all, args=(user_token, site_url, site_data_suffix, UPDATE_PERIOD, VALUE_VARIABILITY_AMOUNT)).start()
  
  while True:
    menu(user_token, site_url, site_data_suffix, person_data, VALUE_VARIABILITY_AMOUNT, UPDATE_PERIOD)
