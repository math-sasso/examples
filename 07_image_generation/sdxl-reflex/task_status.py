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
