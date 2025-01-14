# local_network_monitoring
Diploma project, local network monitoring using PYSNMP and Flutter for the UI

To run backend:
    1. Create venv:
        ```python -m venv venv```
    2. Start venv:
        On MacOS: ```python venv/bin/activate```
        On Windows: ```python venv/Scripts/activate```
    3. Start the "network_monitoring" file inside services

To run UI:
    1. Make sure no leftovers in the project are left:
        ```flutter clean```
    2. Resolve flutter dependencies:
        ```flutter pub get```
    3. Make a clean build for macOS (or any needed platform):
        Navigate to "UI/local_network_monitoring" and run the following commands:
            MacOS: ```flutter build macos --debug```
            Windows: ```flutter build windows --debug```