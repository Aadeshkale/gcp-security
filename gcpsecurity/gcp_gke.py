"""
This script perform some checks on GCP kubernetes engine
"""
import csv
from googleapiclient import discovery
from google.oauth2 import service_account


class GkeChecks:
    """
        this class perform different checks on all gcp kubernetes engine
    """
    def __init__(self, gke_client, clusters, project):
        self.gke_client = gke_client
        self.clusters = clusters
        self.project = project

    # --- check methods ---
    # this method check gke cluster is zonal
    def check_8_1_gke_cluster_is_zonal(self):
        check_id = 8.1
        description = "Check for gke cluster is zonal"
        if len(self.clusters) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp gke cluster is created for this project",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for loc, clust in self.clusters.items():
                for m in clust:
                    if len(m['locations']) == 1:
                        resource_list.append(m['name'])

            if len(resource_list) > 0:
                result = True
                reason = "Gke cluster is zonal"
            else:
                result = False
                reason = "All gke cluster are regional"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check gke cluster is created in default network
    def check_8_2_gke_cluster_is_created_in_default_network(self):
        check_id = 8.2
        description = "Check for gke cluster is created in default network"
        if len(self.clusters) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp gke cluster is created for this project",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for loc, clust in self.clusters.items():
                for m in clust:
                    if 'default' in str(m['networkConfig']):
                        resource_list.append(m['name'])

            if len(resource_list) > 0:
                result = True
                reason = "Gke cluster is created in default network"
            else:
                result = False
                reason = "All gke clusters are not in default network"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check gke cluster has all api access to this project
    def check_8_3_gke_cluster_has_all_api_access(self):
        check_id = 8.3
        description = "Check for gke cluster has all api access to this project"
        if len(self.clusters) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp gke cluster is created for this project",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for loc, clust in self.clusters.items():
                for m in clust:
                    try:
                        if 'cloud-platform' in str(m['nodeConfig']['oauthScopes']):
                            resource_list.append(m['name'])
                    except:
                        pass

            if len(resource_list) > 0:
                result = True
                reason = "Gke cluster has all api access to this project"
            else:
                result = False
                reason = "All gke clusters does not have all api access to this project"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check gke cluster has node pools auto scaling
    def check_8_4_gke_cluster_has_node_pool_autoscaling(self):
        check_id = 8.4
        description = "Check for gke cluster has node pools auto scaling"
        if len(self.clusters) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp gke cluster is created for this project",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for loc, clust in self.clusters.items():
                for m in clust:
                    try:
                        if m['nodePools']['autoscaling']['enabled'] == True:
                            resource_list.append(m['name'])
                    except:
                        pass

            if len(resource_list) > 0:
                result = True
                reason = "Gke cluster has node pools auto scaling"
            else:
                result = False
                reason = "All gke clusters does not have node pools auto scaling"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check gke cluster has                  vertical pod autoscaling
    def check_8_5_gke_cluster_has_vertical_pod_autoscaling(self):
        check_id = 8.5
        description = "Check for gke cluster has vertical pod autoscaling"
        if len(self.clusters) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp gke cluster is created for this project",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for loc, clust in self.clusters.items():
                for m in clust:
                    try:
                        if m['verticalPodAutoscaling']['enabled'] == True:
                            resource_list.append(m['name'])
                    except:
                        pass

            if len(resource_list) > 0:
                result = True
                reason = "Gke cluster has vertical pod autoscaling"
            else:
                result = False
                reason = "All gke clusters does not have vertical pod autoscaling"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check gke cluster nodes is encrypted using gcp kms key
    def check_8_6_gke_cluster_nodes_encrypted_kms_key(self):
        check_id = 8.6
        description = "Check for gke cluster nodes is encrypted using gcp kms key"
        if len(self.clusters) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp gke cluster is created for this project",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for loc, clust in self.clusters.items():
                for m in clust:
                    try:
                        if m['nodeConfig']['bootDiskKmsKey']:
                            resource_list.append(m['name'])
                    except:
                        pass

            if len(resource_list) > 0:
                result = True
                reason = "Gke cluster nodes is encrypted using gcp kms key"
            else:
                result = False
                reason = "All gke cluster nodes is encrypted using gcp kms key"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check gke cluster is regional
    def check_8_7_gke_cluster_is_regional(self):
        check_id = 8.7
        description = "Check for gke cluster is regional"
        if len(self.clusters) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp gke cluster is created for this project",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for loc, clust in self.clusters.items():
                for m in clust:
                    if len(m['locations']) > 1:
                        resource_list.append(m['name'])

            if len(resource_list) > 0:
                result = True
                reason = "Gke cluster is regional"
            else:
                result = False
                reason = "All gke cluster are zonal"
            return self.result_template(check_id, result, reason, resource_list, description)

    # this method check gke cluster is not running
    def check_8_8_gke_cluster_is_not_running(self):
        check_id = 8.8
        description = "Check for gke cluster is not running"
        if len(self.clusters) <= 0:
            res = self.result_template(
                check_id=check_id,
                result=False,
                reason="There is no gcp gke cluster is created for this project",
                resource_list=[],
                description=description
            )
            return res
        else:
            resource_list = []
            for loc, clust in self.clusters.items():
                for m in clust:
                    if m['status'] != 'RUNNING':
                        resource_list.append(m['name'])

            if len(resource_list) > 0:
                result = True
                reason = "Gke cluster is not running"
            else:
                result = False
                reason = "All gke cluster are running"
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
        with open('gcp_gke.csv', 'w') as outcsv:
            headers = ["check_id", "result", "reason", "resource_list", "description"]
            writer = csv.DictWriter(outcsv, fieldnames=headers)
            writer.writeheader()
            for row in all_check_result:
                writer.writerow(row)
        print("Output write to:gcp_gke.csv")


