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
        return [SlotSet("name", None), SlotSet("password", None), SlotSet("amount", None), SlotSet("price", None), SlotSet("side", None)]
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
            return [SlotSet("amount", None), SlotSet("price", None), SlotSet("side", None)]

        # Login Error
        elif type == 3:
            bot_message = "Your username or password is incorrect..."

            dispatcher.utter_message(text=bot_message)
            return [SlotSet("name", None), SlotSet("password", None), SlotSet("amount", None), SlotSet("price", None), SlotSet("side", None)]

        # Order Accepted
        elif type == 5:
            bot_message = "Your order has been accepted by the exchange"

            dispatcher.utter_message(text=bot_message)
            return [SlotSet("amount", None), SlotSet("price", None), SlotSet("side", None)]

        # Access denied
        elif type == 10:
            bot_message = "Hmmm... Looks like you don't have access to do that... :("

            dispatcher.utter_message(text=bot_message)
            return [SlotSet("amount", None), SlotSet("price", None), SlotSet("side", None)]

        # Cash Balance Insufficient
        elif type == 11:
            bot_message = "Your cash balance is insufficient"

            dispatcher.utter_message(text=bot_message)
            return [SlotSet("amount", None), SlotSet("price", None), SlotSet("side", None)]

        # Stocks insufficient
        elif type == 12:
            bot_message = "Your don't  have enough stocks to sell"

            dispatcher.utter_message(text=bot_message)
            return [SlotSet("amount", None), SlotSet("price", None), SlotSet("side", None)]

        # Check Balance
        elif type == 4:
            user_bean = r['userBean']

            cash_balance = user_bean['cash']
            stock_balance = user_bean['stocks']

            bot_message = "You have: " + str(cash_balance) + " LKR Cash Balance and " \
                          + str(stock_balance) + " Stock holdings"

            dispatcher.utter_message(text=bot_message)
            return []



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

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "name": [
                self.from_entity(entity="name", intent="get_user_name")
            ],
            "password": [
                self.from_entity(entity="password", intent="get_password"),
            ],
        }

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

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "name": [
                self.from_entity(entity="name", intent="get_user_name")
            ],
            "password": [
                self.from_entity(entity="password", intent="get_password"),
            ],
        }

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
        return handle_response(r, dispatcher, tracker)

class ActionLogOut(Action):

    def name(self) -> Text:
        return "action_log_out"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet("name", None), SlotSet("password", None)]


class ActionTrade(Action):

    def name(self) -> Text:
        return "action_trade"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user = tracker.get_slot("name")
        password = tracker.get_slot("password")

        if (user == None or password == None):
            dispatcher.utter_message(
                "You need to login or register first...")
        else:
            buttons = [

                {
                    'title': 'Buy',
                    'payload': '/buy_button'
                },

                {
                    'title': 'Sell',
                    'payload': '/sell_button'
                }
            ]

            dispatcher.utter_message(text="How do you want to trade?", buttons=buttons)
        return []

class ActionBuy(Action):

    def name(self) -> Text:
        return "action_buy"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            "You are going to buy stocks...")
        return [SlotSet("side", 1)]


class ActionSell(Action):

    def name(self) -> Text:
        return "action_sell"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            "You are going to sell stocks...")
        return [SlotSet("side", 2)]

class TradeForm(FormAction):
    """Collects trade information and sends it to back end"""

    def name(self):
        return "trade_form"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return [
            "amount",
            "price",
        ]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "amount": [
                self.from_entity(entity="amount", intent="get_amount"),
            ],
            "price": [
                self.from_entity(entity="price", intent="get_price"),
                self.from_entity(entity="price", intent="get_price"),
            ],
        }

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[EventType]:
        """Once we have an email, attempt to add it to the database"""

        # utter submit template
        dispatcher.utter_message(template="utter_success")
        return [FollowupAction("action_trade_confirm_prompt")]

class ActionTradeConfirmPrompt(Action):

    def name(self) -> Text:
        return "action_trade_confirm_prompt"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        amount = tracker.get_slot("amount")
        price = tracker.get_slot("price")
        side = tracker.get_slot("side")

        buttons = [

            {
                'title': 'Confirm',
                'payload': '/confirm_button'
            },

            {
                'title': 'Cancel',
                'payload': '/cancel_button'
            }
        ]
        side_str = "";
        if side == 1:
            side_str = "Buy"
        else:
            side_str = "Sell"

        dispatcher.utter_message(
            text="Do you want to " + side_str + " " + amount + " stocks at " + price + " LKR?",
            buttons=buttons)
        return []

class ActionTradeConfirm(Action):

    def name(self) -> Text:
        return "action_trade_confirm"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user = tracker.get_slot("name")
        password = tracker.get_slot("password")

        amount = tracker.get_slot("amount")
        price = tracker.get_slot("price")
        side = tracker.get_slot("side")

        side_str = "";
        if side == 1:
            side_str = "Buy"
        else:
            side_str = "Sell"

        request = {'username': user, 'password': password, 'stocks': amount, 'price': price, 'side': side}

        register_url = URL + "order"

        r = requests.post(url=register_url, json=request).json()

        dispatcher.utter_message(
            "You sent a " + side_str + " order of " + amount + " stocks at " + price + " LKR")

        return handle_response(r, dispatcher, tracker)


class ActionTradeCancel(Action):

    def name(self) -> Text:
        return "action_trade_cancel"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Trade Cancelled...")

        return [SlotSet("amount", None), SlotSet("price", None), SlotSet("side", None)]

class ActionCheckBalance(Action):

    def name(self) -> Text:
        return "action_check_balance"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user = tracker.get_slot("name")
        password = tracker.get_slot("password")

        if (user == None or password == None):
            dispatcher.utter_message(
                "You need to login or register first...")
            return []
        else:

            request = {'username': user, 'password': password}

            request_url = URL + "balance"

            r = requests.post(url=request_url, json=request).json()

            dispatcher.utter_message(
                "Checking your balance...")

            return handle_response(r, dispatcher, tracker)