"""
This script perform some checks on GCP Cloud Sql
"""
import csv
from googleapiclient import discovery
from google.oauth2 import service_account


class SqlChecks:
    """
        this class perform different checks on GCP Cloud Sql
    """
    def __init__(self, sql_client, sql_instances):
        self.sql_client = sql_client
        self.sql_instances = sql_instances

    # --- check methods ---
    # this method check gcp cloud sql instance has public internet access
    def check_4_1_cloud_sql_public_access(self):
        check_id = 4.1
        description = "Check for gcp cloud sql instance has public internet access"
        if len(self.sql_instances) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp cloud sql instances created",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for inst in self.sql_instances:
                try:
                    if inst['settings']['ipConfiguration']['ipv4Enabled'] == True:
                        resource_list.append(inst['connectionName'])
                except:
                    pass

            if len(resource_list) > 0:
                result = True
                reason = "Gcp cloud sql instance has public internet access"
            else:
                result = False
                reason = "ALL Gcp cloud sql instances does not have public internet access"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check gcp cloud sql does not have auto backup
    def check_4_2_cloud_sql_backup_config(self):
        check_id = 4.2
        description = "Check for gcp cloud sql instance does not have auto backup"
        if len(self.sql_instances) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp cloud sql instances created",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for inst in self.sql_instances:
                try:
                    if inst['settings']['backupConfiguration']['enabled']:
                        pass
                    else:
                        resource_list.append(inst['connectionName'])
                except:
                    resource_list.append(inst['connectionName'])

            if len(resource_list) > 0:
                result = True
                reason = "Gcp cloud sql instance does not have auto backup"
            else:
                result = False
                reason = "ALL gcp cloud sql instances  have auto backup"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check gcp cloud sql instance does not have auto scaling enabled
    def check_4_3_cloud_sql_auto_scaling(self):
        check_id = 4.3
        description = "Check for gcp cloud sql instance does not have auto scaling enabled"
        if len(self.sql_instances) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp cloud sql instances created",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for inst in self.sql_instances:
                try:
                    if inst['settings']['storageAutoResize']:
                        pass
                    else:
                        resource_list.append(inst['connectionName'])
                except:
                    resource_list.append(inst['connectionName'])

            if len(resource_list) > 0:
                result = True
                reason = "gcp cloud sql instance does not have auto scaling enabled"
            else:
                result = False
                reason = "ALL gcp cloud sql instances have auto scaling enabled"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check gcp cloud sql instance does not have high availability in region
    def check_4_4_cloud_sql_high_availability(self):
        check_id = 4.4
        description = "Check for gcp cloud sql instance does not have high availability in region"
        if len(self.sql_instances) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp cloud sql instances created",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for inst in self.sql_instances:
                try:
                    if inst['settings']['availabilityType'] == 'REGIONAL':
                        pass
                    else:
                        resource_list.append(inst['connectionName'])
                except:
                    resource_list.append(inst['connectionName'])

            if len(resource_list) > 0:
                result = True
                reason = "gcp cloud sql instance does not have high availability in region"
            else:
                result = False
                reason = "ALL gcp cloud sql instances have high availability in region"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check gcp cloud sql instance authorized to GEA Applications
    def check_4_5_cloud_sql_gae_application(self):
        check_id = 4.5
        description = "Check for gcp cloud sql instance authorized to GEA Applications"
        if len(self.sql_instances) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp cloud sql instances created",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for inst in self.sql_instances:
                try:
                    if len(inst['settings']['authorizedGaeApplications']) > 0:
                        res = dict()
                        gae_list = []
                        for gae in inst['settings']['authorizedGaeApplications']:
                            gae_list.append(gae)
                        res[inst['name']] = gae_list
                        resource_list.append(res)
                    else:
                        pass
                except:
                    pass

            if len(resource_list) > 0:
                result = True
                reason = "gcp cloud sql instance authorized to GEA Applications"
            else:
                result = False
                reason = "ALL gcp cloud sql instances not authorized to GEA Applications"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check gcp cloud sql instance does not have fail over replica
    def check_4_6_cloud_sql_fail_over_replica(self):
        check_id = 4.6
        description = "Check for gcp cloud sql instance does not have fail over replica"
        if len(self.sql_instances) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp cloud sql instances created",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for inst in self.sql_instances:
                try:
                    if len(inst['failoverReplica']['available']) == False:
                        resource_list.append(inst['connectionName'])
                    else:
                        pass
                except:
                    resource_list.append(inst['connectionName'])

            if len(resource_list) > 0:
                result = True
                reason = "gcp cloud sql instance does not have fail over replica"
            else:
                result = False
                reason = "ALL gcp cloud sql instances have fail over replica"
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
        with open('gcp_cloud_sql.csv', 'w') as outcsv:
            headers = ["check_id", "result", "reason", "resource_list", "description"]
            writer = csv.DictWriter(outcsv, fieldnames=headers)
            writer.writeheader()
            for row in all_check_result:
                writer.writerow(row)
        print("Output write to:gcp_cloud_sql.csv")


class SqlResource:
    """
        this class set different resource information to perform checks on all gcp cloud sql
    """
    def __init__(self, service_account_file, project_id):
        credentials = service_account.Credentials.from_service_account_file(service_account_file)
        # building gcp compute client using gcp compute v1 api
        self.sql_client = discovery.build('sqladmin', 'v1beta4', credentials=credentials)
        self.project = project_id

    # this method returns information of all gcp cloud sql of project
    def all_project_instances(self):
        sql_instances = []
        resp = self.sql_client.instances().list(project=self.project).execute()
        if 'items' in str(resp):
            for inst in resp['items']:
                sql_instances.append(inst)
        return sql_instances


class ExecuteCheckSql:
    """
        This class Execute all check and generates report
    """
    def __init__(self, servive_account_file_path, project_id):
        self.servive_account_file_path = servive_account_file_path
        self.project_id = project_id

    # this method execute checks
    def perform_check(self):
        # getting resources for performing check
        resource_obj = SqlResource(service_account_file=self.servive_account_file_path, project_id=self.project_id)
        sql_instances = resource_obj.all_project_instances()
        sql_client = resource_obj.sql_client
        # initiate Checks class
        check_obj = SqlChecks(sql_client=sql_client, sql_instances=sql_instances)
        all_check_result = [
            check_obj.check_4_1_cloud_sql_public_access(),
            check_obj.check_4_2_cloud_sql_backup_config(),
            check_obj.check_4_3_cloud_sql_auto_scaling(),
            check_obj.check_4_4_cloud_sql_high_availability(),
            check_obj.check_4_5_cloud_sql_gae_application(),
            check_obj.check_4_6_cloud_sql_fail_over_replica(),
        ]
        return all_check_result

