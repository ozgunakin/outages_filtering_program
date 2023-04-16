#!/usr/bin/env python
# coding: utf-8

# LIBRARY IMPORT
import requests
import json
from datetime import datetime
import conf


# Define global variables
outages_url = conf.outages_url
site_info_url = conf.site_info_url
api_headers = conf.headers
date_filter = conf.date_filter
results_url = conf.results_url


# User Defined Functions
def read_outages(outages_url: str, api_headers: dict):
    outages_req = requests.get(outages_url, headers=api_headers)
    if outages_req.status_code == 200:
        outages = outages_req.json()
        return {"message": "Success", "status": 200, "data": outages}

    else:
        response_json = json.loads(outages_req.text)
        return {"message": response_json["message"],
                "status": outages_req.status_code, "data": []}


def read_site_info(site_info_url: str, api_headers: dict):
    site_info_req = requests.get(site_info_url, headers=api_headers)
    if site_info_req.status_code == 200:
        site_info = site_info_req.json()
        return {"message": "Success", "status": 200, "data": site_info}

    else:
        response_json = json.loads(site_info_req.text)
        return {"message": response_json["message"],
                "status": site_info_req.status_code, "data": []}


def filter_and_enhance_outages(outages: dict, site_info: dict,
                               date_filter: str):

    date_filter_dt = datetime.strptime(date_filter, '%Y-%m-%dT%H:%M:%S.%fZ')

    site_outages = []
    for outage in outages:
        ou_id = outage["id"]
        ou_begin = outage["begin"]
        ou_begin_dt = datetime.strptime(ou_begin, '%Y-%m-%dT%H:%M:%S.%fZ')
        device_name = [a["name"] for a in site_info["devices"]
                       if a['id'] == ou_id]

        if ou_begin_dt >= date_filter_dt and len(device_name) > 0:
            outage.update({"name": device_name[0]})
            new_outage = {"id": outage["id"],
                          "name": outage["name"],
                          "begin": outage["begin"],
                          "end": outage["end"]}

            site_outages.append(new_outage)

    enhanced_outages = json.dumps(site_outages)

    return enhanced_outages


def post_outage_results(api_url, api_headers, result_data: dict):
    resp = requests.post(url=api_url, headers=api_headers, data=result_data)

    if resp.status_code == 200:
        return {"message": "Success", "status": resp.status_code}

    else:
        response_json = json.loads(resp.text)
        return {"message": response_json["message"],
                "status": resp.status_code}


def main():
    # Read Outages Data
    outages = read_outages(outages_url, api_headers)
    if outages["status"] != 200:
        return {"message": "Outages API Failure : {}"
                .format(outages["message"]), "status": outages["status"]}

    # Read Site Info Data
    site_info = read_site_info(site_info_url, api_headers)
    if site_info["status"] != 200:
        return {"message": "Site Info API Failure : {}"
                .format(site_info["message"]), "status": site_info["status"]}

    # Filter and Process
    enhanced_outages = filter_and_enhance_outages(outages=outages["data"],
                                                  site_info=site_info["data"],
                                                  date_filter=date_filter)

    # Post Results
    post_response = post_outage_results(api_url=results_url,
                                        api_headers=api_headers,
                                        result_data=enhanced_outages)
    if post_response["status"] != 200:
        return {"message": "Post API Failure : {}"
                .format(post_response["message"]),
                "status": post_response["status"]}

    return post_response


if __name__ == "__main__":
    result = main()
    print(result)
