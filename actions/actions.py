#actions.py
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionDebugIntent(Action):
    def name(self) -> Text:
        return "action_debug_intent"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        latest_message = tracker.latest_message
        intent = latest_message.get('intent', {}).get('name', 'unknown')
        confidence = latest_message.get('intent', {}).get('confidence', 0.0)

        print(f"Debug - Detected Intent: {intent} (confidence: {confidence})")
        return []


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


# New Actions for Career Development Flow
class ActionReviewCurrentSkills(Action):
    def name(self) -> Text:
        return "action_review_current_skills"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Logic to fetch user strengths and feedback history
        feedback_summary = "You’re doing great in collaboration and critical thinking. Recent feedback suggests focusing on leadership."
        dispatcher.utter_message(text=feedback_summary)
        return [SlotSet("feedback_summary", feedback_summary)]


class ActionAskAspirations(Action):
    def name(self) -> Text:
        return "action_ask_aspirations"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="What skills or roles would you like to develop for your career growth?")
        return []


class ActionSuggestNextStepCareer(Action):
    def name(self) -> Text:
        return "action_suggest_next_step_career"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        aspiration = tracker.get_slot("aspirations")

        suggestions = {
            "leadership": "Consider taking on team lead responsibilities in your current projects",
            "technical": "Look into advanced certifications in your technical field",
            "management": "Shadow a project manager and take on small team coordination tasks",
            "default": "Consider identifying specific skills you'd like to develop"
        }

        # Determine category based on aspiration text
        category = "default"
        if aspiration:
            aspiration_lower = aspiration.lower()
            if any(word in aspiration_lower for word in ["lead", "leadership", "manage people"]):
                category = "leadership"
            elif any(word in aspiration_lower for word in ["technical", "coding", "development"]):
                category = "technical"
            elif any(word in aspiration_lower for word in ["manage", "management", "project"]):
                category = "management"

        suggestion = suggestions[category]
        dispatcher.utter_message(text=f"Based on your interest in {aspiration}, here's a suggestion: {suggestion}")
        return []


class ActionProvideLearningPath(Action):
    def name(self) -> Text:
        return "action_provide_learning_path"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        aspiration = tracker.get_slot("aspirations")

        learning_paths = {
            "leadership": [
                "1. Take the 'Leadership Essentials' course on Coursera",
                "2. Read 'The Making of a Manager' by Julie Zhuo",
                "3. Join Toastmasters to improve communication skills"
            ],
            "technical": [
                "1. Complete advanced certification in your tech stack",
                "2. Build a portfolio project showcasing new skills",
                "3. Contribute to open source projects"
            ],
            "management": [
                "1. Take a Project Management Professional (PMP) course",
                "2. Shadow current project managers",
                "3. Read 'The Manager's Path' by Camille Fournier"
            ],
            "default": [
                "1. Schedule a career planning session with your manager",
                "2. Take personality and strengths assessments",
                "3. Research industry trends and in-demand skills"
            ]
        }

        # Determine category
        category = "default"
        if aspiration:
            aspiration_lower = aspiration.lower()
            if any(word in aspiration_lower for word in ["lead", "leadership", "manage people"]):
                category = "leadership"
            elif any(word in aspiration_lower for word in ["technical", "coding", "development"]):
                category = "technical"
            elif any(word in aspiration_lower for word in ["manage", "management", "project"]):
                category = "management"

        path = "\n".join(learning_paths[category])
        dispatcher.utter_message(text=f"Here's a suggested learning path for you:\n\n{path}")
        return [SlotSet("learning_path", path)]


class ActionTrackProgressCareer(Action):
    def name(self) -> Text:
        return "action_track_progress_career"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        progress_tracking = tracker.get_slot("progress_tracking")
        if progress_tracking:
            dispatcher.utter_message(text="Great! I’ll check in weekly to track your progress.")
        else:
            dispatcher.utter_message(text="No worries, feel free to let me know if you need further help.")
        return [SlotSet("progress_tracking", progress_tracking)]


class ActionSetPreviousFlow(Action):
    def name(self) -> Text:
        return "action_set_previous_flow"

    def run(self, dispatcher, tracker, domain):
        # Set the flow name
        current_flow = tracker.get_active_form_name() or "unknown"
        return [SlotSet("context.previous_flow_name", current_flow)]
