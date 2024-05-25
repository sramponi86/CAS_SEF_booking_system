# Car Rental Project


Repository created and started from the SEF module from the ETH CAS AIS.
Added on top of the car rental project an ML module (CNN) for image recognition and identification
and a POC of front end regression testing using playwright and cucumber/behave

# Pre-requisites

Flask should be installed as well as torch, torchvision and their supporting libraries (numpy)
PIL should be also installed

Regarding the frontend testing , please install behave and pytest-playwright (follow official guidelines)

Usual command pip install {package-name}

Please pay attention eventually to the interpreter choosen to be used.

# Frontend tests

To run the front end tests and the corresponding scenarios covering the requirements
- go to the terminal
- move to the FE-tests folder level
- execute "behave --tags="@test"" (note that the tags are the ones that are related to the scenarios to be run)