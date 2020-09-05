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


# this class perform different checks on all gcp compute engines
class Checks:
    def __init__(self, all_info):
        self.all_info = all_info




class Resource:

    def __init__(self,compute_client,project):
        self.compute_client = compute_client
        self.project = project

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
        return all_info


res = Resource(compute_client=COMPUTE_CLIENT,project=PROJECT_ID)
print(res.all_instances())

