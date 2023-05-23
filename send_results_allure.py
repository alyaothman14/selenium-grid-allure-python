# We use this to send the allure results to our allure server that was built using docker-compose-allure
# More info could be found here: https://github.com/fescobar/allure-docker-service/tree/master/allure-docker-api-usage
# You can send the results using a bash file, jenkins or by code e.g python. I opted for python
import os, requests, json, base64

# This directory is where you have all your results locally, generally named as `allure-results`
allure_results_directory = '/allure-results'
# This url is where the Allure container is deployed. We are using localhost as example
allure_ip_address=os.environ.get('ALLURE_IP_ADDRESS')
allure_server="http://{0}:5050".format(allure_ip_address)
# Project ID according to existent projects in your Allure container - Check endpoint for project creation >> `[POST]/projects`
project_id = 'default'
#project_id = 'my-project-id'


current_directory = os.path.dirname(os.path.realpath(__file__))
results_directory = current_directory + allure_results_directory
files = os.listdir(results_directory)

print('FILES:')
results = []
for file in files:
    result = {}

    file_path = results_directory + "/" + file

    if os.path.isfile(file_path):
        try:
            with open(file_path, "rb") as f:
                content = f.read()
                if content.strip():
                    b64_content = base64.b64encode(content)
                    result['file_name'] = file
                    result['content_base64'] = b64_content.decode('UTF-8')
                    results.append(result)
                else:
                    print('Empty File skipped: '+ file_path)
        finally :
            f.close()
    else:
        print('Directory skipped: '+ file_path)

headers = {'Content-type': 'application/json'}
request_body = {
    "results": results
}
json_request_body = json.dumps(request_body)

ssl_verification = True

print("------------------SEND-RESULTS------------------")
response = requests.post(allure_server + '/allure-docker-service/send-results?project_id=' + project_id, headers=headers, data=json_request_body, verify=ssl_verification)
print("STATUS CODE:")
print(response.status_code)


print("------------------GENERATE-REPORT------------------")
execution_name = 'execution from my script'
execution_from = 'http://google.com'
execution_type = 'teamcity'
response = requests.get(allure_server + '/allure-docker-service/generate-report?project_id=' + project_id + '&execution_name=' + execution_name + '&execution_from=' + execution_from + '&execution_type=' + execution_type, headers=headers, verify=ssl_verification)
print("STATUS CODE:")
print(response.status_code)
print("RESPONSE:")
json_response_body = json.loads(response.content)

print('ALLURE REPORT URL:')
print(json_response_body['data']['report_url'])

