from typing import Any, Dict, Text, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, ConversationPaused
import json

class ActionNoInternet(Action):

    def name(self) -> Text:
        return "action_no_internet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # check if user's intent is "no_internet"
        if tracker.latest_message.get("intent") == "no_internet":
            # ask user to check if router is connected to a valid power source
            dispatcher.utter_message(template="utter_check")
            return []

class ActionCheck(Action):

    def name(self) -> Text:
        return "action_check"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            if tracker.latest_message.get("intent") == 'deny':
                dispatcher.utter_message(template="utter_connect:")
            else:
                dispatcher.utter_message(template="utter_notification")
                return []

class ActionNotification(Action):

    def name(self) -> Text:
        return "action_notificaion"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            if tracker.latest_message.get("intent") == 'affirm':
                dispatcher.utter_message(template="utter_repair")
            else:
                dispatcher.utter_message(template="utter_paid")
                return []          

class ActionPayment(Action):

    def name(self) -> Text:
        return "action_payment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            if tracker.latest_message.get("intent") ==  'deny':
                dispatcher.utter_message(template="utter_till")
            else:
                dispatcher.utter_message(template="utter_number")
                return []

class RouterCheck(Action):
    def name(self) ->Text:
        return "action_router_check"
        
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        if tracker.latest_message.get("intent") == "router_number":
            router_number = tracker.latest_message.get("text")
            tracker.slots["router_number"] = router_number

            router_number = tracker.get_slot("router_number")
            dispatcher.utter_message(template="utter_correct", router_number=router_number)
            
            with open("router_details.json") as f:
                data = json.load(f)
            
            for router in data["routers"]:
                if router["router_number"] == router_number:
                    if router["under_maintenance"]:
                        dispatcher.utter_message(template="utter_maintenance")
                    elif not router["is_active"]:
                        dispatcher.utter_message(template="utter_subscription_expired")
                    else:
                        dispatcher.utter_message(template="utter_customer_care")
                        return []

class ActionGoodbye(Action):

    def name(self):
        return "action_goodbye"

    def run(self, dispatcher, tracker, domain):
        if tracker.latest_message.get("text").lower() in ["bye", "goodbye", "thanks", "see you later"]:
            dispatcher.utter_message("Goodbye! Have a great day.")
            return [ConversationPaused()]