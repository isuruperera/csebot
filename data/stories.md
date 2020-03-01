## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot

## answer explain single
* explain
    - utter_why
  
## explain name
* register
    - register_form
    - form{"name": "register_form"}
    - slot{"name": "name"}
* explain
    - utter_explain_why_name
    - register_form
    - form{"name": null}

## explain password
* register
    - register_form
    - form{"name": "register_form"}
    - slot{"password": "password"}
* explain
    - utter_explain_why_password
    - register_form
    - form{"name": null}
    
## explain login name
* login
    - login_form
    - form{"name": "login_form"}
    - slot{"name": "name"}
* explain
    - utter_explain_why_name
    - login_form
    - form{"name": null}

## explain login password
* login
    - login_form
    - form{"name": "login_form"}
    - slot{"password": "password"}
* explain
    - utter_explain_why_password
    - login_form
    - form{"name": null}
    
## log out
* log_out
  - action_log_out