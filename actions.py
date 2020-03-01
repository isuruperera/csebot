import logging
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.events import (
    SlotSet,
    EventType,
    FollowupAction,
)
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from typing import Any, Dict, List, Text, Union

logger = logging.getLogger(__name__)

# URL to our Back End Server
URL = "http://localhost:8080/api/"

# Handles responses from the Back End Server
def handle_response(r, dispatcher: CollectingDispatcher, tracker: Tracker):
    logger.info(r)

    status = r['status']
    logger.warn(status)

    if (status == 'FAIL'):
        dispatcher.utter_message(template="utter_error")
        return []
    else:
        type = r['type']
        logger.warn(type)

        # Login or Register
        if type == 1 or type == 2:
            user_bean = r['userBean']

            cash_balance = user_bean['cash']
            stock_balance = user_bean['stocks']

            bot_message = "You have: " + str(cash_balance) + " LKR Cash Balance and " \
                          + str(stock_balance) + " Stock holdings"

            dispatcher.utter_message(text=bot_message)
            return []

        # Login Error
        elif type == 3:
            bot_message = "Your username or password is incorrect..."

            dispatcher.utter_message(text=bot_message)
            return [SlotSet("name", None), SlotSet("password", None)]



class RegisterForm(FormAction):
    """Collects sales information and sends it to back end"""

    def name(self):
        return "register_form"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return [
            "name",
            "password",
        ]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[EventType]:
        """Once we have an details, attempt to add it to the back end"""

        user = tracker.get_slot("name")
        password = tracker.get_slot("password")

        request = {'username': user, 'password': password}

        register_url = URL + "register"

        r = requests.post(url=register_url, json=request).json()

        # utter submit template
        dispatcher.utter_message(template="utter_thanks")
        return handle_response(r, dispatcher, tracker)

class LoginForm(FormAction):
    """Collects sales information and sends it to back end"""

    def name(self):
        return "login_form"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return [
            "name",
            "password",
        ]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[EventType]:
        """Once we have an details, attempt to login at the back end"""

        user = tracker.get_slot("name")
        password = tracker.get_slot("password")

        request = {'username': user, 'password': password}

        register_url = URL + "login"

        r = requests.post(url=register_url, json=request).json()

        # utter submit template
        dispatcher.utter_message(text="You're logging in...")
        handle_response(r, dispatcher, tracker)
        return []

class ActionLogOut(Action):

    def name(self) -> Text:
        return "action_log_out"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet("name", None), SlotSet("password", None)]