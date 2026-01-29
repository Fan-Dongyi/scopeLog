import datetime
import pandas as pd
import os, re
import json
import logging
import sys
import time
from os.path import dirname
import logging
import logging.config
import re
import math
from tabulate import tabulate

pd.options.display.max_colwidth = None

if os.path.exists("./result.log"):
    os.rename("./result.log", "./result.log.prev")

result_logger = logging.getLogger("result_logger")
#result_logger.setLevel(logging.INFO)
result_logger.setLevel(logging.DEBUG)
result_handler = logging.FileHandler("./result.log", mode="w")
result_handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
result_logger.addHandler(result_handler)

result_logger.info("Starting evaluation at datetime: %s", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

BLUE = "\033[34m"
RESET = "\033[0m"
YELLOW = "\033[33m"
GREEN = "\033[32m"


benchmark_settings = {
    'HPC': {
        'log_file': 'HPC/HPC_2k.log',
        'log_format': '<LogId> <Node> <Component> <State> <Time> <Flag> <Content>',
        'regex': [],
        'filter': []
        },

    'OpenStack': {
        'log_file': 'OpenStack/OpenStack_2k.log',
        'log_format': '<Logrecord> <Date> <Time> <Pid> <Level> <Component> \\[<ADDR>\\] <Content>',
        'regex': ["(\\w+-\\w+-\\w+-\\w+-\\w+)", r'HTTP\/\d+\.\d+', r'(?:\d{1,3}\.){3}\d{1,3},(?:\d{1,3}\.){3}\d{1,3}'],
        'filter': [r'HTTP\/\d+\.\d+', ]
        },

    'BGL': {
        'log_file': 'BGL/BGL_2k.log',
        'log_format': '<Label> <Timestamp> <Date> <Node> <Time> <NodeRepeat> <Type> <Component> <Level> <Content>',
        'regex': [],
        'filter': []
        },

    'HDFS': {
        'log_file': 'HDFS/HDFS_2k.log',
        'log_format': '<Date> <Time> <Pid> <Level> <Component>: <Content>',
        'regex': [r'blk_-?\d+'],
        'filter': []
        },

    'Hadoop': {
        'log_file': 'Hadoop/Hadoop_2k.log',
        'log_format': '<Date> <Time> <Level> \\[<Process>\\] <Component>: <Content>',
        #'regex': [r'\[.*?(_.*?)+\]', ],
        'regex': [],
        'filter': []
        },

    'Spark': {
        'log_file': 'Spark/Spark_2k.log',
        'log_format': '<Date> <Time> <Level> <Component>: <Content>',
        'regex': [],
        'filter': []
        },

    'Zookeeper': {
        'log_file': 'Zookeeper/Zookeeper_2k.log',
        'log_format': '<Date> <Time> - <Level>  \\[<Node>:<Component>@<Id>\\] - <Content>',
        'regex': [],
        'filter': []
        },

    'Thunderbird': {
        'log_file': 'Thunderbird/Thunderbird_2k.log',
        'log_format': '<Label> <Timestamp> <Date> <User> <Month> <Day> <Time> <Location> <Component>(\\[<PID>\\])?: <Content>',
        'regex': [r'(\d+\.){3}\d+', r'\bLOCAL\(\d+\)', r'_([A-Z]\d+)'],
        'filter': []
        },

    'Windows': {
        'log_file': 'Windows/Windows_2k.log',
        'log_format': '<Date> <Time>, <Level>                  <Component>    <Content>',
        'regex': [],
        'filter': []
        },

    'Linux': {
        'log_file': 'Linux/Linux_2k.log',
        'log_format': '<Month> <Date> <Time> <Level> <Component>(\\[<PID>\\])?: <Content>',
        'regex': [],
        'filter': []
        },

    'Andriod': {
        'log_file': 'Android/Android_2k.log',
        'log_format': '<Date> <Time>  <Pid>  <Tid> <Level> <Component>: <Content>',
        'regex': [r'(/[\w-]+)+', r'([\w-]+\.){2,}[\w-]+', r'\b(\-?\+?\d+)\b|\b0[Xx][a-fA-F\d]+\b|\b[a-fA-F\d]{4,}\b',
                  r'-\<\*\>'],
        'filter': []
        },

    'HealthApp': {
        'log_file': 'HealthApp/HealthApp_2k.log',
        'log_format': '<Time>\\|<Component>\\|<Pid>\\|<Content>',
        'regex': [],
        'filter': []
        },

    'Apache': {
        'log_file': 'Apache/Apache_2k.log',
        'log_format': '\\[<Time>\\] \\[<Level>\\] <Content>',
        'regex': [r'\/(?:\w+\/){2,}\w+\.\w+$'],
        'filter': []
        },

    'Proxifier': {
        'log_file': 'Proxifier/Proxifier_2k.log',
        'log_format': '\\[<Time>\\] <Program> - <Content>',
        'regex': [r'<\d+\ssec', r'([\w-]+\.)+[\w-]+(:\d+)?', r'\d{2}:\d{2}(:\d{2})*', r'[KGTM]B'],
        "filter": [r' \(\d+(\.\d+)?\s(?:K|M)B\)', ]
        },

    'OpenSSH': {
        'log_file': 'OpenSSH/OpenSSH_2k.log',
        'log_format': '<Date> <Day> <Time> <Component> sshd\\[<Pid>\\]: <Content>',
        #'regex': [r"(\d+):"],
        'regex': [r'(\d+\.){3}\d+', r'([\w-]+\.){2,}[\w-]+'],
        'filter': []
        },

    'Mac': {
        'log_file': 'Mac/Mac_2k.log',
        'log_format': '<Month>  <Date> <Time> <User> <Component>\\[<PID>\\]( \\(<Address>\\))?: <Content>',
        #'regex': [],
        'regex': [r'([\w-]+\.){2,}[\w-]+'],
        'filter': []
        },

    'Thunderbird_epd': {
        'log_file': 'Thunderbird/Thunderbird_2k.log',
        'log_format': '<Label> <Timestamp> <Date> <User> <Month> <Day> <Time> <Location> <Component>(\\[<PID>\\])?: <Content>',
        'regex': [],
        'filter': []
        },

    'Audit': {
        'log_file': 'Audit/Audit_2k.log',
        'log_format': "type=<Type> msg=audit\\(<Time>\\): <Content>",
        'regex': [],
        'filter': []
    },
}

class format_log:    # this part of code is from LogPai https://github.com/LogPai
    def __init__(self, log_format, indir='./'):
        self.path = indir
        self.logName = None
        self.df_log = None
        self.log_format = log_format

    def get_format_logs(self, logName):
        self.logName=logName
        self.load_data()
        return self.df_log

    def generate_logformat_regex(self, logformat):
        """ Function to generate regular expression to split log messages
        """
        headers = []
        splitters = re.split(r'(<[^<>]+>)', logformat)
        regex = ''
        for k in range(len(splitters)):
            if k % 2 == 0:
                splitter = re.sub(r' +', r'\\s+', splitters[k])
                regex += splitter
            else:
                header = splitters[k].strip('<').strip('>')
                regex += '(?P<%s>.*?)' % header
                headers.append(header)
        regex = re.compile('^' + regex + '$')
        return headers, regex

    def log_to_dataframe(self, log_file, regex, headers, logformat):
        """ Function to transform log file to dataframe
        """
        log_messages = []
        linecount = 0
        with open(log_file, 'r', encoding='UTF-8') as fin:
            for line in fin.readlines():
                try:
                    match = regex.search(line.strip())
                    message = [match.group(header) for header in headers]
                    log_messages.append(message)
                    linecount += 1
                except Exception as e:
                    pass
        logdf = pd.DataFrame(log_messages, columns=headers)
        logdf.insert(0, 'LineId', None)
        logdf['LineId'] = [i + 1 for i in range(linecount)]
        return logdf


    def load_data(self):
        headers, regex = self.generate_logformat_regex(self.log_format)
        self.df_log = self.log_to_dataframe(os.path.join(self.path, self.logName), regex, headers, self.log_format)


def preprocess(line, rex, filter):
    for currentFil in filter:
        line = re.sub(currentFil, '', line)
    for currentRex in rex:
        line = re.sub(currentRex, '<*>', line)
    return line

def isTemplateSameWithGroundtruth(template, groundtruth):
    """
    Compare the template with the groundtruth template.
    :param template: The template generated by the miner.
    :param groundtruth: The groundtruth template.
    :return: True if they are the same, False otherwise.
    """
    groundtruth = re.sub(r'(<\*>[\s]*){2,}', '<*> ', groundtruth)
    normalized_groundtruth = re.sub(r'\s+', '', groundtruth).strip()
    normalized_template = re.sub(r'\s+', '', template).strip()

    return normalized_template == normalized_groundtruth

def sample_event(group, n):
    if len(group) > n:
        return group.sample(n=n, random_state=42)
    else:
        return group

def parse_file_to_table(file_path):
    # Define regex to parse data, with support for template updates
    pattern = re.compile(
        r"Evaluation on Dataset: (\S+), Group Accuracy: ([\d.]+), PA Accuracy: ([\d.]+), FGA: ([\d.]+), FTA: ([\d.]+), "
        r"Duration: ([\d.]+) sec, "
        r"Total of (\d+) lines, rate ([\d.]+) lines/sec, (\d+) clusters, "
        r"Template update from forward tree: (\d+), Template update from reverse tree: (\d+), Template update from pool: (\d+), "
        r"Total log length: (\d+), Total length node count: (\d+), Total LLM Call count: (\d+), "
        r"Total LLM Call Tokens: (\d+)"
    )

    # Store extracted data
    best_data_by_dataset = {}

    # Read file and parse data
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            match = pattern.search(line)
            if match:
                (
                    dataset, GA_accuracy, PA_accuracy, FGA, FTA, duration, line_number, rate,
                    clusters, upd_fwd_tree, upd_rv_tree, upd_pool,
                    total_log_len, len_node_cnt, llm_call_cnt, llm_call_tokens
                ) = match.groups()

                data = [
                    dataset,
                    float(GA_accuracy),
                    float(PA_accuracy),
                    float(FGA),
                    float(FTA),
                    float(duration),
                    int(line_number),
                    int(clusters),
                    #int(upd_fwd_tree),
                    #int(upd_rv_tree),
                    #int(upd_pool),
                    int(llm_call_cnt),
                    int(llm_call_tokens)
                ]

                if dataset not in best_data_by_dataset or data[1] > best_data_by_dataset[dataset][1]:
                    best_data_by_dataset[dataset] = data

    # Create table using Pandas
    best_data = list(best_data_by_dataset.values())
    df = pd.DataFrame(best_data, columns=[
        "Dataset", "GA", "PA", "FGA", "FTA", "Duration", "#Line",
        "#Template",
        #"#Upd(Fwd)", "#Upd(Rev)", "#Upd(Pool)",
        "#LLM Call", "#LLM Tokens"
    ])

    # Calculate averages with "Average" in Dataset column
    if len(df) > 0:
        avg_row = ["Average"] + [df[col].mean() for col in df.columns[1:]]
        df.loc[len(df)] = avg_row

    return df


benchmark_result=[]

# Add the directory containing the module to sys.path
scope_dir = os.path.join(os.path.dirname(__file__), "../code")
sys.path.insert(0, scope_dir)  # Insert at the start of sys.path

from templateMiner import TemplateMiner
from templateMinerConfig import TemplateMinerConfig

#in_log_file = os.path.join(os.path.dirname(__file__), "scopeTestFile.txt")
config = TemplateMinerConfig()
config.load(f"{dirname(__file__)}/scope.ini")
config.profiling_enabled = True



# Add main function with argument parsing
def main():
    import argparse

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='SCOPE Log Template Mining Evaluator')
    parser.add_argument('--dataset', type=str, default='2K',
                        help='Dataset size: 2K (default) or Full')
    parser.add_argument('--type', type=str, default='corrected',
                        help='Log file type: corrected (default) or raw')
    # Convert dataset argument to uppercase for case-insensitive comparison
    args = parser.parse_args()
    args.dataset = args.dataset.upper()
    if args.dataset not in ['2K', 'FULL']:
        parser.error("Dataset must be either '2K' or 'Full'.")

    args.type = args.type.upper()
    if args.type not in ['CORRECTED', 'RAW']:
        parser.error("Type must be either 'CORRECTED' or 'RAW'.")

    global log_file_category, log_file_type
    log_file_category = '2k' if args.dataset == '2K' else 'full'
    log_file_type = 'corrected' if args.type == 'CORRECTED' else 'raw'

    result_logger.info("Dataset:%s, Type:%s, Bi-Tree:%s, Pool:%s, SLM:%s, LLM:%s, model:%s, thinking:%s",
                    args.dataset, args.type, config.bi_tree_support, config.pool_support, config.POS_support, config.LLM_support,
                    config.LLM_model, config.LLM_thinking)

    FullDataSets = [
        "Proxifier",
        "Apache",
        "OpenSSH",
        "HDFS",
        "OpenStack",
        "HPC",
        "Zookeeper",
        "HealthApp",
        "Hadoop",
        "Spark",
        "BGL",
        "Linux",
        "Mac",
        "Thunderbird",
    ]
    PartDataSets = [
        "Proxifier",
        "Apache",
        "OpenSSH",
        "HDFS",
        "OpenStack",
        "HPC",
        "Zookeeper",
        "HealthApp",
        "Hadoop",
        "Spark",
        "BGL",
        "Linux",
        "Mac",
        "Thunderbird",
        "Windows",
        "Andriod",
    ]
    allDataSets = [
        "Proxifier",
        #"Apache",
        #"OpenSSH",
        #"HDFS",
        #"OpenStack",
        #"HPC",
        #"Zookeeper",
        #"HealthApp",
        #"Hadoop",
        #"Spark",
        #"BGL",
        #"Linux",
        #"Mac",
        #"Thunderbird",
        #"Windows",
        #"Andriod",
    ]
    # Execute evaluation

    datasets = FullDataSets if log_file_category == 'full' else PartDataSets
    datasets = allDataSets

    for dataset in datasets:
        setting = benchmark_settings[dataset]
        parse = format_log(log_format=setting['log_format'], indir=dirname(__file__)+'/loghub-2K/')
        df = pd.DataFrame()

        if log_file_category == 'full':
            setting['log_file'] = setting['log_file'].replace("2k", "full")
            structured_log_file = os.path.join(dirname(__file__), 'loghub-2.0', setting['log_file'] + '_structured.csv')
            df = pd.read_csv(structured_log_file)
            sentences = df['Content'].tolist()
        else:  # log_file_category is '2k'
            if log_file_type == 'corrected':
                structured_log_file = os.path.join(dirname(__file__), 'loghub-2K', setting['log_file'] + '_structured_corrected.csv')
            else:  # log_file_type is 'raw'
                structured_log_file = os.path.join(dirname(__file__), 'loghub-2K', setting['log_file'] + '_structured.csv')

            df = pd.read_csv(structured_log_file)
            sentences = df['Content'].tolist()

        df_groundtruth = df
        df_data = pd.DataFrame()

        retryMax = 1
        tryCnt = 0
        while(tryCnt < retryMax):
            template_miner = TemplateMiner(config=config)

            start_time = time.time()
            batch_start_time = start_time
            batch_size = 10000
            line_count = 0
            log_templateIds = []
            log_templateStrs = []

            for line in sentences:
                line = line.rstrip()
                line = preprocess(line, setting['regex'], setting['filter'])
                result = template_miner.add_log_message(line)
                line_count += 1
                if line_count % batch_size == 0:
                    time_took = time.time() - batch_start_time
                    rate = batch_size / time_took
                    batch_start_time = time.time()
                if result["change_type"] != None:
                    result_json = json.dumps(result)

                log_templateIds.append(result["cluster_id"])
                log_templateStrs.append(result["template_mined"])

            time_took = time.time() - start_time
            rate = line_count / time_took

            df_data['EventId'] = log_templateIds
            df_data['EventTemplate'] = log_templateStrs

            GA_cnt = 0 # Group match log count
            PA_cnt = 0 # template match log count
            TP_cnt = 0 # template match template count
            TA_cnt = 0 # Group & template match template count
            data = df_data['EventId']
            groundtruth = df_groundtruth['EventId']
            for parsed_eventId in data.value_counts().index:
                logIds = data[data == parsed_eventId].index
                groundtruth_eventIDs_Of_logLines = groundtruth[logIds].value_counts()
                if groundtruth_eventIDs_Of_logLines.size == 1:
                    groundtruth_eventId = groundtruth_eventIDs_Of_logLines.index[0]
                    groundtruth_logLines_Of_eventId = groundtruth[groundtruth == groundtruth_eventId]
                    GroupMatch = False
                    if logIds.size == groundtruth_logLines_Of_eventId.size:
                        GA_cnt += logIds.size
                        TP_cnt += 1
                        GroupMatch = True
                    else:
                        diff = groundtruth_logLines_Of_eventId.index.difference(logIds)
                    if isTemplateSameWithGroundtruth(df_data['EventTemplate'][logIds[-1]], df_groundtruth['EventTemplate'][groundtruth_logLines_Of_eventId.index[0]]):
                        PA_cnt += logIds.size
                        if GroupMatch:
                            TA_cnt += 1
                else:
                    for groundtruth_eventId, groundtruth_logLines_num in groundtruth_eventIDs_Of_logLines.items():
                        gt_indices = df_groundtruth[df_groundtruth['EventId'] == groundtruth_eventId].index
                        if len(gt_indices) > 0:
                            gt_template = df_groundtruth['EventTemplate'][gt_indices[0]]
                            if isTemplateSameWithGroundtruth(df_data['EventTemplate'][logIds[-1]], gt_template):
                                PA_cnt += groundtruth_logLines_num

            GA_accuracy = round(float(GA_cnt) / data.size, 4)
            PGA = round(float(TP_cnt) / len(data.value_counts()), 4)
            RGA = round(float(TP_cnt) / len(groundtruth.value_counts()), 4)
            FGA = round(2 * PGA * RGA / (PGA + RGA), 4) if (PGA + RGA) > 0 else 0.0

            PA_accuracy = round(float(PA_cnt) / data.size, 4)
            PTA = round(float(TA_cnt) / len(data.value_counts()), 4)
            RTA = round(float(TA_cnt) / len(groundtruth.value_counts()), 4)
            FTA = round(2 * PTA * RTA / (PTA + RTA), 4) if (PTA + RTA) > 0 else 0.0

            GA_accuracy = f"{GA_accuracy:.4f}"
            PA_accuracy = f"{PA_accuracy:.4f}"
            FGA = f"{FGA:.4f}"
            FTA = f"{FTA:.4f}"
            result_logger.info('\n=== Evaluation on %s ==='%dataset)
            print(f"\n{'*'*100} \n")
            print('Dataset:', dataset, 'GA_accuracy:', GA_accuracy, 'PA_accuracy:', PA_accuracy, 'FGA:', FGA, 'FTA:', FTA)
            print(f"\n{'*'*100} \n")
            print('Dataset:', dataset, 'GA_accuracy:', GA_accuracy, 'PA_accuracy:', PA_accuracy)
            result_logger.info(f"Evaluation on Dataset: {dataset}, Group Accuracy: {GA_accuracy}, PA Accuracy: {PA_accuracy}, FGA: {FGA}, FTA: {FTA}, "
                f"Duration: {time_took:.2f} sec, "
                f"Total of {line_count} lines, rate {rate:.1f} lines/sec, {len(template_miner.scope.clusters)} clusters, "
                f"Template update from forward tree: {template_miner.scope.TplUpdByFwdTree}, Template update from reverse tree: {template_miner.scope.TplUpdByRevTree}, Template update from pool: {template_miner.scope.TplUpdByPool}, "
                f"Total log length: {template_miner.scope.totalTokens}, Total length node count: {template_miner.scope.lengthNodeCounts}, Total LLM Call count: {template_miner.scope.llmCallCnt}, "
                f"Total LLM Call Tokens: {template_miner.scope.llmCallTokens}, "
                f"logMatchInTree: {template_miner.scope.logMatchedInTree}, posCallCntInTree: {template_miner.scope.posCallCntInTree}, llmCallCntInTree: {template_miner.scope.llmCallCntInTree}, "
                f"logMatchInPool: {template_miner.scope.logMatchedInPool}, posCallCntInPool: {template_miner.scope.posCallCntInPool}, llmCallCntInPool: {template_miner.scope.llmCallCntInPool}"
                )

            if config.LLM_support:
                tryCnt += 1
            else:
                break

    file_path = "./result.log"
    # Extract system configuration info from the log file
    config_info = ""
    with open("./result.log", "r") as f:
        for line in f:
            if "Starting evaluation at datetime:" in line or "Bi-Tree:" in line or "Dataset type:" in line:
                config_info += line.strip() + "\n"
    print("\n" + config_info)

    table = parse_file_to_table(file_path)
    # Print the table to console
    print(tabulate(table, headers="keys", tablefmt="github"))

    # Log the table and averages to result.log
    result_logger.info("\nEvaluation Results Summary:")
    result_logger.info(config_info)
    result_logger.info("\n" + tabulate(table, headers="keys", tablefmt="github"))

    table.to_csv("output.csv", index=False)

# Run main function if script is executed directly
if __name__ == "__main__":
    main()












