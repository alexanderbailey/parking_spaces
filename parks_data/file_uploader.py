import argparse
import requests
from time import sleep
import os

rest_base_url = 'http://localhost:8000'


class FileUploader:

    session: requests.Session

    def __init__(self):
        self.session = requests.session()

    def upload_file(self, file_path, weather: bool):
        if weather:
            endpoint = f'{rest_base_url}/v1/weather/upload'
        else:
            endpoint = f'{rest_base_url}/v1/data/upload'
        files = {'server_response': open(file_path, 'rb')}
        for attempt in range(3):
            try:
                response = self.session.post(endpoint, files=files)
                if response.status_code == 201:
                    print(f"Successfully uploaded file {response.text}")
                    return
                else:
                    raise requests.HTTPError(f"Error uploading file: {response.text}")
            except requests.exceptions.SSLError:
                print(f"Upload attempt {attempt} failed...")
                sleep(2)
                continue
        raise TimeoutError("Upload failed")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--weather", "-w", action='store_true', required=False, help="Upload weather data")
    parser.add_argument("--file", "-f", type=str, required=True, help="The file to be uploaded")
    args = parser.parse_args()

    uploader = FileUploader()
    uploader.upload_file(args.file, args.weather)
