"""
This script perform some checks on GCP compute engine VM's
"""
import os
import csv
from googleapiclient import discovery
from google.oauth2 import service_account

PROJECT_ID = "info1-284008"
SERVICE_ACCOUNT_FILE_PATH = "credentials/my_credentials.json"

# client api for communication
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE_PATH)
COMPUTE_CLIENT = discovery.build('compute', 'v1', credentials=credentials)


class Checks:
    """
        this class perform different checks on all gcp compute engines
    """
    def __init__(self, all_info):
        self.all_info = all_info

    # --- check methods ---
    # this method check compute engine instances which are not running
    def check_1_1_instances_which_are_not_running(self):
        check_id = 1.1
        description = "Check for compute engine instances which are not running"
        if len(self.all_info) <= 0:
            self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp compute engine instances",
                resource_list=[],
                description=description
            )
        else:
            resource_list = []
            for reg, inst in self.all_info.items():
                for m in inst:
                    if m['status'] != 'RUNNING':
                        resource_list.append(m['id'])

            if len(resource_list) > 0:
                result = True
                reason = "Compute engine instances are not running"
            else:
                result = False
                reason = "All Compute engine instances are running"
            return self.result_template(check_id, result, reason, resource_list, description)

    # --- supporting methods ---
    # this method generates template for each check
    def result_template(self, check_id, result, reason, resource_list, description):
        template = dict()
        template['check_id'] = check_id
        template['result'] = result
        template['reason'] = reason
        template['resource_list'] = resource_list
        template['description'] = description
        return template

    # this method generate csv file for check results
    def generate_csv(self, all_check_result):
        with open('gcp_vm.csv', 'w') as outcsv:
            headers = ["check_id", "result", "reason", "resource_list", "description"]
            writer = csv.DictWriter(outcsv, fieldnames=headers)
            writer.writeheader()
            for row in all_check_result:
                writer.writerow(row)
        print("Output write to:gcp_vm.csv")


class Resource:
    """
        this class get different resource information to perform checks on all gcp compute engines
    """
    def __init__(self, compute_client, project):
        self.compute_client = compute_client
        self.project = project

    # this method returns list of all zones of gcp
    def get_zones(self):
        zones = self.compute_client.zones().list(project=self.project).execute()
        zones_list = []
        for i in zones['items']:
            zones_list.append(i['name'])
        return zones_list

    # this method returns information of all compute engine of all zones
    def all_instances(self):
        all_info = {}
        for n in self.get_zones():
            result = self.compute_client.instances().list(project=self.project, zone=n).execute()
            if 'items' in result:
                if len(result['items']) > 0:
                    all_info[n] = result['items']
        return all_info


class ExecuteCheck:
    """
        This class Execute all check and generates report
    """
    # this method execute checks
    def perform_check(self):
        # getting resources for performing check
        resource_obj = Resource(compute_client=COMPUTE_CLIENT, project=PROJECT_ID)
        all_info = resource_obj.all_instances()
        #
        check_obj = Checks(all_info=all_info)
        all_check_result = [
            check_obj.check_1_1_instances_which_are_not_running(),
        ]
        check_obj.generate_csv(all_check_result)


exp = ExecuteCheck()
exp.perform_check()