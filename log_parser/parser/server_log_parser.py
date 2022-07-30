import argparse
import csv
import datetime as dt
import json

def load_log_file(log_file_path):
    with open(log_file_path, 'r') as f:
        packet_jsons = json.loads(f.read())
        return packet_jsons

def parse_log_file(packet_json) -> dict:
    processmining_elements = {}
    processmining_elements['timestamp'] = parse_timestamp(packet_json)
    processmining_elements['client_ip'] = parse_client_ip(packet_json)
    processmining_elements['server_ip'] = parse_server_ip(packet_json)
    processmining_elements['http_referer'] = parse_http_referer(packet_json)
    processmining_elements['http_request_url'] = parse_http_request_url(packet_json)
    processmining_elements['html'] = parse_html(packet_json)
    return processmining_elements

def parse_timestamp(packet_json):
    timestamp = dt.datetime.strptime(packet_json.get('_source').get('layers').get('frame').get('frame.time'), '%b %d, %Y %H:%M:%S.%f000 %Z')
    year = timestamp.year
    month = timestamp.month
    day = timestamp.day
    hour = timestamp.hour
    minute = timestamp.minute
    second = timestamp.second
    microsecond = timestamp.microsecond
    return f'{year}-{month}-{day} {hour}:{minute}:{second}.{microsecond}'

def parse_client_ip(packet_json):
    return packet_json.get('_source').get('layers').get('ip').get('ip.src')

def parse_server_ip(packet_json):
    return packet_json.get('_source').get('layers').get('ip').get('ip.dst')

def parse_http_referer(packet_json):
    try:
        return packet_json.get('_source').get('layers').get('http').get('http.referer')
    except AttributeError:
        return None
    
def parse_http_request_url(packet_json):
    try:
        return packet_json.get('_source').get('layers').get('http').get('http.request.full_uri') \
            or packet_json.get('_source').get('layers').get('http').get('http.response_for.uri')
    except AttributeError:
        return None

def parse_html(packet_json):
    try:
        return packet_json.get('_source').get('layers').get('http').get('http.file_data')
    except AttributeError:
        return None

def parse_log_file_to_csv(log_file_path, csv_file_path):
    packet_jsons = load_log_file(log_file_path)
    processmining_elements = list(map(parse_log_file, packet_jsons))
    with open(csv_file_path, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=processmining_elements[0].keys())
        writer.writeheader()
        writer.writerows(processmining_elements)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--file_path', type=str, required=True, help='The path of raw server logs file. (require list of jsons format with .txt).')
    parser.add_argument('-o', '--save_path', type=str, required=True, help='The path to save parsed csv data.')
    return parser.parse_args()

def main(file_path, save_path):
    parse_log_file_to_csv(file_path, save_path)

if __name__ == '__main__':
    args = parse_args()
    main(args.file_path, args.save_path)