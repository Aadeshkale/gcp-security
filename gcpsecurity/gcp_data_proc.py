"""
This script perform some checks on GCP Data proc
"""
import csv
from googleapiclient import discovery
from google.oauth2 import service_account


class DpChecks:
    """
        this class perform different checks on all gcp data proc
    """
    def __init__(self, data_proc_client, clusters_info, project):

        self.data_proc_client = data_proc_client
        self.clusters_info = clusters_info
        self.project = project

    # --- check methods ---
    # this method check data proc cluster which are not running
    def check_7_1_data_proc_cluster_is_not_running(self):
        check_id = 7.1
        description = "Check for data proc cluster which are not running"
        if len(self.clusters_info) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp data proc cluster is created for this project",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for reg, clust in self.clusters_info.items():
                for m in clust:
                    if 'RUNNING' not in str(m['status']):
                        data = dict()
                        data[reg] = m['clusterName']
                        resource_list.append(data)

            if len(resource_list) > 0:
                result = True
                reason = "Gcp data proc cluster which are not running"
            else:
                result = False
                reason = "All Gcp project data proc cluster are running"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check data proc cluster does not have any worker node
    def check_7_2_data_proc_cluster_without_worker_node(self):
        check_id = 7.2
        description = "Check for data proc cluster does not have any worker node"
        if len(self.clusters_info) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp data proc cluster is created for this project",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for reg, clust in self.clusters_info.items():
                for m in clust:
                    try:
                        work_config = m['config']['workerConfig']
                        if work_config:
                            if work_config['numInstances'] <= 0:
                                data = dict()
                                data[reg] = m['clusterName']
                                resource_list.append(data)
                    except:
                        data = dict()
                        data[reg] = m['clusterName']
                        resource_list.append(data)

            if len(resource_list) > 0:
                result = True
                reason = "Gcp data proc cluster does not have any worker node"
            else:
                result = False
                reason = "All Gcp project data proc clusters have worker nodes"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check data proc cluster does not have preemptible worker node
    def check_7_3_data_proc_cluster_without_preemptible_worker_node(self):
        check_id = 7.3
        description = "Check for data proc cluster does not have preemptible worker node"
        if len(self.clusters_info) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp data proc cluster is created for this project",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for reg, clust in self.clusters_info.items():
                for m in clust:
                    try:
                        work_config = m['config']['workerConfig']
                        if work_config:
                            if work_config['preemptibility'] == "NON_PREEMPTIBLE":
                                data = dict()
                                data[reg] = m['clusterName']
                                resource_list.append(data)
                    except:
                        data = dict()
                        data[reg] = m['clusterName']
                        resource_list.append(data)

            if len(resource_list) > 0:
                result = True
                reason = "Gcp data proc cluster does not have preemptible worker node"
            else:
                result = False
                reason = "All Gcp project data proc clusters have preemptible worker nodes"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check data proc cluster have secondary worker node
    def check_7_4_data_proc_cluster_with_secondary_worker_node(self):
        check_id = 7.4
        description = "Check for data proc cluster have secondary worker node"
        if len(self.clusters_info) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp data proc cluster is created for this project",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for reg, clust in self.clusters_info.items():
                for m in clust:
                    try:
                        secondary_worker_config = m['config']['secondaryWorkerConfig']
                        if secondary_worker_config:
                            if secondary_worker_config['numInstances'] > 0:
                                data = dict()
                                data[reg] = m['clusterName']
                                resource_list.append(data)
                    except:
                        data = dict()
                        data[reg] = m['clusterName']
                        resource_list.append(data)

            if len(resource_list) > 0:
                result = True
                reason = "Gcp data proc cluster have secondary worker node"
            else:
                result = False
                reason = "All Gcp project data proc clusters does not have secondary worker node"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check data proc cluster has allow api access to all gcp services in the same project
    def check_7_5_data_proc_cluster_with_all_service_access(self):
        check_id = 7.5
        description = "Check for data proc cluster has allow api access to all gcp services in the same project"
        if len(self.clusters_info) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp data proc cluster is created for this project",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for reg, clust in self.clusters_info.items():
                for m in clust:
                    try:
                        config = m['config']['gceClusterConfig']
                        if config:
                            scope = "cloud-platform"
                            if scope in str(config['serviceAccountScopes']):
                                data = dict()
                                data[reg] = m['clusterName']
                                resource_list.append(data)
                    except:
                        data = dict()
                        data[reg] = m['clusterName']
                        resource_list.append(data)

            if len(resource_list) > 0:
                result = True
                reason = "Gcp data proc cluster has allow api access to all gcp services in the same project"
            else:
                result = False
                reason = "All Gcp project data proc clusters does not allow api access to all gcp services"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check data proc cluster does not have any job
    def check_7_6_data_proc_cluster_without_any_job(self):
        check_id = 7.6
        description = "Check for data proc cluster cluster does not have any job"
        if len(self.clusters_info) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp data proc cluster is created for this project",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for reg, clust in self.clusters_info.items():
                for m in clust:
                    try:
                        region = reg
                        name = m['clusterName']
                        res = self.check_for_cluster_has_job(clust_region=region, clust_name=name)
                        if res == True:
                            data = dict()
                            data[reg] = m['clusterName']
                            resource_list.append(data)
                    except:
                        pass

            if len(resource_list) > 0:
                result = True
                reason = "Gcp data proc cluster does not have any job"
            else:
                result = False
                reason = "All Gcp project data proc clusters have job allocated"
            return self.result_template(check_id, result, reason, resource_list, description)

    # --- supporting methods ---
    # this method is check for data proc cluster has a job
    def check_for_cluster_has_job(self, clust_region, clust_name):
        resp = self.data_proc_client.projects().regions().jobs().list(
            projectId=self.project,
            region=clust_region,
            clusterName=clust_name
        ).execute()
        if len(resp) == 0:
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
        with open('gcp_data_proc.csv', 'w') as outcsv:
            headers = ["check_id", "result", "reason", "resource_list", "description"]
            writer = csv.DictWriter(outcsv, fieldnames=headers)
            writer.writeheader()
            for row in all_check_result:
                writer.writerow(row)
        print("Output write to:gcp_data_proc.csv")


