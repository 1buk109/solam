import argparse
import csv
import datetime as dt
import json

class ServerLogParser:
    def __init__(self, file_path, save_path):
        self.file_path = file_path
        self.save_path = save_path

    def load_log_file(self, log_file_path):
        with open(log_file_path, 'r') as f:
            packet_jsons = json.loads(f.read())
            return packet_jsons

    def parse_log_file(self, packet_json) -> dict:
        processmining_elements = {}
        processmining_elements['timestamp'] = self.parse_timestamp(packet_json)
        processmining_elements['client_ip'] = self.parse_client_ip(packet_json)
        processmining_elements['server_ip'] = self.parse_server_ip(packet_json)
        processmining_elements['http_referer'] = self.parse_http_referer(packet_json)
        processmining_elements['http_request_url'] = self.parse_http_request_url(packet_json)
        processmining_elements['html'] = self.parse_html(packet_json)
        return processmining_elements

    def parse_timestamp(self, packet_json):
        timestamp = dt.datetime.strptime(packet_json.get('_source').get('layers').get('frame').get('frame.time'), '%b %d, %Y %H:%M:%S.%f000 %Z')
        year = timestamp.year
        month = timestamp.month
        day = timestamp.day
        hour = timestamp.hour
        minute = timestamp.minute
        second = timestamp.second
        microsecond = timestamp.microsecond
        return f'{year}-{month}-{day} {hour}:{minute}:{second}.{microsecond}'

    def parse_client_ip(self, packet_json):
        return packet_json.get('_source').get('layers').get('ip').get('ip.src')

    def parse_server_ip(self, packet_json):
        return packet_json.get('_source').get('layers').get('ip').get('ip.dst')

    def parse_http_referer(self, packet_json):
        try:
            return packet_json.get('_source').get('layers').get('http').get('http.referer')
        except AttributeError:
            return None
        
    def parse_http_request_url(self, packet_json):
        try:
            return packet_json.get('_source').get('layers').get('http').get('http.request.full_uri') \
                or packet_json.get('_source').get('layers').get('http').get('http.response_for.uri')
        except AttributeError:
            return None

    def parse_html(self, packet_json):
        try:
            return packet_json.get('_source').get('layers').get('http').get('http.file_data')
        except AttributeError:
            return None

    def parse_log_file_to_csv(self, log_file_path, csv_file_path):
        packet_jsons = self.load_log_file(log_file_path)
        processmining_elements = list(map(self.parse_log_file, packet_jsons))
        with open(csv_file_path, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=processmining_elements[0].keys())
            writer.writeheader()
            writer.writerows(processmining_elements)

    def main(self):
        self.parse_log_file_to_csv(self.file_path, self.save_path)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--file_path', type=str, required=True, help='The path of raw server logs file. (require list of jsons format with .txt).')
    parser.add_argument('-o', '--save_path', type=str, required=True, help='The path to save parsed csv data.')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    slp = ServerLogParser(args.file_path, args.save_path)
    slp.main()