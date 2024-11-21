from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionCategorizeProgress(Action):
    def name(self) -> Text:
        return "action_categorize_progress"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        progress = tracker.get_slot("progress_input").lower()
        
        # Expanded keyword lists
        positive_keywords = [
            "completed", "finished", "achieved", "did", "made",
            "went to", "worked", "studied", "learned", "practiced",
            "exercised", "workout", "worked out", "read", "wrote",
            "created", "built", "organized", "planned", "attended"
        ]
        
        negative_keywords = [
            "didn't", "did not", "nothing", "couldn't", "failed",
            "missed", "skipped", "forgot", "no progress"
        ]

        # Check for negative indicators first
        if any(word in progress for word in negative_keywords):
            return [SlotSet("progress_category", "none")]
        
        # Check for positive activities
        if any(word in progress for word in positive_keywords):
            return [SlotSet("progress_category", "positive")]
            
        # Default to neutral if no clear indicators
        return [SlotSet("progress_category", "neutral")]

class ActionSuggestNextStep(Action):
    def name(self) -> Text:
        return "action_suggest_next_step"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        category = tracker.get_slot("progress_category")
        progress = tracker.get_slot("progress_input")

        suggestions = {
            "positive": "starting the next module tomorrow",
            "neutral": "setting aside 30 minutes tomorrow for focused work",
            "none": "trying a quick 10-minute review session to get back on track"
        }

        if category == "positive":
            dispatcher.utter_message(template="utter_positive_feedback",
                                  suggestion=suggestions[category])
        else:
            dispatcher.utter_message(template="utter_neutral_feedback",
                                  suggestion=suggestions[category])
        
        return []