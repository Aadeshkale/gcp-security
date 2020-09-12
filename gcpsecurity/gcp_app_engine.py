"""
This script perform some checks on GCP App Engine
"""
import csv
from googleapiclient import discovery
from google.oauth2 import service_account


class GaeChecks:
    """
        this class perform different checks on GCP Cloud Sql
    """
    def __init__(self, gae_client, services_info, project):
        self.gae_client = gae_client
        self.services_info = services_info
        self.project = project

    # --- check methods ---
    # this method check gcp app engine has more than one service
    def check_6_1_app_engine_has_many_services(self):
        check_id = 6.1
        description = "Check for gcp app engine has more than one service"
        if len(self.services_info) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp app engine app",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            if len(self.services_info) > 0:
                for ser in self.services_info:
                    try:
                        resource_list.append(ser['name'])
                    except:
                        pass
            if len(resource_list) > 1:
                result = True
                reason = "Gcp app engine has more than one service"
            else:
                result = False
                reason = "Gcp app engine has only one service"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check gcp app engine service more than one version
    def check_6_2_app_engine_service_has_more_than_one_versions(self):
        check_id = 6.2
        description = "Check for gcp app engine service more than one version"
        if len(self.services_info) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp app engine app",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for ser in self.services_info:
                id = ser['id']
                res = self.check_multiple_versions(service_id=id)
                if type(res) == bool:
                    pass
                else:
                    data = dict()
                    data[ser['name']] = res
                    resource_list.append(data)

        if len(resource_list) > 0:
                result = True
                reason = "Gcp app engine service more than one version"
        else:
            result = False
            reason = "Gcp app engine each service has only one version"
        return self.result_template(check_id, result, reason, resource_list, description)

    # this method check app engine service is not serving
    def check_6_3_app_engine_service_is_not_serving(self):
        check_id = 6.3
        description = "Check for gcp app engine service is not serving"
        if len(self.services_info) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp app engine app",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for ser in self.services_info:
                id = ser['id']
                res = self.check_multiple_versions(service_id=id)
                if res == False:
                    resource_list.append(ser['name'])

        if len(resource_list) > 0:
                result = True
                reason = "Gcp app engine service is not serving"
        else:
            result = False
            reason = "Gcp app engine all services are in serving state"
        return self.result_template(check_id, result, reason, resource_list, description)

    # --- supporting methods ---
    def check_multiple_versions(self, service_id):
        resp = self.gae_client.apps().services().versions().list(
            appsId=self.project,
            servicesId=service_id
        ).execute()
        ver_list = []
        if len(resp['versions']) > 1:
            for ver in resp['versions']:
                ver_list.append(ver['id'])
            return ver_list
        else:
            return False

    def check_service_status(self, service_id):
        resp = self.gae_client.apps().services().versions().list(
            appsId=self.project,
            servicesId=service_id
        ).execute()
        if len(resp['versions']) > 0:
            ver_list = []
            for ver in resp['versions']:
                if ver['servingStatus'] == 'SERVING':
                    ver_list.append(ver['id'])

            if len(ver_list) > 0:
                return True
            else:
                return False
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
        with open('gcp_app_engine.csv', 'w') as outcsv:
            headers = ["check_id", "result", "reason", "resource_list", "description"]
            writer = csv.DictWriter(outcsv, fieldnames=headers)
            writer.writeheader()
            for row in all_check_result:
                writer.writerow(row)
        print("Output write to:gcp_app_engine.csv")


class GaeResource:
    """
        this class set different resource information to perform checks on all gcp cloud sql
    """
    def __init__(self, service_account_file, project_id):
        credentials = service_account.Credentials.from_service_account_file(service_account_file)
        # building gcp compute client using gcp GAE v1 api
        self.gae_client = discovery.build('appengine', 'v1', credentials=credentials)
        self.project = project_id

    # this method returns information of all GAP
    def gae_services_info(self):
        services_info = []
        try:
            resp = self.gae_client.apps().services().list(appsId="info1-284008").execute()
            for ser in resp['services']:
                services_info.append(ser)
        except:
            pass
        return services_info

class ExecuteCheckGae:
    """
        This class Execute all check and generates report
    """
    def __init__(self, servive_account_file_path, project_id):
        self.servive_account_file_path = servive_account_file_path
        self.project_id = project_id

    # this method execute checks
    def perform_check(self):
        # getting resources for performing check
        resource_obj = GaeResource(service_account_file=self.servive_account_file_path, project_id=self.project_id)
        gae_client = resource_obj.gae_client
        project = resource_obj.project
        services_info = resource_obj.gae_services_info()
        # initiate Checks class
        check_obj = GaeChecks(gae_client=gae_client, services_info=services_info, project=project)
        all_check_result = [
            check_obj.check_6_1_app_engine_has_many_services(),
            check_obj.check_6_2_app_engine_service_has_more_than_one_versions(),
            check_obj.check_6_3_app_engine_service_is_not_serving(),
        ]
        return all_check_result
