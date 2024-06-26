import time
import requests

BEAM_TOKEN = "Vw-o1_PKvHuWFDYNGl2Zh6mTUYv7-9rFNY5-orm-o2LhEwpSE75Rmlw41dLC6cmTXJd3GEXYMBFVcfCsq1YWwg=="
BEAM_URL = "https://app.beam.cloud/endpoint/id/a94fd09c-ecbd-4305-abc6-611dc8242213"

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
        
        elapsed_time = time.time() - start_time
        print(f"Time elapsed: {elapsed_time:.2f} seconds")
        
        if response.status_code == 200:
            print(response.text)
            return response.json()
        else:
            raise Exception(f"Request failed with status code {response.status_code}")

# if __name__ == '__main__':
#     BeamService(prompt="a bicile").call_api()

