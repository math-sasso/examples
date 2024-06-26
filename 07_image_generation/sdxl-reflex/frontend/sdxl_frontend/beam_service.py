import requests
import time
BEAM_TOKEN = ""
BEAM_URL = ""


class BeamService:
    def __init__(self, prompt):
        self.url = BEAM_URL
        self.headers = {
            "Authorization": f"Bearer {BEAM_TOKEN}",
            "Content-Type": "application/json",
        }
        self.data = {"prompt": prompt}

    def call_api(self):
        start_time = time.time()
        
        response = requests.post(
            self.url, headers=self.headers, json=self.data, stream=True
        )

        print("------> Raw response <------\n")
        print(response.text)
        
        end_time = time.time()
        duration = end_time - start_time
        print(f"Time taken to run call_api: {duration:.2f} seconds")

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request failed with status code {response.status_code}")


class BeamTaskStatus:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {BEAM_TOKEN}",
            "Content-Type": "application/json",
        }

    def call_api(self,task_id):
        response = requests.get(
            f"https://api.beam.cloud/v2/task/{task_id}", headers=self.headers
        )

        import pdb;pdb.set_trace()
        return response
