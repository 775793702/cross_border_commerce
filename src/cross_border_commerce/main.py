#!/usr/bin/env python
import os
import sys
import warnings
from datetime import datetime

from cross_border_commerce.crew import CrossBorderCommerce

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

REQUIRED_KEYS = ("DEEPSEEK_API_KEY", "SERPER_API_KEY")
DEFAULT_CATEGORY = "宠物自动饮水机"
DEFAULT_MARKET = "美国 Amazon"


def missing_keys() -> list[str]:
    return [name for name in REQUIRED_KEYS if not os.getenv(name, "").strip()]


def _prompt(label: str, default: str) -> str:
    if not sys.stdin.isatty():
        return default
    entered = input(label).strip()
    return entered or default


def run() -> None:
    """运行跨境电商商业分析 crew。"""
    absent = missing_keys()
    if absent:
        print(f"缺少环境变量: {', '.join(absent)}")
        raise SystemExit(1)

    inputs = {
        "category": _prompt(f"品类 [{DEFAULT_CATEGORY}]: ", DEFAULT_CATEGORY),
        "target_market": _prompt(f"目标市场 [{DEFAULT_MARKET}]: ", DEFAULT_MARKET),
        "current_date": str(datetime.now().date()),
    }
    try:
        CrossBorderCommerce().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}") from e


def train() -> None:
    """训练 crew。"""
    inputs = {
        "category": DEFAULT_CATEGORY,
        "target_market": DEFAULT_MARKET,
        "current_date": str(datetime.now().date()),
    }
    try:
        CrossBorderCommerce().crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}") from e


def replay() -> None:
    """从指定任务重放。"""
    try:
        CrossBorderCommerce().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}") from e


def test() -> None:
    """测试 crew。"""
    inputs = {
        "category": DEFAULT_CATEGORY,
        "target_market": DEFAULT_MARKET,
        "current_date": str(datetime.now().date()),
    }
    try:
        CrossBorderCommerce().crew().test(
            n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}") from e


if __name__ == "__main__":
    run()
