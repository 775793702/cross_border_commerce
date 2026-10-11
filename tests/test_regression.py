import ast
import os
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "cross_border_commerce"
CONFIG = SRC / "config"


def _function_names(tree: ast.AST, decorator_name: str) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        for decorator in node.decorator_list:
            target = decorator.func if isinstance(decorator, ast.Call) else decorator
            if isinstance(target, ast.Name) and target.id == decorator_name:
                names.add(node.name)
    return names


def test_yaml_keys_match_crew_methods() -> None:
    crew_source = (SRC / "crew.py").read_text(encoding="utf-8")
    tree = ast.parse(crew_source)
    agents = _function_names(tree, "agent")
    tasks = _function_names(tree, "task")
    agent_yaml = yaml.safe_load((CONFIG / "agents.yaml").read_text(encoding="utf-8"))
    task_yaml = yaml.safe_load((CONFIG / "tasks.yaml").read_text(encoding="utf-8"))
    assert set(agent_yaml) == agents
    assert set(task_yaml) == tasks


def test_tasks_declare_expected_files_and_context() -> None:
    task_yaml = yaml.safe_load((CONFIG / "tasks.yaml").read_text(encoding="utf-8"))
    assert task_yaml["scout_opportunities"]["output_file"] == "output/opportunities.json"
    assert task_yaml["analyze_platforms"]["context"] == ["scout_opportunities"]
    assert task_yaml["analyze_platforms"]["output_file"] == "output/platform_analysis.json"
    assert task_yaml["estimate_unit_economics"]["context"] == ["analyze_platforms"]
    assert task_yaml["estimate_unit_economics"]["output_file"] == "output/unit_economics.json"
    assert task_yaml["decide_opportunity"]["context"] == [
        "scout_opportunities",
        "analyze_platforms",
        "estimate_unit_economics",
    ]
    assert task_yaml["decide_opportunity"]["output_file"] == "output/decision.md"


def test_crew_instantiates_without_kickoff() -> None:
    os.environ["DEEPSEEK_API_KEY"] = "test-key"
    os.environ["SERPER_API_KEY"] = "test-key"
    from crewai import Process

    from cross_border_commerce.crew import CrossBorderCommerce

    built = CrossBorderCommerce().crew()
    assert len(built.agents) == 4
    assert len(built.tasks) == 4
    assert built.process == Process.sequential

    search_agents = []
    analysis_agents = []
    for agent in built.agents:
        assert agent.llm.model == "deepseek-flash"
        assert agent.llm.provider == "deepseek"
        assert agent.llm.base_url == "https://api.deepseek.com/v1"
        assert agent.llm.temperature == 0.2
        if agent.max_iter == 10:
            search_agents.append(agent)
            assert agent.tools
            assert agent.llm.additional_params["extra_body"] == {
                "thinking": {"type": "disabled"}
            }
        else:
            analysis_agents.append(agent)
            assert not agent.tools
            assert "extra_body" not in agent.llm.additional_params
    assert len(search_agents) == 2
    assert len(analysis_agents) == 2

    output_files = [task.output_file for task in built.tasks]
    assert output_files == [
        "output/opportunities.json",
        "output/platform_analysis.json",
        "output/unit_economics.json",
        "output/decision.md",
    ]


def test_missing_keys_exit_before_kickoff() -> None:
    env = os.environ.copy()
    env.pop("DEEPSEEK_API_KEY", None)
    env.pop("SERPER_API_KEY", None)
    script = (
        "from cross_border_commerce.main import missing_keys, run\n"
        "import os\n"
        "os.environ.pop('DEEPSEEK_API_KEY', None)\n"
        "os.environ.pop('SERPER_API_KEY', None)\n"
        "try:\n"
        "    run()\n"
        "except SystemExit as exc:\n"
        "    raise SystemExit(exc.code)\n"
    )
    completed = subprocess.run(
        [sys.executable, "-c", script],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 1, completed.stderr
    assert "DEEPSEEK_API_KEY" in completed.stdout
    assert "SERPER_API_KEY" in completed.stdout


if __name__ == "__main__":
    test_yaml_keys_match_crew_methods()
    test_tasks_declare_expected_files_and_context()
    test_missing_keys_exit_before_kickoff()
    test_crew_instantiates_without_kickoff()
    print("regression checks passed")
