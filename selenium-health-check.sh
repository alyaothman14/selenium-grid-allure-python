# We ensure that the grid is up with nodes registered before running the test
index=0
max_retries=20
echo "Checking if hub is ready"

while [ "$( curl -s http://$HUB_HOST_NAME:4444/wd/hub/status | jq -r .value.ready )" != "true"] 
do
	if [ "$index" -eq "$max_retries" ]; then
    echo "Maximum number of retries reached to check selenium grid is up and running. Exiting..."
    break
    fi
    echo "Node not ready. Status: $(curl -s http://$HUB_HOST_NAME:4444/wd/hub/status | jq -r .value.ready)"
    index=$((index + 1))
    sleep 3
done


# The command to run our test
pipenv run pytest --reruns 2 -n 8 --run_option grid 
# The command to send the results to the allure server
pipenv run python send_results_allure.py 
