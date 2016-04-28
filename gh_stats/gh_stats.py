# -*- coding: utf-8 -*-

# Akvo Reporting is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.

import json
import os

import requests
import sys
import tablib

from collections import namedtuple

DEBUG = True

AKVO_GH_BASE_URL = "https://api.github.com/repos/akvo/"

DASH_REPO = "akvo-dash/"
FLOW_REPO = "akvo-flow/"
FLOW_MOBILE_REPO = "akvo-flow-mobile/"
PROVISION_REPO = "akvo-provisioning/"
RSR_REPO = "akvo-rsr/"
RSR_UP_REPO = "akvo-rsr-up/"
SITES_REPO = "akvo-sites/"
WEB_REPO = "akvo-web/"

ISSUE_STATE = "all"
ENDPOINT = "issues"

json_field = namedtuple("json_field", "title path")


class GitHubAPI():
    def __init__(self, repo):
        self.repo = repo
        self.akvo_gh_base_url = AKVO_GH_BASE_URL
        self.endpoint = ENDPOINT
        self.query_vars = {"state": ISSUE_STATE}
        self.issues = []
        self.user, self.token = self.get_gh_credentials()

    def get_gh_credentials(self):
        try:
            with open('github.txt', 'r') as f:
                gh_text = f.read()
                return gh_text.split('\n')[0], gh_text.split('\n')[1]
        except IOError:
            return None, None

    def query(self, extra=None):
        if extra is not None:
            extra.update(self.query_vars)
        else:
            extra = self.query_vars
        return "&".join(["{}={}".format(k, v) for k, v in extra.items()])

    def call(self, page_no):
        url = "".join([
            self.akvo_gh_base_url,
            self.repo,
            self.endpoint,
            "?",
            self.query({"page": page_no})
        ])
        if self.user:
            return requests.get(url, auth=(self.user, self.token))
        else:
            return requests.get(url)

    def fetch_all_issues(self):
        page_no = 1
        while True:
            if DEBUG:
                print("Getting page {}".format(page_no))
            request = self.call(page_no)
            if request.status_code != 200:
                raise "Error getting data from da Hub :("
            json_data = request.json()
            if json_data != []:
                self.issues += json_data
                page_no += 1
            else:
                break

class Issues():
    def __init__(self, repo):
        self.repo = repo
        self.data = tablib.Dataset()
        self.fields = (
            json_field("Title", "title"),
            json_field("Created at", "created_at"),
            json_field("Closed at", "closed_at"),
            json_field("Labels", "labels[].name"),
            json_field("Issue number", "number"),
            json_field("State", "state"),
            json_field("Milestone", "milestone.title"),
        )
        self.da_hub = GitHubAPI(repo)

    def fetch_from_da_hub(self):
        self.da_hub.fetch_all_issues()

    def json_to_tabular(self):
        self.data.headers = [col.title for col in self.fields]
        for issue in self.da_hub.issues:
            row = []
            for field in self.fields:
                if field.path.find("[].") > 0:
                    row += [
                        ",".join(
                            [bit[field.path.split("[].")[1]] for bit in
                             issue[field.path.split("[].")[0]]]
                        )
                    ]
                elif field.path.find(".") > 0:
                    bit1 = field.path.split(".")[0]
                    bit2 = field.path.split(".")[1]
                    row += [issue.get(bit1).get(bit2) if issue.get(bit1) else ""]
                else:
                    row += [issue.get(field.path)]
            self.data.append(row)

    def save_to_csv(self):
        file_name = "{}.csv".format(self.repo[:-1])
        if not os.path.exists('csv'):
            os.makedirs('csv')
        with open("csv/{}".format(file_name), 'wb') as f:
            f.write(self.data.csv)

    def save_raw_json(self):
        file_name = "{}.json".format(self.repo[:-1])
        if not os.path.exists('json'):
            os.makedirs('json')
        with open("json/{}".format(file_name), 'wb') as f:
            f.write(json.dumps(self.da_hub.issues))


def run():
    for repo in [RSR_REPO, FLOW_REPO]:#, WEB_REPO, FLOW_MOBILE_REPO, RSR_UP_REPO, SITES_REPO, PROVISION_REPO]:
        if DEBUG:
            print("Getting issues from {}".format(repo[:-1]))
        issues = Issues(repo)
        issues.fetch_from_da_hub()
        issues.save_raw_json()
        issues.json_to_tabular()
        issues.save_to_csv()

if __name__ == "__main__":
    run()


