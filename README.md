- [Objective](#objective)
- [Pipeline Project Limitation](#pipeline-project-limitation)
  * [What is ideal pipeline setup?](#what-is-ideal-pipeline-setup?)
- [Recreate this project](#recreate-this-project)
- [Starting with this Project](#starting-with-this-project)
  * [Run Testcases Locally with standalone browser](#run-testcases-locally-with-standalone-browser)
  * [Run selenium grid and serve reports to allure LOCALLY](#run-selenium-grid-and-serve-reports-to-allure-locally)
  * [Run selenium grid and serve reports to allure REMOTELY](#run-selenium-grid-and-serve-reports-to-allure-remotely)
  
# Objective

This project is targeted toward QA Engineers looking to run Selenium test cases using Selenium Grid and utilize Allure for comprehensive reporting while maintaining a test history.

A quick google search for setting up Selenium Grid, the recommended approach involves downloading and configuring the Selenium Grid server directly on your local machine. However, in this project, we opt for leveraging Docker as a powerful tool for several reasons:
1. Ease of setup and management: Docker simplifies the setup process by encapsulating the entire Selenium Grid infrastructure and its dependencies into containers. This means you don't have to worry about manually installing and configuring the Grid server, managing different versions, or dealing with compatibility issues. Docker takes care of all these aspects, allowing for a streamlined and consistent setup experience.

2. Portability and reproducibility: With Docker, you can package the entire Selenium Grid environment, including its configurations, dependencies, and required tools, into a single container. This container can be easily shared, distributed, and deployed across different environments, ensuring consistent behavior and reproducibility. It eliminates the need for manual setup and configuration on each individual machine, saving time and effort.

3. Scalability and flexibility: Docker enables easy scaling of the Selenium Grid infrastructure by allowing you to spin up multiple container instances of the Selenium nodes. This makes it straightforward to parallelize test execution across multiple browsers and platforms, enhancing the efficiency of your testing process. Docker's flexibility also enables you to customize and extend the Selenium Grid environment as per your specific requirements.

4. Isolation and resource management: Docker containers provide isolation for the Selenium Grid components, ensuring that changes or issues in one container do not affect others. Additionally, Docker allows you to manage resource allocation and utilization, such as CPU and memory limits, for each container. This enables efficient resource utilization and helps prevent resource contention among different components running on the same machine.

Helpful note: If you are not familiar with Docker, I would suggest going through this [quick guide](https://docker-curriculum.com/)

# Pipeline Project Limitation
This project is not a showcase of how a pipeline should be setup but rather on running testcases against selenium grid and reporting to allure i.e QA side of things.
This project has certain Devops limitations that should be taken into consideration:
1. Manual Copying of docker-compose.yml: In the current setup, the docker-compose.yml file needs to be manually copied to the EC2 instance for remote execution. This manual step introduces a potential source of error and can be tedious when dealing with multiple instances or frequent updates to the configuration.
2. Lack of Auto-Scaling: The project does not implement auto-scaling for the Selenium Grid. Auto-scaling allows the infrastructure to dynamically adjust the number of instances based on workload demands. Without auto-scaling, it can be challenging to handle varying levels of concurrent test execution efficiently, potentially leading to resource limitations or underutilization.
3. PR Bottlenecks: When multiple pull requests (PRs) run simultaneously, all test cases are sent to the same Selenium Grid. This centralized approach can result in a potential bottleneck, as the Selenium Grid may become overloaded with concurrent test executions. It is important to consider ways to distribute the test workload across multiple instances or dynamically allocate resources based on PRs.

## What is ideal pipeline setup?
To address the limitations mentioned above, it is recommended to implement an ideal setup that leverages Infrastructure as Code and Self-Hosted Runners in GitHub Actions:

1. Dynamic Setup using Infrastructure as Code: Instead of manually copying the docker-compose.yml file, adopt an Infrastructure as Code approach, such as using tools like Terraform or AWS CloudFormation, to provision and configure the necessary infrastructure automatically. This ensures consistency, reproducibility, and eliminates the manual steps involved in setting up the remote execution environment.
2. Auto-Scaling with Selenium Grid: Implement auto-scaling for the Selenium Grid infrastructure. Utilize capabilities provided by cloud platforms, such as AWS Auto Scaling Groups or Kubernetes, to automatically scale the number of Selenium Grid instances based on demand. This allows the infrastructure to adapt to varying test workloads, ensuring efficient resource utilization and improved execution performance.
3.PR-specific Selenium Grid Instances: Instead of relying on a single Selenium Grid for all PRs, consider provisioning separate Selenium Grid instances dynamically for each PR. This can be achieved by leveraging infrastructure orchestration tools and dynamically allocating resources, such as creating isolated Docker containers or virtual machines, specifically dedicated to each PR. This approach helps prevent bottlenecks and allows parallel execution of tests across multiple isolated environments.

# Recreate this project
I recommend trying to recreating the setup yourself. To successfully do this, I recommend dividing the project into the following tasks/stories:
1. If you don't know docker, start small and reiterate as you learn.I would suggest going through this [quick guide](https://docker-curriculum.com/)
2. Get your selenium automation setup in any programming language of your choice or you can fork one of my repo [selenium-python](https://github.com/alyaothman14/selenium-python) or [selenium-java](https://github.com/alyaothman14/selenium-java)
3. Ensure that selenium testcases are running locally on standalone browser, similar to [here](https://github.com/alyaothman14/selenium-grid-allure-python/blob/main/tests/conftest.py#L37)
4. Work on setting up [selenium-grid using docker](https://github.com/SeleniumHQ/docker-selenium) to run locally.Make sure you are using Selenium 4 and not 3 as the architecture has changed. Ensure you can access the selenium grid on localhost:4444,similar to [here](https://github.com/alyaothman14/selenium-grid-allure-python/blob/main/docker-compose.yml). Note that if you are running an arm or mac M1 use [this](https://github.com/alyaothman14/selenium-grid-allure-python/blob/main/docker-compose-arm.yml)
5. Work on changing your testcases to use the selenium grid instead of the standalone similar to [here](https://github.com/alyaothman14/selenium-grid-allure-python/blob/main/tests/conftest.py#L52)
    a. I would highly recommend to implement a way to be able to run testcases on standalone browser or against the grid
5. Work on setting up [allure report docker](https://github.com/fescobar/allure-docker-service) and make sure you can access it on localhost:5050, similar to [here](https://github.com/alyaothman14/selenium-grid-allure-python/blob/main/docker-compose-arm.yml#L44)
6. Work on sending the results from your run to the allure service. There are multiple ways to do this [here](https://github.com/fescobar/allure-docker-service/tree/master/allure-docker-api-usage)
7. Ensure that after running testcases that reports are published to allure services and you can access it.
8. [Optional]: Work on getting the testcases to run remotely by hosting the selenium-grid and allure service remotely on AWS or GCP or Digital Ocean. Usually DevOps Engineer can help you setup this 
9. [Optional]: Setup pipeline using github actions or Jenkins. Usually DevOps Engineer can help you setup this 

# Starting with this Project

## Run Testcases Locally with standalone browser
There is no need to install or download any browser as we are using webdriver manager python library and it takes care or downloading and setting the binary.
Useful for debugging or writing testcases
1. Install Allure(Reporting tool):
```bash brew install allure ```
2. Install the required Python packages:
```bash pip install ```
3. Run the tests using one of the following commands:
Note if you are using visual studio, you can use the testing extention and all testcases will show. In pytest.ini the option debug is already passed.
```bash 
pipenv run pytest -k "chrome" to run chrome only
pipenv run pytest -k "firefox" to run firefox only
pipenv run pytest to run all 
```
4. Generate the Allure report:
```bash 
allure generate && allure serve
```

## Run selenium grid and serve reports to allure LOCALLY
**Install docker** https://docs.docker.com/desktop/install/mac-install/

**Bring Allure Services up**
```bash 
docker-compose -f docker-compose.yml up -d allure
```

**Bring Selenium grid up**
```bash 
docker-compose -f docker-compose-arm.yml up -d selenium-hub  selenium-chrome  selenium-firefox
```

**Run Testcases**
Option 1
Using DockerFile Image
Build docker image
Make sure you are in the repo directory
```bash 
docker build -t=aothmana/selenium-grid-python .
```
Run testcases
```bash 
ALLURE_IP_ADDRESS=<LOCAL_IP_ADDRESS> docker-compose-arm.yml up selenium-test
```
OR
option 2
```bash 
pip install
export HUB_HOST_NAME=<LOCAL_IP_ADDRESS> 
export ALLURE_IP_ADDRESS=<LOCAL_IP_ADDRESS>
pipenv run pytest --reruns 2 -n 8 --run_option grid
pipenv run python send_results_allure.py 
```

## Run selenium grid and serve reports to allure REMOTELY
You will need an cloud service provider e.g GCP or AWS or Digital Ocean. I have used AWS
Note that I have terminated the EC2 Instance but attached images for showcase
1. Setup EC2 Instance on AWS
2. Copy the docker-compose.yml to your instance
3. Start up allure service and selenium grid service on EC2 Instance 
4. Run testcases 
```bash 
export HUB_HOST_NAME=<REMOTE_IP_ADDRESS> 
export ALLURE_IP_ADDRESS=<REMOTE_IP_ADDRESS>
pipenv run pytest --reruns 2 -n 8 --run_option grid && pipenv run python send_results_allure.py 
```
You can see an example of this in .github/workflow/run-selenium.yml

<img width="1418" alt="image" src="https://github.com/alyaothman14/selenium-grid-allure-python/assets/87079479/1060f924-ed5d-4ec0-a099-4c773e0826ae">
<img width="1416" alt="image" src="https://github.com/alyaothman14/selenium-grid-allure-python/assets/87079479/601abc6b-0be8-4be7-958f-40f1dd6dc9f0">





