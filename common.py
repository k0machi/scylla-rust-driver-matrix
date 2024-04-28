import logging
import re
import subprocess
from collections import defaultdict
from pathlib import Path

# CCM_CLUSTER_IP_PREFIX = "127.0.1"
# CCM_CLUSTER_NODES = 3


def run_command_in_shell(driver_repo_path: str, cmd: str, environment: dict = None):
    logging.debug("Execute the cmd '%s'", cmd)
    with subprocess.Popen(cmd, shell=True, executable="/bin/bash", env=environment,
                          cwd=Path(driver_repo_path), stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        stderr = proc.communicate()
        status_code = proc.returncode
    assert status_code == 0, stderr


def scylla_uri_per_node(nodes_ips):
    uri_per_node = []
    for node, ip in nodes_ips.items():
        node_index = node.replace("node", "").replace("1", "")
        uri_per_node.append(f"SCYLLA_URI{node_index}={ip}:9042")
        # uri_per_node = "SCYLLA_URI=127.0.1.1:9042 " + " ".join([f"SCYLLA_URI{i+1}=127.0.1.{i+1}:9042" for i in range(1, nodes)])
    return " ".join(uri_per_node)
