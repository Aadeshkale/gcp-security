"""
    This is demo main file for handling all checking operations which improves,
    your GCP gcpsecurity, this script is working on project level.
    This script might take time to execute because of hugh API calls.
"""
import csv
from gcpsecurity.gcp_vm import ExecuteCheckVm
from gcpsecurity.gcp_iam import ExecuteCheckIam
from gcpsecurity.gcp_vpc import ExecuteCheckVpc
from gcpsecurity.gcp_gcs import ExecuteCheckGcs
from gcpsecurity.gcp_cloud_sql import ExecuteCheckSql
from gcpsecurity.gcp_app_engine import ExecuteCheckGae
from gcpsecurity.gcp_data_proc import ExecuteCheckDp
from gcpsecurity.gcp_gke import ExecuteCheckGke

# Credentials path
SERVICE_ACCOUNT_FILE_PATH = 'credentials/my_credentials.json'
PROJECT_ID = "tech-289406"

# creating objects of class to perform check operations as per service

vm = ExecuteCheckVm(servive_account_file_path=SERVICE_ACCOUNT_FILE_PATH, project_id=PROJECT_ID)
vm_result = vm.perform_check()
vpc = ExecuteCheckVpc(servive_account_file_path=SERVICE_ACCOUNT_FILE_PATH, project_id=PROJECT_ID)
vpc_result = vpc.perform_check()
iam = ExecuteCheckIam(servive_account_file_path=SERVICE_ACCOUNT_FILE_PATH, project_id=PROJECT_ID)
iam_result = iam.perform_check()
gcs = ExecuteCheckGcs(servive_account_file_path=SERVICE_ACCOUNT_FILE_PATH, project_id=PROJECT_ID)
gcs_result = gcs.perform_check()
sql = ExecuteCheckSql(servive_account_file_path=SERVICE_ACCOUNT_FILE_PATH, project_id=PROJECT_ID)
sql_result = sql.perform_check()
gae = ExecuteCheckGae(servive_account_file_path=SERVICE_ACCOUNT_FILE_PATH, project_id=PROJECT_ID)
gae_result = gae.perform_check()
dp = ExecuteCheckDp(servive_account_file_path=SERVICE_ACCOUNT_FILE_PATH, project_id=PROJECT_ID)
dp_result = dp.perform_check()
gke = ExecuteCheckGke(servive_account_file_path=SERVICE_ACCOUNT_FILE_PATH, project_id=PROJECT_ID)
gke_result = gke.perform_check()

# combine all results of each service
result = vm_result + vpc_result + iam_result + sql_result\
         + gcs_result + gae_result + dp_result + gke_result

# generating csv file from result
def generate_csv(result):
    with open('gcp_security.csv', 'w') as outcsv:
        headers = ["check_id", "result", "reason", "resource_list", "description"]
        writer = csv.DictWriter(outcsv, fieldnames=headers)
        writer.writeheader()
        for row in result:
            writer.writerow(row)
    print("Output write to:gcp_security.csv")


generate_csv(result)
