import argparse
import json

from piqard.extensions.react.agent_loader import AgentLoader
from utils import directory


if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)

    parser.add_argument("query", type=str, help="query")
    parser.add_argument(
        "--config",
        type=str,
        help="config",
        default="./assets/configs/react_config.yaml",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="output",
        default="./result",
    )
    args = parser.parse_args()

    agent_loader = AgentLoader()
    agent = agent_loader.load(args.config)
    agent.show_info()

    result = agent(args.query)

    with open(f"{directory(args.output)}/generated_react_result.txt", "w") as f:
        json.dump(result, f, indent=4)
    print("== Result")
    print(result["answer"])
