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
    def __init__(self, compute_client, vpc_net, firewall_rules):
        self.compute_client = compute_client
        self.vpc_net = vpc_net
        self.firewall_rules = firewall_rules

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

    # this method check gcp vpc network has auto created subnets
    def check_2_2_vpc_has_auto_created_subnets(self):
        check_id = 2.2
        description = "Check for gcp vpc network has auto created subnets"
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
                if net['autoCreateSubnetworks'] == True:
                    res = "vpc_id:{}".format(net['id'])
                    resource_list.append(res)

            if len(resource_list) > 0:
                result = True
                reason = "GCP vpc network has network has auto created subnets"
            else:
                result = False
                reason = "GCP vpc network has no auto created subnets"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check gcp vpc network has no subnets
    def check_2_3_there_is_no_subnets(self):
        check_id = 2.3
        description = "Check for gcp vpc network has network has no subnets created"
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
                if len(net['subnetworks']) <= 0:
                    res = "vpc_id:{}".format(net['id'])
                    resource_list.append(res)

            if len(resource_list) > 0:
                result = True
                reason = "GCP vpc network has network has no subnets created"
            else:
                result = False
                reason = "GCP vpc network has subnets created"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check gcp vpc network does not have any firewall rule
    def check_2_4_vpc_does_not_have_any_firewall_rule(self):
        check_id = 2.4
        description = "Check for gcp vpc network does not have any firewall rule"
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
                network_name = net['name']
                res = self.check_firewall_rule_exits(network_name)
                if res == False:
                    resp = "vpc_id:{}".format(net['id'])
                    resource_list.append(resp)

            if len(resource_list) > 0:
                result = True
                reason = "GCP vpc network does not have any firewall rule"
            else:
                result = False
                reason = "GCP vpc networks have firewall rules"
            return self.result_template(check_id, result, reason, resource_list, description)




    # --- supporting methods ---
    # this method check gcp vpc network has firewall rule
    def check_firewall_rule_exits(self, network_name):
        net_rule = []
        for rule in self.firewall_rules:
            if network_name in str(rule['network']):
                net_rule.append(rule)
        if len(net_rule) > 0:
            return True
        else:
            return False




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

    # this method returns information of all vpc networks available in particular project
    def all_vpc_networks(self):
        vpc_net = []
        response = self.compute_client.networks().list(project=PROJECT_ID).execute()
        for network in response['items']:
            vpc_net.append(network)
        return vpc_net

    # this method returns information of all firewall rules available in particular project
    def all_firewall_rules(self):
        firewall_rules = []
        response = self.compute_client.firewalls().list(project=PROJECT_ID).execute()
        for network in response['items']:
            firewall_rules.append(network)
        return firewall_rules

class ExecuteCheck:
    """
        This class Execute all check and generates report
    """
    # this method execute checks
    def perform_check(self):
        # getting resources for performing check
        resource_obj = Resource(service_account_file=SERVICE_ACCOUNT_FILE_PATH, project_id=PROJECT_ID)
        vpc_net = resource_obj.all_vpc_networks()
        firewall_rules = resource_obj.all_firewall_rules()
        compute_client = resource_obj.compute_client

        # initiate Checks class
        check_obj = Checks(compute_client=compute_client, vpc_net=vpc_net, firewall_rules=firewall_rules)
        all_check_result = [
            check_obj.check_2_1_vpc_has_global_routing(),
            check_obj.check_2_2_vpc_has_auto_created_subnets(),
            check_obj.check_2_3_there_is_no_subnets(),
            check_obj.check_2_4_vpc_does_not_have_any_firewall_rule(),
        ]
        check_obj.generate_csv(all_check_result)




exp = ExecuteCheck()
exp.perform_check()
