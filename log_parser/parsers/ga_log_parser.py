import argparse
import pandas as pd

class GALogParser:
    def __init__(self, file_path, save_path):
        self.file_path = file_path
        self.save_path = save_path

    def insert_process_end(self, file_path, COLUMNS=['case_id', 'activity', 'timestamp']):
        df_ga_log = pd.read_csv(file_path)
        df_ga_log.columns = COLUMNS
        df_ga_log = df_ga_log.sort_values([COLUMNS[0], COLUMNS[2]]).reset_index(drop=True)
        df_ga_log_pm = pd.DataFrame(columns=COLUMNS)
        for row in df_ga_log.index:
            df_ga_log_pm = pd.concat([df_ga_log_pm, pd.DataFrame([df_ga_log.loc[row, :]])], axis=0)
            try:
                if df_ga_log.loc[row, COLUMNS[0]] != df_ga_log.loc[row + 1, COLUMNS[0]]:
                    process_end_record = pd.DataFrame([df_ga_log.loc[row, :]])
                    process_end_record['activity'] = 'process_end'
                    df_ga_log_pm = pd.concat([df_ga_log_pm, process_end_record], axis=0)
            except KeyError:
                process_end_record = pd.DataFrame([df_ga_log.loc[row, :]])
                process_end_record['activity'] = 'process_end'
                df_ga_log_pm = pd.concat([df_ga_log_pm, process_end_record], axis=0)
        return df_ga_log_pm.reset_index(drop=True)

    def main(self):
        self.insert_process_end(self.file_path).to_csv(self.save_path, index = False)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--file_path', type=str, required=True, help='The path of the raw GA csv file.')
    parser.add_argument('-o', '--save_path', type=str, required=True, help='The path of the GA csv file inserted process_end.')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    galp = GALogParser(args.file_path, args.save_path)
    galp.main()