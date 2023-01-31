from typing import Any, Dict, Text, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json
import datetime as dt

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

            # check if user has received repair notification
            if tracker.get_slot("notification") == "deny":
                # ask if user has paid for subscription
                dispatcher.utter_message(template="utter_paid")
                if tracker.get_slot("paid") == "affirm":
                    # ask for router number
                    dispatcher.utter_message(template="utter_number")
                    # confirm router number
                    router_number = tracker.latest_message.get("text")
                    tracker.slots["router_number"] = router_number

                    router_number = tracker.get_slot("router_number")
                    dispatcher.utter_message(template="utter_correct", router_number=router_number)
                    # check details in json file
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
                else:
                    dispatcher.utter_message(template="utter_repair")
                return []




class ActionTime(Action):
    def name(self)->Text:
        return "action_show_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f"(dt.datetime.now())")

        return[]