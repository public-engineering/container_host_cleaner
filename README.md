# Container Host Cleaner

Ansible role to configure a cron job that terminates containers older than `LIMIT_HOURS` number of hours.

This is used with `public-engineering/vpn.public.engineering` to clean up terminated VPN instances.

## Requirements

Must have `pip3` and Docker installed on your target system-- this package will only install the Docker Python SDK.

## Using

In `examples/main.yml` there is an example usage:

```yaml
---
- hosts:
    - docker_hosts
  roles:
         - { role: container_host_cleaner, docker_remote_user: "ubuntu" }
```

This only requires `docker_remote_user` (ideally this would be the same as your Ansible user).

This role configures the `container_prune.py` script, and configures a cronjob to run at an hourly interval, with `LIMIT_HOURS` defaulting to `2.0` unless another value is provided.

This role is intended to run against the local Docker daemon, and should be installed on all nodes running Docker where you anticipate a need for this behavior, and as shown above, can be included alongside other roles (i.e. one that configures Docker, or other configuration required on those nodes).

