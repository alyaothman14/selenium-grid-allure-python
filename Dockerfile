# We are using Dockefile to build our own image to use in docker-compose that will setup our test
# The image started from python:3
# We installed curl and jq as this will be used in the selenium-health-check to check that the grid is up and node are registred before running the test
# More info about the health check in selenium-health-check.sh
# Changed working dir on the image and copied the folder from the host to the image
# Installed the project depedency using pipenf
# Set env variables for the Selenium hub name and the allure report ip
FROM python:3
RUN apt-get update && apt-get install -y curl jq
WORKDIR /home/selenium-test
COPY . /home/selenium-test
RUN python -m pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install
RUN export HUB_HOST_NAME=$HUB_HOST_NAME
RUN export ALLURE_IP_ADDRESS=$ALLURE_IP_ADDRESS
ENTRYPOINT sh selenium-health-check.sh
  

