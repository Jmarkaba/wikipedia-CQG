import argparse
import pandas as pd


def combine_data(args):
    with open(args.ctx_ans_file, encoding="utf-8") as fin:
        input_lines = [x.strip().split(" [SEP] ") for x in fin.readlines()]
    with open(args.q_file, encoding="utf-8") as fin:
        q_lines = [x.strip() for x in fin.readlines()]
        assert len(input_lines) == len(q_lines)
        data = [(x[0], y, x[1], 'yes') for x, y in zip(input_lines, q_lines)]
    df = pd.DataFrame(data)
    df.columns = ['Context', 'Question', 'Answer', 'Label']
    df.to_csv(args.output_file, header=args.header, index=False)


def main():
    parser = argparse.ArgumentParser(
        description='Create a csv file from the formatted context-answer file and the resulting questions file'
    )
    parser.add_argument(
        '--ctx_ans_file',
        type=str,
        default=None,
        required=True,
        help='The file containing passages and answers, e.g. sample.pa.txt'
    )
    parser.add_argument(
        '--q_file',
        type=str,
        default=None,
        required=True,
        help='THe file containing generated questions, e.g., sample.q.txt'
    )
    parser.add_argument(
        '--output_file',
        type=str,
        default='data.csv',
        required=False,
        help='The destination file to save the resulting .csv'
    )
    parser.add_argument(
        '--header',
        action='store_true',
        help='Whether to add headers to the csv'
    )
    args = parser.parse_args()
    combine_data(args)

main()