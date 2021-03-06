import argparse
import numpy as np
import pandas as pd

class PMLogParser:
    def __init__(self, file_path, save_path, server_ip):
        self.file_path = file_path
        self.save_path = save_path
        self.SERVER_IP = server_ip

    def define_sessions(self, file_path, COLUMNS=['case_id', 'activity', 'timestamp']):
        df_parsed_server_logs = self.parse_logs(file_path)
        df_parsed_server_logs_pm = pd.DataFrame(columns=COLUMNS)
        case_id = 1
        for row in df_parsed_server_logs.index:
            session_record = self.parse_session_record_for_pm(case_id, df_parsed_server_logs.loc[row, 'http_request_url'], df_parsed_server_logs.loc[row, 'timestamp'])
            df_parsed_server_logs_pm = pd.concat([df_parsed_server_logs_pm, session_record], axis=0)
            try:
                if (df_parsed_server_logs.loc[row, 'http_request_url'] == df_parsed_server_logs.loc[row + 1, 'http_referer']) \
                    and (df_parsed_server_logs.loc[row, 'client_ip'] == df_parsed_server_logs.loc[row + 1, 'client_ip']):
                    continue
                elif np.isnan(df_parsed_server_logs.loc[row + 1, 'http_referer']):
                    process_end_record = self.generate_process_end_record(case_id, df_parsed_server_logs.loc[row, 'timestamp'])
                    df_parsed_server_logs_pm = pd.concat([df_parsed_server_logs_pm, process_end_record], axis=0)
                    case_id += 1
                else:
                    print('exception')
                    break
            except KeyError:
                process_end_record = self.generate_process_end_record(case_id, df_parsed_server_logs.loc[row, 'timestamp'], COLUMNS)
                df_parsed_server_logs_pm = pd.concat([df_parsed_server_logs_pm, process_end_record], axis=0)
        return df_parsed_server_logs_pm.reset_index(drop=True)

    def parse_logs(self, file_path):
        df_parsed_server_logs = pd.read_csv(file_path)
        df_parsed_server_logs['timestamp'] = pd.to_datetime(df_parsed_server_logs['timestamp'])
        df_parsed_server_logs = df_parsed_server_logs.query('client_ip != @self.SERVER_IP') # server????????????????????????????????????????????????
        df_parsed_server_logs.dropna(subset=['http_request_url'], inplace=True)             # request NaN??????????????????????????????
        df_parsed_server_logs = df_parsed_server_logs[~df_parsed_server_logs['http_request_url'].str.contains('favicon.ico')]
        return df_parsed_server_logs.sort_values(['client_ip', 'timestamp']).reset_index(drop=True)
        

    def parse_session_record_for_pm(self, case_id, activity, timestamp, COLUMNS=['case_id', 'activity', 'timestamp']):
        return pd.DataFrame([pd.Series(data = [case_id, activity, timestamp], index = COLUMNS)])

    def generate_process_end_record(self, case_id, timestamp, COLUMNS=['case_id', 'activity', 'timestamp']):
        return pd.DataFrame([pd.Series(data = [case_id, 'process_end', timestamp], index = COLUMNS)])

    def main(self):
        self.define_sessions(self.file_path).to_csv(self.save_path, index = False)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--file_path', type=str, required=True, help='The path of the parsed server logs csv file.')
    parser.add_argument('-o', '--save_path', type=str, required=True, help='The path of the csv file parsed for PM.')
    return parser.parse_args()

if __name__ == '__main__':
    SERVER_IP = '10.19.11.215'
    args = parse_args()
    pmlp = PMLogParser(args.file_path, args.save_path, SERVER_IP)
    pmlp.main()