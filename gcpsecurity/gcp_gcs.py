"""
This script perform some checks on GCP compute engine VM's
"""
import csv
from googleapiclient import discovery
from google.oauth2 import service_account


class GcsChecks:
    """
        this class perform different checks on all google cloud storage
    """
    def __init__(self, storage_client, buckets_info):
        self.storage_client = storage_client
        self.buckets_info = buckets_info

    # --- check methods ---
    # this method check gcp gcs bucket is not multi-regional
    def check_5_1_multi_regional_bucket(self):
        check_id = 5.1
        description = "Check for gcp gcs bucket is not multi-regional"
        if len(self.buckets_info) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp gcs bucket is created",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for buk in self.buckets_info:
                try:
                    if buk['locationType'] != 'multi-region':
                        resource_list.append(buk['id'])
                except:
                    pass

            if len(resource_list) > 0:
                result = True
                reason = "Gcp gcs bucket is not multi-regional"
            else:
                result = False
                reason = "All gcp gcs buckets are multi-regional"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check gcp gcs bucket has retention policy
    def check_5_2_bucket_has_retention_policy(self):
        check_id = 5.2
        description = "Check for gcp gcs bucket has retention policy"
        if len(self.buckets_info) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp gcs bucket is created",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for buk in self.buckets_info:
                try:
                    if buk['retentionPolicy']:
                        resource_list.append(buk['id'])
                except:
                    pass
            if len(resource_list) > 0:
                result = True
                reason = "Gcp gcs bucket has retention policy"
            else:
                result = False
                reason = "All gcp gcs buckets does not have any retention policy"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check gcp gcs bucket has uniform bucket level access
    def check_5_3_bucket_uniform_bucket_level_access(self):
        check_id = 5.3
        description = "Check for gcp gcs gcp gcs bucket has uniform bucket level access"
        if len(self.buckets_info) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp gcs bucket is created",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for buk in self.buckets_info:
                try:
                    if buk['uniformBucketLevelAccess']['enabled'] == True:
                        resource_list.append(buk['id'])
                except:
                    pass
            if len(resource_list) > 0:
                result = True
                reason = "Gcp gcs bucket has uniform bucket level access"
            else:
                result = False
                reason = "All gcp gcs buckets does not have uniform bucket level access"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check gcp gcs bucket has public access
    def check_5_4_bucket_bucket_has_public_access(self):
        check_id = 5.4
        description = "Check for gcp gcs bucket has public access"
        if len(self.buckets_info) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp gcs bucket is created",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for buk in self.buckets_info:
                try:
                    name = buk['id']
                    res = self.check_bucket_is_public(name)
                    if res == True:
                        resource_list.append(buk['id'])
                except:
                    pass
            if len(resource_list) > 0:
                result = True
                reason = "Gcp gcs bucket has public access"
            else:
                result = False
                reason = "All gcp gcs buckets does not have public access"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check gcp gcs bucket is empty
    def check_5_5_bucket_bucket_is_empty(self):
        check_id = 5.5
        description = "Check for gcp gcs bucket is empty"
        if len(self.buckets_info) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp gcs bucket is created",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for buk in self.buckets_info:
                try:
                    name = buk['id']
                    res = self.check_bucket_items(name)
                    if res == False:
                        resource_list.append(buk['id'])
                except:
                    pass
            if len(resource_list) > 0:
                result = True
                reason = "Gcp gcs bucket is empty"
            else:
                result = False
                reason = "All gcp gcs buckets are not empty"
            return self.result_template(check_id, result, reason, resource_list, description)

        # this method check gcp gcs bucket has retention policy

    def check_5_6_bucket_has_lifecycle(self):
        check_id = 5.6
        description = "Check for gcp gcs bucket has lifecycle"
        if len(self.buckets_info) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp gcs bucket is created",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for buk in self.buckets_info:
                try:
                    if buk['lifecycle']:
                        resource_list.append(buk['id'])
                except:
                    pass
            if len(resource_list) > 0:
                result = True
                reason = "Gcp gcs bucket has lifecycle"
            else:
                result = False
                reason = "All gcp gcs buckets does not have any lifecycle"
            return self.result_template(check_id, result, reason, resource_list, description)

    # --- supporting methods ---
    # this method check gcs bucket is public
    def check_bucket_is_public(self,name):
        resp = self.storage_client.buckets().getIamPolicy(bucket=name).execute()
        try:
            if 'allUsers' in str(resp):
                for per in resp['bindings']:
                    if per['role'] == 'roles/storage.legacyBucketReader' and 'allUsers' in str(per):
                        return True
        except:
            return False

    # this method check gcs bucket is empty
    def check_bucket_items(self,name):
        resp = self.storage_client.objects().list(bucket=name).execute()
        if 'items' in resp:
            if len(resp['items']) > 0:
                return True
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
        with open('gcp_gcs.csv', 'w') as outcsv:
            headers = ["check_id", "result", "reason", "resource_list", "description"]
            writer = csv.DictWriter(outcsv, fieldnames=headers)
            writer.writeheader()
            for row in all_check_result:
                writer.writerow(row)
        print("Output write to:gcp_gcs.csv")


class GcsResource:
    """
        this class set different resource information to perform checks on all google cloud storage
    """
    def __init__(self, service_account_file, project_id):
        credentials = service_account.Credentials.from_service_account_file(service_account_file)
        # building gcp client using gcp storage v1 api
        self.storage_client = discovery.build('storage', 'v1', credentials=credentials)
        self.project = project_id


    # this method returns information of all gcp storage bucket information
    def all_buckets_info(self):
        buckets_info = []
        req = self.storage_client.buckets().list(project=self.project)
        resp = req.execute()
        if 'items' in str(resp):
            for buk in resp['items']:
                buckets_info.append(buk)
        return buckets_info


class ExecuteCheckGcs:
    """
        This class Execute all check and generates report
    """
    def __init__(self, servive_account_file_path, project_id):
        self.servive_account_file_path = servive_account_file_path
        self.project_id = project_id

    # this method execute checks
    def perform_check(self):
        # getting resources for performing check
        resource_obj = GcsResource(service_account_file=self.servive_account_file_path, project_id=self.project_id)
        buckets_info = resource_obj.all_buckets_info()
        storage_client = resource_obj.storage_client

        # initiate Checks class
        check_obj = GcsChecks(storage_client=storage_client, buckets_info=buckets_info)
        all_check_result = [
            check_obj.check_5_1_multi_regional_bucket(),
            check_obj.check_5_2_bucket_has_retention_policy(),
            check_obj.check_5_3_bucket_uniform_bucket_level_access(),
            check_obj.check_5_4_bucket_bucket_has_public_access(),
            check_obj.check_5_5_bucket_bucket_is_empty(),
            check_obj.check_5_6_bucket_has_lifecycle(),
        ]
        return all_check_result