class DpResource:
    """
        this class set different resource information to perform checks on all gcp data proc
    """
    def __init__(self, service_account_file, project_id):
        self.credentials = service_account.Credentials.from_service_account_file(service_account_file)
        # building gcp compute client using gcp data proc v1 api
        self.data_proc_client = discovery.build('dataproc', 'v1', credentials=self.credentials)
        self.project = project_id

    # this method returns list of all regions of gcp
    def get_regions(self):
        compute_client = discovery.build('compute', 'v1', credentials=self.credentials)
        regions = compute_client.regions().list(project=self.project).execute()
        regions_list = []
        for i in regions['items']:
            regions_list.append(i['name'])
        return regions_list

    # this method return all list of clusters in project in all regions
    def get_clusters(self):
        clusters_info = {}
        for rg in self.get_regions():
            resp = self.data_proc_client.projects().regions().clusters().list(projectId=self.project,
                                                                              region=rg).execute()
            if 'clusters' in str(resp):
                clusters_info[rg] = resp['clusters']
        return clusters_info


class ExecuteCheckDp:
    """
        This class Execute all check and generates report
    """
    def __init__(self, servive_account_file_path, project_id):
        self.servive_account_file_path = servive_account_file_path
        self.project_id = project_id

    # this method execute checks
    def perform_check(self):
        # getting resources for performing check
        resource_obj = DpResource(service_account_file=self.servive_account_file_path, project_id=self.project_id)
        clusters_info = resource_obj.get_clusters()
        data_proc_client = resource_obj.data_proc_client
        project = resource_obj.project
        # initiate Checks class
        check_obj = DpChecks(data_proc_client=data_proc_client, clusters_info=clusters_info, project=project)
        all_check_result = [
            check_obj.check_7_1_data_proc_cluster_is_not_running(),
            check_obj.check_7_2_data_proc_cluster_without_worker_node(),
            check_obj.check_7_3_data_proc_cluster_without_preemptible_worker_node(),
            check_obj.check_7_4_data_proc_cluster_with_secondary_worker_node(),
            check_obj.check_7_5_data_proc_cluster_with_all_service_access(),
            check_obj.check_7_6_data_proc_cluster_without_any_job(),
        ]
        return all_check_result