class GkeResource:
    """
        this class set different resource information to perform checks on all gcp kubernetes engine
    """
    def __init__(self, service_account_file, project_id):
        self.credentials = service_account.Credentials.from_service_account_file(service_account_file)
        # building gcp Gke client using gcp Gke v1 api
        self.gke_client = discovery.build('container', 'v1', credentials=self.credentials)
        self.project = project_id

    # this method returns list of all zones of gcp
    def get_zones(self):
        compute_client = discovery.build('compute', 'v1', credentials=self.credentials)
        zones = compute_client.zones().list(project=self.project).execute()
        zones_list = []
        for i in zones['items']:
            zones_list.append(i['name'])
        return zones_list

    # this method returns list of all zones of gcp
    def get_regions(self):
        compute_client = discovery.build('compute', 'v1', credentials=self.credentials)
        regions = compute_client.regions().list(project=self.project).execute()
        regions_list = []
        for i in regions['items']:
            regions_list.append(i['name'])
        return regions_list

    # get all kubernetes clusters across all project
    def get_clusters(self):
        clusters = {}
        # list of gcp regions + zones
        region_zone = self.get_zones() + self.get_regions()
        for loc in region_zone:
            parent = "projects/{}/locations/{}".format(self.project, loc)
            resp = self.gke_client.projects().locations().clusters().list(parent=parent).execute()
            if 'clusters' in str(resp):
               clusters[loc] = resp['clusters']
        return clusters


class ExecuteCheckGke:
    """
        This class Execute all check and generates report
    """
    def __init__(self, servive_account_file_path, project_id):
        self.servive_account_file_path = servive_account_file_path
        self.project_id = project_id

    # this method execute checks
    def perform_check(self):
        # getting resources for performing check
        resource_obj = GkeResource(service_account_file=self.servive_account_file_path, project_id=self.project_id)
        clusters = resource_obj.get_clusters()
        gke_client = resource_obj.gke_client
        project = resource_obj.project
        # initiate Checks class
        check_obj = GkeChecks(gke_client=gke_client, clusters=clusters, project=project)
        all_check_result = [
            check_obj.check_8_1_gke_cluster_is_zonal(),
            check_obj.check_8_2_gke_cluster_is_created_in_default_network(),
            check_obj.check_8_3_gke_cluster_has_all_api_access(),
            check_obj.check_8_4_gke_cluster_has_node_pool_autoscaling(),
            check_obj.check_8_5_gke_cluster_has_vertical_pod_autoscaling(),
            check_obj.check_8_6_gke_cluster_nodes_encrypted_kms_key(),
            check_obj.check_8_7_gke_cluster_is_regional(),
            check_obj.check_8_8_gke_cluster_is_not_running(),

        ]
        return all_check_result
