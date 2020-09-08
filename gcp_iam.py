"""
This script perform some checks on GCP Iam
"""
import csv
from googleapiclient import discovery
from google.oauth2 import service_account

PROJECT_ID = "info1-284008"
SERVICE_ACCOUNT_FILE_PATH = "credentials/my_credentials.json"


class IamChecks:
    """
        this class perform different checks on GCP Iam
    """
    def __init__(self, iam_client, all_service_accounts):
        self.iam_client = iam_client
        self.all_service_accounts = all_service_accounts

    # --- check methods ---
    # this method check service account does have user managed key
    def check_3_1_service_account_user_managed_key(self):
        check_id = 3.1
        description = "Check for gcp service account does have user managed key"
        if len(self.all_service_accounts) <= 0:
            self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp iam service account created",
                resource_list=[],
                description=description
            )
        else:
            resource_list = []
            for sacc in self.all_service_accounts:
                res = self.check_no_of_user_managed_keys(sacc['name'])
                if res == True:
                    resource_list.append(sacc['name'])

            if len(resource_list) > 0:
                result = True
                reason = "Gcp service account does have user managed key"
            else:
                result = False
                reason = "ALL Gcp service accounts does have user managed key"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check service account is disabled
    def check_3_2_service_account_is_disabled(self):
        check_id = 3.2
        description = "Check for gcp service account is disabled"
        if len(self.all_service_accounts) <= 0:
            self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp iam service account created",
                resource_list=[],
                description=description
            )
        else:
            resource_list = []
            for sacc in self.all_service_accounts:
                try:
                    if sacc['disabled'] == True:
                        resource_list.append(sacc['name'])
                except:
                    pass
            if len(resource_list) > 0:
                result = True
                reason = "Gcp service account is disabled"
            else:
                result = False
                reason = "There is no service account which is disabled"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method service account has project owner permission



    # --- supporting methods ---
    # this method chek gcp iam service account has one or more keys
    def check_no_of_user_managed_keys(self, name):
        response = self.iam_client.projects().serviceAccounts().keys().list(name=name).execute()
        if 'USER_MANAGED' in str(response):
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
        with open('gcp_iam.csv', 'w') as outcsv:
            headers = ["check_id", "result", "reason", "resource_list", "description"]
            writer = csv.DictWriter(outcsv, fieldnames=headers)
            writer.writeheader()
            for row in all_check_result:
                writer.writerow(row)
        print("Output write to:gcp_iam.csv")


class IamResource:
    """
        this class set different resource information to perform checks on all gcp iam
    """
    def __init__(self, service_account_file, project_id):
        credentials = service_account.Credentials.from_service_account_file(service_account_file)
        # building gcp compute client using gcp compute v1 api
        self.iam_client = discovery.build('iam', 'v1', credentials=credentials)
        self.project = project_id

    # this method returns information of all compute engine of all zones
    def all_service_accounts(self):
        service_accounts_info = []
        name = 'projects/{}'.format(self.project)
        response = self.iam_client.projects().serviceAccounts().list(name=name).execute()
        for item in response['accounts']:
            service_accounts_info.append(item)
        return service_accounts_info


class ExecuteCheckIam:
    """
        This class Execute all check and generates report
    """
    def __init__(self, servive_account_file_path, project_id):
        self.servive_account_file_path = servive_account_file_path
        self.project_id = project_id

    # this method execute checks
    def perform_check(self):
        # getting resources for performing check
        resource_obj = IamResource(service_account_file=self.servive_account_file_path, project_id=self.project_id)
        all_service_accounts = resource_obj.all_service_accounts()
        iam_client = resource_obj.iam_client

        # initiate Checks class
        check_obj = IamChecks(iam_client=iam_client, all_service_accounts=all_service_accounts)
        all_check_result = [
            check_obj.check_3_1_service_account_user_managed_key(),
            check_obj.check_3_2_service_account_is_disabled(),
        ]
        check_obj.generate_csv(all_check_result)


exp = ExecuteCheckIam(servive_account_file_path=SERVICE_ACCOUNT_FILE_PATH, project_id=PROJECT_ID)
exp.perform_check()
