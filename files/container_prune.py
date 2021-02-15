from datetime import datetime
import os
import docker
import dateparser

STARTING_TIME = str(datetime.now()).split(" ")[0]+ "T" + str(datetime.now()).split(" ")[1] + "Z"

client = docker.from_env()
api_client = docker.APIClient(base_url='unix://var/run/docker.sock')

def compare_time(run_time,container_started_at):
    dt = dateparser.parse(container_started_at).timestamp()
    mt = dateparser.parse(run_time).timestamp()
    interval = mt - dt
    return interval

def eval_interval(interval):
    eval = (interval / 60 ) / 60
    if eval > 2.0:
        return True
    else:
        return False

def check_containers():
    to_delete = []
    for c in client.containers.list():
        start_at = c.attrs['State']['StartedAt']
        interval = compare_time(STARTING_TIME,start_at)
        deleteable = eval_interval(interval)
        print(c.name + " (" + c.id + ") " + str(c.image) + " " + str(deleteable))
        if deleteable == True:
            to_delete.append({"id": c.id, "name": c.name})
        else:
            continue
    return to_delete

def delete_containers(to_delete):
    failed_deletions = []
    for c in to_delete:
        try:
            running_container = str(c['id'])
            print("Deleting: " + running_container)
            print(api_client.stop(container=running_container))
        except:
            failed_deletions.append(c)
            print("Failed to delete: " + c.id)
    return failed_deletions

def main():
    to_delete = check_containers()
    delete_expired = delete_containers(to_delete)
    return delete_expired

if __name__ == "__main__":
    main()