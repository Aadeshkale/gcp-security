"""
This script perform some checks on GCP Iam
"""
import csv
from googleapiclient import discovery
from google.oauth2 import service_account


class IamChecks:
    """
        this class perform different checks on GCP Iam
    """
    def __init__(self, iam_client, all_service_accounts, policies):
        self.iam_client = iam_client
        self.all_service_accounts = all_service_accounts
        self.policies = policies

    # --- check methods ---
    # this method check service account does have user managed key
    def check_3_1_service_account_user_managed_key(self):
        check_id = 3.1
        description = "Check for gcp service account does have user managed key"
        if len(self.all_service_accounts) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp iam service account created",
                resource_list=[],
                description=description
            )
            return res
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
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp iam service account created",
                resource_list=[],
                description=description
            )
            return res
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

    # this method service account has project owner policy role
    def check_3_3_service_account_has_owner_permission(self):
        check_id = 3.3
        description = "Check for gcp service account has project owner policy role"
        if len(self.all_service_accounts) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp iam service account created",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for sacc in self.all_service_accounts:
                if len(self.policies) > 0:
                    for p in self.policies:
                        if sacc['name'] in p['members'] and p['role'] == 'roles/owner':
                            resource_list.append(sacc['name'])

            if len(resource_list) > 0:
                result = True
                reason = "Gcp service account has project owner policy role"
            else:
                result = False
                reason = "There is no service account with project owner policy role"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check gcp project has more than one owner user
    def check_3_4_more_than_one_owner(self):
        check_id = 3.4
        description = "Check for gcp project has more than one owner user"
        if len(self.all_service_accounts) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp iam service account created",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            owner_list = []
            if len(self.policies) > 0:
                for p in self.policies:
                    if p['role'] == 'roles/owner' and 'user:' in str(p['members']):
                        for member in p['members']:
                            if 'user:' in member:
                                owner_list.append(member)
            if len(owner_list) > 1:
                for mem in owner_list:
                    resource_list.append(mem)

            if len(resource_list) > 0:
                result = True
                reason = "Gcp project has more than one owner user"
            else:
                result = False
                reason = "There is only one project owner"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method service account has project editor policy role
    def check_3_5_service_account_has_editor_role(self):
        check_id = 3.5
        description = "Check for gcp service account has project editor policy role"
        if len(self.all_service_accounts) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp iam service account created",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for sacc in self.all_service_accounts:
                if len(self.policies) > 0:
                    for p in self.policies:
                        if sacc['name'] in p['members'] and p['role'] == 'roles/editor':
                            resource_list.append(sacc['name'])

            if len(resource_list) > 0:
                result = True
                reason = "Gcp service account has project editor policy role"
            else:
                result = False
                reason = "There is no service account with project editor policy role"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check gcp project has more than one editor user
    def check_3_6_more_than_one_editor(self):
        check_id = 3.6
        description = "Check for gcp project has more than one editor user"
        if len(self.all_service_accounts) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp iam service account created",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            owner_list = []
            if len(self.policies) > 0:
                for p in self.policies:
                    if p['role'] == 'roles/editor' and 'user:' in str(p['members']):
                        for member in p['members']:
                            if 'user:' in member:
                                owner_list.append(member)
            if len(owner_list) > 1:
                for mem in owner_list:
                    resource_list.append(mem)

            if len(resource_list) > 0:
                result = True
                reason = "Gcp project has more than one editor user"
            else:
                result = False
                reason = "There is only one project editor or there is no editor user"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check gcp project viewer user
    def check_3_7_there_is_project_viewer(self):
        check_id = 3.7
        description = "Check for gcp project has viewer user"
        if len(self.all_service_accounts) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp iam service account created",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            if len(self.policies) > 0:
                for p in self.policies:
                    if p['role'] == 'roles/viewer' and 'user:' in str(p['members']):
                        for member in p['members']:
                            if 'user:' in member:
                                resource_list.append(member)

            if len(resource_list) > 0:
                result = True
                reason = "Gcp project has viewer user"
            else:
                result = False
                reason = "There is no project viewer user"
            return self.result_template(check_id, result, reason, resource_list, description)

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
        # building gcp iam client using gcp compute v1 api
        self.iam_client = discovery.build('iam', 'v1', credentials=credentials)
        self.resource_manager_client = discovery.build("cloudresourcemanager", "v1", credentials=credentials)
        self.project = project_id

    # this method returns information of all compute engine of all zones
    def all_service_accounts(self):
        service_accounts_info = []
        name = 'projects/{}'.format(self.project)
        response = self.iam_client.projects().serviceAccounts().list(name=name).execute()
        for item in response['accounts']:
            service_accounts_info.append(item)
        return service_accounts_info

    def all_policies(self):
        try:
            policy = self.resource_manager_client.projects().getIamPolicy(resource=self.project).execute()
            res = policy['bindings']
        except:
            return list()
        return res


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
        policies = resource_obj.all_policies()
        iam_client = resource_obj.iam_client

        # initiate Checks class
        check_obj = IamChecks(iam_client=iam_client, all_service_accounts=all_service_accounts, policies=policies)
        all_check_result = [
            check_obj.check_3_1_service_account_user_managed_key(),
            check_obj.check_3_2_service_account_is_disabled(),
            check_obj.check_3_3_service_account_has_owner_permission(),
            check_obj.check_3_4_more_than_one_owner(),
            check_obj.check_3_5_service_account_has_editor_role(),
            check_obj.check_3_6_more_than_one_editor(),
            check_obj.check_3_7_there_is_project_viewer(),
        ]
        return all_check_result

