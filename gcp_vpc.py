"""
This script perform some checks on GCP VPC network
"""
import csv
from googleapiclient import discovery
from google.oauth2 import service_account

PROJECT_ID = "info1-284008"
SERVICE_ACCOUNT_FILE_PATH = "credentials/my_credentials.json"


class Checks:
    """
        this class perform different checks on all gcp vpc network
    """
    def __init__(self, compute_client, vpc_net):
        self.compute_client = compute_client
        self.vpc_net = vpc_net

    # --- check methods ---
    # this method check gcp vpc network has global routing
    def check_2_1_vpc_has_global_routing(self):
        check_id = 2.1
        description = "Check for gcp vpc network has global routing"
        if len(self.vpc_net) <= 0:
            self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp vpc network created",
                resource_list=[],
                description=description
            )
        else:
            resource_list = []
            for net in self.vpc_net:
                if net['routingConfig']['routingMode'] == 'GLOBAL':
                    res = "vpc_id:{}".format(net['id'])
                    resource_list.append(res)

            if len(resource_list) > 0:
                result = True
                reason = "GCP vpc network has global routing"
            else:
                result = False
                reason = "GCP vpc networks has no global routing"
            return self.result_template(check_id, result, reason, resource_list, description)


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
        with open('gcp_vpc.csv', 'w') as outcsv:
            headers = ["check_id", "result", "reason", "resource_list", "description"]
            writer = csv.DictWriter(outcsv, fieldnames=headers)
            writer.writeheader()
            for row in all_check_result:
                writer.writerow(row)
        print("Output write to:gcp_vpc.csv")


class Resource:
    """
        this class set different resource information to perform checks on all gcp vpc networks
    """
    def __init__(self, service_account_file, project_id):
        credentials = service_account.Credentials.from_service_account_file(service_account_file)
        # building gcp compute client using gcp compute v1 api
        self.compute_client = discovery.build('compute', 'v1', credentials=credentials)
        self.project = project_id

    # this method returns list of all zones of gcp
    # def get_zones(self):
    #     zones = self.compute_client.zones().list(project=self.project).execute()
    #     zones_list = []
    #     for i in zones['items']:
    #         zones_list.append(i['name'])
    #     return zones_list

    # this method returns information of all compute engine of all zones
    def all_vpc_networks(self):
        vpc_net = []
        response = self.compute_client.networks().list(project=PROJECT_ID).execute()
        for network in response['items']:
            vpc_net.append(network)
        return vpc_net


class ExecuteCheck:
    """
        This class Execute all check and generates report
    """
    # this method execute checks
    def perform_check(self):
        # getting resources for performing check
        resource_obj = Resource(service_account_file=SERVICE_ACCOUNT_FILE_PATH, project_id=PROJECT_ID)
        vpc_net = resource_obj.all_vpc_networks()
        compute_client = resource_obj.compute_client

        # initiate Checks class
        check_obj = Checks(compute_client=compute_client, vpc_net=vpc_net)
        all_check_result = [
            check_obj.check_2_1_vpc_has_global_routing(),
        ]
        check_obj.generate_csv(all_check_result)


exp = ExecuteCheck()
exp.perform_check()
