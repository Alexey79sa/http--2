from pprint import pprint
from this import s

import requests

def err_msg(http_code, msg=''):
    print(f'\n\tHttp code:\t{http_code}')
    err = int(http_code) / 100 >= 4
    if err:
        print(msg)
        print('The file has not been uploaded to Yandex.Disk!')
        print('The program terminated with an error')
    else:
        print("'The file is uploaded to Yandex.Disk!'")
    return error

def get_address_api():
    return 'https://cloud-api.yandex.net/'


class YandexDisk:


    def __init__(self, token: str):
        self.token = token


    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Autorization': f'OAuth {self.token}'
        }


    def _get_upload_link(self, disk_file_path):
        print(f'Requesting Yandex.Disk API file download link {disk_file_path} ...')
        upload_url = get_address_api() + 'v1/disk/resources/upload'
        headers = self.get_headers()
        params = {"path": disk_file_path, 'overwrite': 'true'}
        response = requests.get(upload_url, params=params, headers=headers)
        if err_msg(response.status_code, 'The link to download the file was not received!'):
            quit(1)
        pprint(response.json())
        return response.json()


    def upload_file_to_disk(self, disk_file_path, filename):
        print(f'\nLets write a file {disk_file_path} on Yandex.Disk ...')
        href = self._get_upload_link(disk_file_path=disk_file_path)
        response = requests.put(href, data=open(filename, 'rb'))
        if err_msg(response.status_code):
            quit(1)
        response.raise_for_status()
