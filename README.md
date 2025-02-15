# Install as User
Navigate to the "installers" folder and download the installer according to your platform

Follow the installation guide.

$${\color{red}!! \space Currently \space the \space container \space is \space not \space hosted \space on \space a \space cloud, \space so \space in \space order \space to \space run \space the \space app, \space you \space need \space to \space start \space a \space docker, \space which \space runs \space the \space backend \space !!}$$

# Install as Developer
Diploma project, local network monitoring using PYSNMP and Flutter for the UI

Python version used: 3.11.1
Flutter 3.22.2 • channel stable • https://github.com/flutter/flutter.git
Framework • revision 761747bfc5 (7 months ago) • 2024-06-05 22:15:13 +0200
Engine • revision edd8546116
Tools • Dart 3.4.3 • DevTools 2.34.3

To run backend:
    Start via docker:
        1. Execute in root:
            build the container: ```docker build -t network_monitor .```
            create and run: ```docker run -it --rm -p 8001:8001 -p 8050:8050 -p 62079:62079 --name network_monitor_container network_monitor```
            if container exists: ```docker start network_monitor_container```

    Start manually:
        1. Create venv:
            ```python -m venv venv```
            Or if using "pyenv":
                ```1. pyenv install 3.11.1```
                ```2. /Users/yourname/.pyenv/versions/3.10.9/bin/python -m venv venv```

        2. Start venv:
            On MacOS: ```source venv/bin/activate```
            On Windows: ```source venv/Scripts/activate```
        3. Install the python requirements:
            ```pip install -r Backend/requirements.txt```
        4. Make sure the correct python interpretes is selected.
        5. Start the service:
            1. Go to "Backend" directory and execute:
                ```python app.py```

To run UI:
    1. Make sure no leftovers in the project are left:
        ```flutter clean```
    2. Resolve flutter dependencies:
        ```flutter pub get```
    3. Make a clean build for macOS (or any needed platform):
        Navigate to "UI/local_network_monitoring" and run the following commands:
            MacOS: ```flutter build macos --debug```
            Windows: ```flutter build windows --debug```
