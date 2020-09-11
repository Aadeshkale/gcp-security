"""
This script perform some checks on GCP VPC network
"""
import csv
from googleapiclient import discovery
from google.oauth2 import service_account


class VpcChecks:
    """
        this class perform different checks on all gcp vpc network
    """
    def __init__(self, compute_client, vpc_net, firewall_rules, project):
        self.compute_client = compute_client
        self.vpc_net = vpc_net
        self.firewall_rules = firewall_rules
        self.project = project
    # --- check methods ---
    # this method check gcp vpc network has global routing
    def check_2_1_vpc_has_global_routing(self):
        check_id = 2.1
        description = "Check for gcp vpc network has global routing"
        if len(self.vpc_net) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp vpc network created",
                resource_list=[],
                description=description
            )
            return res
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
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp vpc network created",
                resource_list=[],
                description=description
            )
            return res
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
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp vpc network created",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for net in self.vpc_net:
                try:
                    if len(net['subnetworks']) <= 0:
                        res = "vpc_id:{}".format(net['id'])
                        resource_list.append(res)
                except:
                    pass
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
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp vpc network created",
                resource_list=[],
                description=description
            )
            return res
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
    
    # this method check gcp vpc subnet allow incoming internet traffic on which port on which
    def check_2_5_vpc_allow_internet_on_port(self):
        check_id = 2.5
        description = "Check for gcp vpc vpc subnet allow incoming internet traffic on which port"
        if len(self.vpc_net) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp vpc network created",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for net in self.vpc_net:
                network_name = net['name']
                res = self.check_incoming_internet_traffic(network_name)
                if res == False:
                  pass
                elif len(res) > 0:
                    resp = "vpc_id_{}".format(net['id'])
                    temp_res = dict()
                    temp_res[resp] = res
                    resource_list.append(temp_res)

            if len(resource_list) > 0:
                result = True
                reason = "GCP vpc subnet network network allow incoming internet traffic on which port"
            else:
                result = False
                reason = "GCP vpc network incoming traffic not allow on any port"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method is check flow logs is not enabled on particular custom vpc subnet
    def check_2_6_vpc_subnet_flow_logs_disabled(self):
        check_id = 2.6
        description = "Check for gcp custom vpc subnet flow logs is not enabled"
        if len(self.vpc_net) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp vpc network created",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for net in self.vpc_net:
                try:
                    subnetworks = net['subnetworks']
                    for subnet in subnetworks:
                        sub_res = subnet.split('/')
                        sub_name = sub_res[-1]
                        sub_region = sub_res[-3]
                        resp = self.check_subnet_flow_log(sub_name,sub_region)
                        if resp == False:
                            res = dict()
                            vpc = "vpc_id_{})".format(str(net['id']))
                            res[vpc] = sub_name
                            resource_list.append(res)
                except:
                    pass

            if len(resource_list) > 0:
                result = True
                reason = "GCP vpc custom subnet flow logs is not enabled"
            else:
                result = False
                reason = "ALL GCP vpc custom subnets flow logs are enabled"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method is check vpc has active peering connection with another vpc
    def check_2_7_vpc_has_active_peering_with_another_vpc(self):
        check_id = 2.7
        description = "Check vpc has active peering connection with another vpc"
        if len(self.vpc_net) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp vpc network created",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for net in self.vpc_net:
                try:
                    if net['peerings']:
                        for peering in net['peerings']:
                            if peering['state'] == 'ACTIVE':
                                name = peering['name']
                                res = dict()
                                vpc = "vpc_id_{})".format(str(net['id']))
                                res[vpc] = name
                                resource_list.append(res)
                except:
                    pass
            if len(resource_list) > 0:
                result = True
                reason = "GCP vpc has active peering connection with another vpc"
            else:
                result = False
                reason = "All GCP vpc does not have any active peering connection"
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

    # this method check gcp vpc network has incoming traffic firewall rule
    def check_incoming_internet_traffic(self, network_name):
        net_rule = []
        for rule in self.firewall_rules:
            if network_name in str(rule['network']):
                if '0.0.0.0/0' in str(rule) and rule['direction'] == 'INGRESS':
                    firewall_id = "firewall_id_{}".format(str(rule['id']))
                    res = dict()
                    res[firewall_id] = rule['allowed']
                    net_rule.append(res)

        if len(net_rule) > 0:
            return net_rule
        else:
            return False

    # this method checks flow logs are enabled on vpc subnet
    def check_subnet_flow_log(self, subnet_name, region):
        response = self.compute_client.subnetworks().get(
            project=self.project,
            region=region,
            subnetwork=subnet_name
        ).execute()
        try:
            return response['enableFlowLogs']
        except:
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


class VpcResource:
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
        response = self.compute_client.networks().list(project=self.project).execute()
        for network in response['items']:
            vpc_net.append(network)
        return vpc_net

    # this method returns information of all firewall rules available in particular project
    def all_firewall_rules(self):
        firewall_rules = []
        response = self.compute_client.firewalls().list(project=self.project).execute()
        for network in response['items']:
            firewall_rules.append(network)
        return firewall_rules


class ExecuteCheckVpc:
    """
        This class Execute all check and generates report
    """
    def __init__(self, servive_account_file_path, project_id):
        self.servive_account_file_path = servive_account_file_path
        self.project_id = project_id

    # this method execute checks
    def perform_check(self):
        # getting resources for performing check
        resource_obj = VpcResource(service_account_file=self.servive_account_file_path, project_id=self.project_id)
        vpc_net = resource_obj.all_vpc_networks()
        firewall_rules = resource_obj.all_firewall_rules()
        compute_client = resource_obj.compute_client
        project_id = resource_obj.project
        # initiate Checks class
        check_obj = VpcChecks(compute_client=compute_client, vpc_net=vpc_net, firewall_rules=firewall_rules, project=project_id)
        all_check_result = [
            check_obj.check_2_1_vpc_has_global_routing(),
            check_obj.check_2_2_vpc_has_auto_created_subnets(),
            check_obj.check_2_3_there_is_no_subnets(),
            check_obj.check_2_4_vpc_does_not_have_any_firewall_rule(),
            check_obj.check_2_5_vpc_allow_internet_on_port(),
            check_obj.check_2_6_vpc_subnet_flow_logs_disabled(),
            check_obj.check_2_7_vpc_has_active_peering_with_another_vpc(),
        ]
        return all_check_result

