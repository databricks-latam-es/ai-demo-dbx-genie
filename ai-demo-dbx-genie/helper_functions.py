###
# Helper functions
# 
# Author: @alberto.murguia
# Revision: 1.0
# 
# This script implements an experimental chatbot that interacts with Databricks' Genie API,
# which is currently in Public Preview. 
# 
# Note: This is experimental code and is not intended for production use.
###

import json
import os
import time
from datetime import datetime
from typing import Optional

import pandas as pd
import requests
import streamlit as st

## Constants
MAX_RETRIES = 300
SLEEP_TIME_BETWEEN_RETRIES = 1

# Function to convert results to JSON format
def to_json_results(result):
    jsonified_results = json.dumps(result)
    return f"Genie Results are: {jsonified_results}"

# Function to convert results to string format
def to_string_results(result):
    results_string = result["sql_query_result"].to_dict(orient="records") if result["sql_query_result"] is not None else None
    return ("Genie Results are: \n"
            f"Space ID: {result['space_id']}\n"
            f"Conversation ID: {result['conversation_id']}\n"
            f"Question That Was Asked: {result['question']}\n"
            f"Content: {result['content']}\n"
            f"SQL Query: {result['sql_query']}\n"
            f"SQL Query Description: {result['sql_query_description']}\n"
            f"SQL Query Result: {results_string}\n"
            f"Error: {result['error']}")

# Function to construct URL
def make_url(host, path):
    return f"{host.rstrip('/')}/{path.lstrip('/')}"

# Function to start a conversation with Genie
def start_conversation(host, token, space_id, start_suffix=""):
    url = make_url(host, f"/api/2.0/genie/spaces/{space_id}/start-conversation")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    resp = requests.post(url, headers=headers, json={"content": "starting conversation" if not start_suffix else f"starting conversation {start_suffix}"})
    resp = resp.json()
    st.write(resp)
    try:
        return resp["conversation_id"]
    except Exception:
        return resp

# Function to ask a question to Genie
def ask_question(host, token, space_id, conversation_id, message):
    url = make_url(host, f"/api/2.0/genie/spaces/{space_id}/conversations/{conversation_id}/messages")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    resp_raw = requests.post(url, headers=headers, json={"content": message})
    resp = resp_raw.json()
    message_id = resp.get("message_id", resp.get("id"))
    if message_id is None:
        st.write(resp, resp_raw.url, resp_raw.status_code, resp_raw.headers)
        return {
            "space_id": space_id,
            "conversation_id": conversation_id,
            "question": message,
            "content": None,
            "sql_query": None,
            "sql_query_description": None,
            "sql_query_result": None,
            "error": "Failed to get message_id"
        }

    attempt = 0
    query = None
    query_description = None
    content = None

    while attempt < MAX_RETRIES:
        resp_raw = requests.get(make_url(host, f"/api/2.0/genie/spaces/{space_id}/conversations/{conversation_id}/messages/{message_id}"), headers=headers)
        resp = resp_raw.json()
        status = resp["status"]
        if status == "COMPLETED":
            try:
                query = resp["attachments"][0]["query"]["query"]
                query_description = resp["attachments"][0]["query"].get("description", None)
                content = resp["attachments"][0].get("text", {}).get("content", None)
            except Exception as e:
                return {
                    "space_id": space_id,
                    "conversation_id": conversation_id,
                    "question": message,
                    "content": resp["attachments"][0].get("text", {}).get("content", None),
                    "sql_query": None,
                    "sql_query_description": None,
                    "sql_query_result": None,
                    "error": str(e)
                }
            break

        elif status == "EXECUTING_QUERY":
            requests.get(make_url(host, f"/api/2.0/genie/spaces/{space_id}/conversations/{conversation_id}/messages/{message_id}/query-result"), headers=headers)
        elif status in ["FAILED", "CANCELED"]:
            return {
                "space_id": space_id,
                "conversation_id": conversation_id,
                "question": message,
                "content": None,
                "sql_query": None,
                "sql_query_description": None,
                "sql_query_result": None,
                "error": f"Query failed with status {status}"
            }
        elif status != "COMPLETED" and attempt < MAX_RETRIES:
            time.sleep(SLEEP_TIME_BETWEEN_RETRIES)
        else:
            return {
                "space_id": space_id,
                "conversation_id": conversation_id,
                "question": message,
                "content": None,
                "sql_query": None,
                "sql_query_description": None,
                "sql_query_result": None,
                "error": f"Query failed or still running after 300 seconds"
            }
        attempt += 1

    resp = requests.get(make_url(host, f"/api/2.0/genie/spaces/{space_id}/conversations/{conversation_id}/messages/{message_id}/query-result"), headers=headers)
    resp = resp.json()
    columns = resp["statement_response"]["manifest"]["schema"]["columns"]
    header = [str(col["name"]) for col in columns]
    rows = []
    output = resp["statement_response"]["result"]
    if not output:
        return {
            "space_id": space_id,
            "conversation_id": conversation_id,
            "question": message,
            "content": content,
            "sql_query": query,
            "sql_query_description": query_description,
            "sql_query_result": pd.DataFrame([], columns=header),
            "error": None
        }
    for item in resp["statement_response"]["result"]["data_typed_array"]:
        row = []
        for column, value in zip(columns, item["values"]):
            type_name = column["type_name"]
            str_value = value.get("str", None)
            if str_value is None:
                row.append(None)
                continue
            if type_name in ["INT", "LONG", "SHORT", "BYTE"]:
                row.append(int(str_value))
            elif type_name in ["FLOAT", "DOUBLE", "DECIMAL"]:
                row.append(float(str_value))
            elif type_name == "BOOLEAN":
                row.append(str_value.lower() == "true")
            elif type_name == "DATE":
                row.append(datetime.strptime(str_value, "%Y-%m-%d").date())
            elif type_name == "TIMESTAMP":
                row.append(datetime.strptime(str_value, "%Y-%m-%d %H:%M:%S"))
            elif type_name == "BINARY":
                row.append(bytes(str_value, "utf-8"))
            else:
                row.append(str_value)
        rows.append(row)

    query_result = pd.DataFrame(rows, columns=header)
    return {
        "space_id": space_id,
        "conversation_id": conversation_id,
        "question": message,
        "content": content,
        "sql_query": query,
        "sql_query_description": query_description,
        "sql_query_result": query_result,
        "error": None
    }