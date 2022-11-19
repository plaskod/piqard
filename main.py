import argparse
import json
from config_loader.config_loader import ConfigLoader
from utils import directory

if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)

    parser.add_argument("--query", type=str, help="query", required=True)
    parser.add_argument(
        "--config",
        type=str,
        help="query",
        default="./config_loader/configs/config.yaml",
    )
    args = parser.parse_args()

    config_loader = ConfigLoader()
    config = config_loader.load(args.config)

    piqard = config.piqard
    result = piqard(args.query)

    with open(f"{directory(config.result_dir)}/generated_result.txt", "w") as f:
        json.dump(result, f)
    print(result["answer"])
