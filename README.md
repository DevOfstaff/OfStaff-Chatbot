# Steps to run the two Rasa flows locally
1. Clone this repo locally.
2. Go to main branch.
3. Create a VENV and activate it.
4. Set RASA_PRO_LICENSE and OPENAI_API_KEY in the .env file.
5. Install rasa locally.
- Option 1: Follow these instructions:
https://rasa.com/docs/rasa-pro/installation/python/installation
- Option 2: Enter these commands:
```
pip install uv
uv pip install rasa-pro --extra-index-url=https://europe-west3-python.pkg.dev/rasa-releases/rasa-pro-python/simple/
```
6. Enter this command:
```
rasa train
```
7. Enter this command:
```
rasa inspect
```
8. Into the chatbot that opens, enter something like "check in" for Flow 1, and "I want to plan my career growth" for Flow 2.


# Notes: 
1. This is a modified Rasa quickstart tutorial, originally for getting started with Rasa Pro in the browser using GitHub Codespaces.
2. Below is part of that tutorial which may be useful:
**Run Custom Actions:**
  In Rasa 3.10 and later, custom actions are automatically run as part of your running assistant. To double-check that this is set up correctly, ensure that your `endpoints.yml` file contains the following configuration:
   ```
   action_endpoint:
      actions_module: "actions" # path to your actions package
    ```
   Then re-run your assistant via `rasa inspect` every time you make changes to your custom actions.
