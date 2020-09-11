"""
This script perform some checks on GCP compute engine VM's
"""
import csv
from googleapiclient import discovery
from google.oauth2 import service_account



class VmChecks:
    """
        this class perform different checks on all gcp compute engine instances
    """
    def __init__(self, compute_client, all_info, project):
        self.compute_client = compute_client
        self.all_info = all_info
        self.project = project
    # --- check methods ---
    # this method check compute engine instances which are not running
    def check_1_1_instances_which_are_not_running(self):
        check_id = 1.1
        description = "Check for compute engine instances which are not running"
        if len(self.all_info) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp compute engine instances",
                resource_list=[],
                description=description
            )
            return res
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

    # this method check compute engine instance does not have deletion protection
    def check_1_2_deletion_protection(self):
        check_id = 1.2
        description = "Check for compute engine instances which does not have deletion protection"
        if len(self.all_info) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp compute engine instances",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for reg, inst in self.all_info.items():
                for m in inst:
                    if m['deletionProtection'] == False:
                        resource_list.append(m['id'])

            if len(resource_list) > 0:
                result = True
                reason = "Compute engine instances does not have deletion protection"
            else:
                result = False
                reason = "All Compute engine instances are deletion protected"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check instance check whether compute engine instance has all api access
    def check_1_3_all_api_access(self):
        check_id = 1.3
        description = "Check for compute engine instances has all api access"
        if len(self.all_info) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp compute engine instances",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for reg, inst in self.all_info.items():
                for m in inst:
                    scope = "https://www.googleapis.com/auth/cloud-platform"
                    if scope in str(m['serviceAccounts']):
                        resource_list.append(m['id'])
            if len(resource_list) > 0:
                result = True
                reason = "Compute engine instances have all api access"
            else:
                result = False
                reason = "Compute engine instances does not have all api access"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check whether compute engine instance disk has snapshot schedule
    def check_1_4_snapshot_schedule_for_compute_engine_disk(self):
        check_id = 1.4
        description = "Check for whether compute engine instance disk has snapshot schedule"
        if len(self.all_info) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp compute engine instances",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for reg, inst in self.all_info.items():
                for m in inst:
                    for disk in m['disks']:
                        name = disk['deviceName']
                        rep = self.check_snapshot_schedule(reg, name)
                        if rep == True:
                            resource_list.append(m['id'])

            if len(resource_list) > 0:
                result = True
                reason = "Compute engine instance disk has snapshot schedule"
            else:
                result = False
                reason = "Compute engine instances disks does not have snapshot schedule"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check compute engine does not have automatic restart policy
    def check_1_5_automatic_restart(self):
        check_id = 1.5
        description = "Check for whether compute engine instance does not have automatic restart policy"
        if len(self.all_info) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp compute engine instances",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for reg, inst in self.all_info.items():
                for m in inst:
                    if m['scheduling']['automaticRestart'] == False:
                       resource_list.append(m['id'])

            if len(resource_list) > 0:
                result = True
                reason = "Compute engine instance does not have automatic restart policy"
            else:
                result = False
                reason = "Compute engine instances does have automatic restart policy"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check compute engine has external ip address
    def check_1_6_external_ip_address(self):
        check_id = 1.6
        description = "Check for whether compute engine instance has external ip address"
        if len(self.all_info) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp compute engine instances",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for reg, inst in self.all_info.items():
                for m in inst:
                    for netf in m['networkInterfaces']:
                        if 'natIP' in str(m['networkInterfaces']):
                            resource_list.append(m['id'])

                    if m['scheduling']['automaticRestart'] == False:
                       resource_list.append(m['id'])

            if len(resource_list) > 0:
                result = True
                reason = "Compute engine instance has external ip address"
            else:
                result = False
                reason = "Compute engine instances has external ip address"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check compute engine instance does not hve any service account associated with it
    def check_1_7_check_for_service_account(self):
        check_id = 1.7
        description = "Check for whether compute engine instances does not have any service account"
        if len(self.all_info) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp compute engine instances",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for reg, inst in self.all_info.items():
                for m in inst:
                    if len(m['serviceAccounts']) <= 0:
                        resource_list.append(m['id'])

            if len(resource_list) > 0:
                result = True
                reason = "Compute engine instances does not have any service account"
            else:
                result = False
                reason = "Compute engine instances has service account"
            return self.result_template(check_id, result, reason, resource_list, description)

    # --- supporting methods ---
    def check_snapshot_schedule(self, zone, disk):
        response = self.compute_client.disks().get(project=self, zone=zone, disk=disk).execute()
        if 'resourcePolicies' in str(response):
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
        with open('gcp_vm.csv', 'w') as outcsv:
            headers = ["check_id", "result", "reason", "resource_list", "description"]
            writer = csv.DictWriter(outcsv, fieldnames=headers)
            writer.writeheader()
            for row in all_check_result:
                writer.writerow(row)
        print("Output write to:gcp_vm.csv")


class VmResource:
    """
        this class set different resource information to perform checks on all gcp compute engine instances
    """
    def __init__(self, service_account_file, project_id):
        credentials = service_account.Credentials.from_service_account_file(service_account_file)
        # building gcp compute client using gcp compute v1 api
        self.compute_client = discovery.build('compute', 'v1', credentials=credentials)
        self.project = project_id

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
        # print(all_info)
        return all_info


class ExecuteCheckVm:
    """
        This class Execute all check and generates report
    """
    def __init__(self, servive_account_file_path, project_id):
        self.servive_account_file_path = servive_account_file_path
        self.project_id = project_id

    # this method execute checks
    def perform_check(self):
        # getting resources for performing check
        resource_obj = VmResource(service_account_file=self.servive_account_file_path, project_id=self.project_id)
        all_info = resource_obj.all_instances()
        compute_client = resource_obj.compute_client
        project = resource_obj.project
        # initiate Checks class
        check_obj = VmChecks(compute_client=compute_client, all_info=all_info, project=project)
        all_check_result = [
            check_obj.check_1_1_instances_which_are_not_running(),
            check_obj.check_1_2_deletion_protection(),
            check_obj.check_1_3_all_api_access(),
            check_obj.check_1_4_snapshot_schedule_for_compute_engine_disk(),
            check_obj.check_1_5_automatic_restart(),
            check_obj.check_1_6_external_ip_address(),
            check_obj.check_1_7_check_for_service_account(),
        ]
        return all_check_result
