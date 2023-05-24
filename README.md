#RUN Testcases Locally with standalone
1. Install Allure(Reporting tool):
brew install allure
2. Install the required Python packages:
pip install
3. Run the tests using one of the following commands:
Note if you are using visual studio, you can use the testing extention and all testcases will show. In pytest.ini the option debug is already passed.
pipenv run pytest -k "chrome" to run chrome only
pipenv run pytest -k "firefox" to run firefox only
pipenv run pytest to run all
4. Generate the Allure report:
allure generate && allure serve

#RUN GRID LOCAL and serve reports to allure
Install docker https://docs.docker.com/desktop/install/mac-install/
Build docker image
Make sure you are in the repo directory
docker build -t=aothmana/selenium-grid-python .
Bring Allure Services up
docker-compose -f docker-compose-allure.yml up -d allure
Change IP address
ALLURE_IP_ADDRESS=<LOCAL_IP_ADDRESS> docker-compose -f docker-compose-arm.yml up -d selenium-hub  selenium-chrome  selenium-firefox
#RUN JENKINS JOB LOCALLY


