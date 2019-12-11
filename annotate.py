import os
import requests
import urllib3
import csv

# Silence warning
urllib3.disable_warnings(urllib3.exceptions.SubjectAltNameWarning)

LAB = 'ACME'
DISEASE_CODE = 'ALS'
token = os.environ['VARDA_TOKEN']

s = requests.Session()
s.headers = {"Authorization": "Bearer %s" % token}
s.verify = 'nginx-selfsigned.crt'

# Get sample id's from file
sample_ids = []
with open('sample_sheet.txt', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ')
    for row in reader:
        sample_ids.append(row[0])

# Assuming the files are already in the uploads directory remotely, create and submit samples
tasks = []
for sample_id in sample_ids[0:]:
    var_file = '%s_variants.varda' % sample_id
    print('%s %s' % (sample_id, var_file))

    resp = s.post('https://res-vard-db01.researchlumc.nl/annotation', json={
        'variant_filename': var_file
    })
    print(resp.json())
    task_uuid = resp.json()['task']

    # Record tasks
    tasks.append(task_uuid)


# Write task uuid's to file
fp = open("tasks.txt", "w")
for task in tasks:
    fp.write("%s\n" % task)
fp.close()
