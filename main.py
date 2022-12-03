import argparse
import json

from piqard.PIQARD_loader import PIQARDLoader
from utils import directory


if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)

    parser.add_argument("query", type=str, help="query")
    parser.add_argument(
        "--config",
        type=str,
        help="config",
        default="./assets/configs/config.yaml",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="output",
        default="./result",
    )
    args = parser.parse_args()

    piqard_loader = PIQARDLoader()
    piqard = piqard_loader.load(args.config)
    piqard.show_info()

    result = piqard(args.query)

    with open(f"{directory(args.output)}/generated_result.txt", "w") as f:
        json.dump(result, f, indent=4)
    print("== Result")
    print(result["answer"])
