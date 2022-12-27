import argparse
import json

from piqard.extensions.self_ask.self_ask_loader import SelfAskLoader
from utils import directory


if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)

    parser.add_argument("query", type=str, help="query")
    parser.add_argument(
        "--config",
        type=str,
        help="config",
        default="./assets/configs/self_ask_config_piqard_piqard.yaml",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="output",
        default="./result",
    )
    args = parser.parse_args()

    self_ask_loader = SelfAskLoader()
    self_ask = self_ask_loader.load(args.config)
    self_ask.show_info()

    result = self_ask(args.query)

    with open(f"{directory(args.output)}/generated_self_ask_result.txt", "w") as f:
        json.dump(result, f, indent=4)
    print("== Result")
    print(result["answer"])
