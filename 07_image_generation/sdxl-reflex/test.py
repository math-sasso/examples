
import requests
import json

url = "https://app.beam.cloud/endpoint/sdxl-reflex/v2"
payload = {}
headers = {
  "Authorization": "Vw-o1_PKvHuWFDYNGl2Zh6mTUYv7-9rFNY5-orm-o2LhEwpSE75Rmlw41dLC6cmTXJd3GEXYMBFVcfCsq1YWwg==",
  "Connection": "keep-alive",
  "Content-Type": "application/json"
}

response = requests.request("POST", url, 
  headers=headers,
  data=json.dumps(payload)
)

response.text
import pdb;pdb.set_trace()