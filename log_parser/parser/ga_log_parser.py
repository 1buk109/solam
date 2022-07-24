import argparse
import pandas as pd

def insert_process_end(file_path, COLUMNS=['case_id', 'activity', 'timestamp']):
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

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--file_path', type=str, required=True, help='The path of the raw GA csv file.')
    parser.add_argument('-o', '--save_path', type=str, required=True, help='The path of the GA csv file inserted process_end.')
    return parser.parse_args()
    
def main(file_path, save_path):
    insert_process_end(file_path).to_csv(save_path, index = False)

if __name__ == '__main__':
    args = parse_args()
    main(args.file_path, args.save_path)