#OBJECTIVE
This project is targeted toward QA Engineers looking to run Selenium test cases using Selenium Grid and utilize Allure for comprehensive reporting while maintaining a test history.

A quick google search for setting up Selenium Grid, the recommended approach involves downloading and configuring the Selenium Grid server directly on your local machine. However, in this project, we opt for leveraging Docker as a powerful tool for several reasons:
1. Ease of setup and management: Docker simplifies the setup process by encapsulating the entire Selenium Grid infrastructure and its dependencies into containers. This means you don't have to worry about manually installing and configuring the Grid server, managing different versions, or dealing with compatibility issues. Docker takes care of all these aspects, allowing for a streamlined and consistent setup experience.

2. Portability and reproducibility: With Docker, you can package the entire Selenium Grid environment, including its configurations, dependencies, and required tools, into a single container. This container can be easily shared, distributed, and deployed across different environments, ensuring consistent behavior and reproducibility. It eliminates the need for manual setup and configuration on each individual machine, saving time and effort.

3. Scalability and flexibility: Docker enables easy scaling of the Selenium Grid infrastructure by allowing you to spin up multiple container instances of the Selenium nodes. This makes it straightforward to parallelize test execution across multiple browsers and platforms, enhancing the efficiency of your testing process. Docker's flexibility also enables you to customize and extend the Selenium Grid environment as per your specific requirements.

4. Isolation and resource management: Docker containers provide isolation for the Selenium Grid components, ensuring that changes or issues in one container do not affect others. Additionally, Docker allows you to manage resource allocation and utilization, such as CPU and memory limits, for each container. This enables efficient resource utilization and helps prevent resource contention among different components running on the same machine.

Helpful note: If you are not familiar with Docker, I would suggest going through this https://docker-curriculum.com/

#THIS PROJECT IS NOT:
This project is not a showcase of how a pipeline should be setup but rather on running testcases against selenium grid and reporting to allure.
The pipeline setup in the project is not the ideal case because
1. docker-compose.yml file is copied manually to the EC2 instance
2. There is no auto-scaling that is added
3. If multiple PRs are running at the same time, all testcases run will be send to the same selenium grid that might cause a bottleneck

#What is ideal:
The ideal cases will be to start the selenium grid on demand for each PR with auto-scaling using Infrastructure as Code and Self-Hosted Runners in Github Actions, i.e


#WANT TO RECREATE THE PROJECT
I recommend trying to recreating the setup yourself. To successfully do this, I recommend dividing the project into the following tasks/stories:
1. Get your selenium automation setup in programming language of your choice or you can fork one of my repo selenium-python or selenium-java
2. Ensure that selenium testcases are running locally on standalone browser
3. Work on setting up selenium-grid using docker to run locally https://github.com/SeleniumHQ/docker-selenium .Make sure you are using Selenium 4 and not 3 as the architecture has changed. Ensure you can access the selenium grid on localhost:4444
4. Work on changing your testcases to use the selenium grid instead of the standalone
    a. I would highly recommend to implement a way to be able to run testcases on standalone browser or against the grid
5. Work on setting up allure report docker https://github.com/fescobar/allure-docker-service and make sure you can access it on localhost:5050
6. Work on sending the results from your run to the allure service. There are multiple ways to do this here https://github.com/fescobar/allure-docker-service/tree/master/allure-docker-api-usage
7. Ensure that after running testcases that reports are published to allure services and you can access it.
8. [Optional]: Work on getting the testcases to run remotely by hosting the selenium-grid and allure service remotely on AWS or GCP or Digital Ocean. Usually DevOps Engineer can help you setup this 
9. [Optional]: Setup pipeline using github actions or Jenkins. Usually DevOps Engineer can help you setup this 

#Starting with this Project

#RUN Testcases Locally with standalone browser
There is no need to install or download any browser as we are using webdriver manager python library and it takes care or downloading and setting the binary.
Useful for debugging or writing testcases
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

#RUN selenium grid and serve reports to allure LOCALLY
Install docker https://docs.docker.com/desktop/install/mac-install/
Bring Allure Services up
docker-compose -f docker-compose.yml up -d allure

Bring Selenium grid up
docker-compose -f docker-compose-arm.yml up -d selenium-hub  selenium-chrome  selenium-firefox
Run Testcases
Option 1
Using DockerFile Image
Build docker image
Make sure you are in the repo directory
docker build -t=aothmana/selenium-grid-python .
Run testcases
ALLURE_IP_ADDRESS=<LOCAL_IP_ADDRESS> docker-compose-arm.yml up selenium-test

option 2
pip install
EXPORT HUB_HOST_NAME=<LOCAL_IP_ADDRESS> 
EXPORT ALLURE_IP_ADDRESS=<LOCAL_IP_ADDRESS>
pipenv run pytest --reruns 2 -n 8 --run_option grid && pipenv run python send_results_allure.py 

#RUN selenium grid and serve reports to allure Remotely
You will need an cloud service provider e.g GCP or AWS or Digital Ocean. I have used AWS
1. Setup EC2 Instance on AWS
2. Copy the docker-compose.yml to your instance
3. Start up allure service and selenium grid service on EC2 Instance 
4. Run testcases 
EXPORT HUB_HOST_NAME=<REMOTE_IP_ADDRESS> 
EXPORT ALLURE_IP_ADDRESS=<REMOTE_IP_ADDRESS>
pipenv run pytest --reruns 2 -n 8 --run_option grid && pipenv run python send_results_allure.py 
You can see an example of this in .github/workflow/run-selenium.yml




