import argparse
import configparser
from arc.arc import ARC


def parse_args():
    parser = argparse.ArgumentParser(description='ARC')
    parser.add_argument(
        '--path', type=str, default='./dataset/ARC-V1-Feb2018/ARC-Challenge/ARC-Challenge-Test.jsonl')
    parser.add_argument('--num_rows', type=int, default=20)
    parser.add_argument('--cuda_device', type=int, default=-1)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    config = configparser.ConfigParser()
    config.read('./arc/conf/arc_configuration.conf')
    arc = ARC(config, args.cuda_device)

    accuracy = arc.analyse_dataset(args.path, args.num_rows)

    print("Reported accuracy = " + str(accuracy))
