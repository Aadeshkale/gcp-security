"""
This script perform some checks on GCP compute engine VM's
"""
import argparse
import sys
import csv
from googleapiclient import discovery
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file('credentials/my_credentials.json')
COMPUTE_CLIENT = discovery.build('compute', 'v1', credentials=credentials)
PROJECT_ID = "info1-284008"


class Resource:

    def __init__(self,compute_client,project):
        self.compute_client = compute_client
        self.project = project

    def get_zones(self):
        zones = self.compute_client.zones().list(project=self.project).execute()
        zones_list = []
        for i in zones['items']:
            zones_list.append(i['name'])
        return zones_list

    # def list_instances(self, compute, project, zone):
    #     result = compute.instances().list(project=project, zone=zone).execute()
    #     return result['items'] if 'items' in result else None


res = Resource(compute_client=COMPUTE_CLIENT,project=PROJECT_ID)
print(res.get_zones())

