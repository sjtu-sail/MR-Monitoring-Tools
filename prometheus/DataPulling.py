import requests
import os
import numpy as np
import json

# base_url = "http://202.120.40.4:19090/api/v1/query_range"
base_url = "http://192.168.22.18:9090/api/v1/query_range"
node_list = ["192.168.22.11", "192.168.22.12"]
default_port = "9100"
type_dict = {"cpu": "100 - (avg(irate(node_cpu_seconds_total{}[5m])) *100)",
             "net": "sum(irate(node_network_receive_bytes_total{}[5m])*8)",
             "disk_read": "sum(irate(node_disk_read_bytes_total{}[5m]))",
             "disk_write": "sum(irate(node_disk_written_bytes_total{}[5m]))"}
result_json = {
    "title": "",
    "interval": [],
    "data": [
        # {
        #     "name":"",
        #     "value":[]
        # }
    ]
}
FilePath = "./mytask"


def send_request(url, params):
    r = requests.get(url, params)
    return r.json()


def prom_query(type, id):
    node = id + ":" + default_port
    q_node = "{instance='" + node + "'}"
    if type == 'cpu':
        q_node = "{instance='" + node + "',mode='idle'}"
    if type == 'net':
        q_node = "{instance=~'" + node + "',device!~'tap.*'}"
    result = type_dict[type].format(q_node)
    return result


def data_transfer(type, start_time, end_time, step):
    for ip in node_list:
        query = prom_query(type, ip)
        params = {'query': query, 'start': start_time, 'end': end_time, 'step': step}
        result = send_request(base_url, params)

        if result['status'] == 'success':
            new_item = {
                "name": ip,
                "value": []
            }
            data = result['data']['result']
            if data:
                vectors = np.array(data[0]['values'])
                vectors = np.split(vectors, 2, axis=1)
                new_item["value"] = vectors[1].ravel().astype(np.float32).tolist()
                result_json["interval"] = vectors[0].ravel().astype(np.int64).tolist()
                result_json["data"].append(new_item)
    if not os.path.exists(FilePath):
        os.makedirs(FilePath)
    filename = os.path.join(FilePath, "./{}.json".format(result_json["title"]))

    with open(filename, "w") as f:
        json.dump(result_json, f)
    result_json["data"] = result_json["interval"] = []


def pulling(test_id, start_time=1552226880, end_time=1552227210, step=15):
    for type in type_dict:
        result_json["title"] = "_".join([str(test_id), type])
        data_transfer(type, start_time, end_time, step)


if __name__ == '__main__':
    pulling("11365")
