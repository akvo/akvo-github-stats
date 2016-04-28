# Akvo GitHub stats

Fetches issues data of select Akvo repositories from the github api. Currently fetches from the following repos:

* https://github.com/akvo/akvo-dash/
* https://github.com/akvo/akvo-flow/
* https://github.com/akvo/akvo-flow-mobile/
* https://github.com/akvo/akvo-provisioning/
* https://github.com/akvo/akvo-rsr/
* https://github.com/akvo/akvo-rsr-up/
* https://github.com/akvo/akvo-sites/
* https://github.com/akvo/akvo-web/

The data is converted to CVS files and stored in the csv directory using the repo name as file name. The raw json is also saved, in the json dir.

### Setup and usage

Clone the repository: ```git clone git@github.com:akvo/akvo-github-stats.git```

Cd into the script dierctory: ```cd akvo-github-stats/gh_stats```

Run the script: ```python gh_stats.py```

Wait for a while.

Grab the files you need!

### Private repos

Private repos are supported, but currently no private repos are included. If needed, a github username and token can be put in a file, **github.txt**, the username on the first line and the token on the second line of the file.