from crewai import Agent, Crew, LLM, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool


def _search_llm() -> LLM:
    return LLM(
        model="deepseek/deepseek-flash",
        temperature=0.2,
        extra_body={"thinking": {"type": "disabled"}},
    )


def _analysis_llm() -> LLM:
    return LLM(
        model="deepseek/deepseek-flash",
        temperature=0.2,
    )


@CrewBase
class CrossBorderCommerce:
    """跨境电商商业分析 crew。"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def market_scout(self) -> Agent:
        return Agent(
            config=self.agents_config["market_scout"],  # type: ignore[index]
            llm=_search_llm(),
            tools=[SerperDevTool()],
            max_iter=10,
            verbose=True,
        )

    @agent
    def platform_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["platform_analyst"],  # type: ignore[index]
            llm=_search_llm(),
            tools=[SerperDevTool()],
            max_iter=10,
            verbose=True,
        )

    @agent
    def unit_economics_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["unit_economics_analyst"],  # type: ignore[index]
            llm=_analysis_llm(),
            verbose=True,
        )

    @agent
    def decision_maker(self) -> Agent:
        return Agent(
            config=self.agents_config["decision_maker"],  # type: ignore[index]
            llm=_analysis_llm(),
            verbose=True,
        )

    @task
    def scout_opportunities(self) -> Task:
        return Task(
            config=self.tasks_config["scout_opportunities"],  # type: ignore[index]
        )

    @task
    def analyze_platforms(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_platforms"],  # type: ignore[index]
        )

    @task
    def estimate_unit_economics(self) -> Task:
        return Task(
            config=self.tasks_config["estimate_unit_economics"],  # type: ignore[index]
        )

    @task
    def decide_opportunity(self) -> Task:
        return Task(
            config=self.tasks_config["decide_opportunity"],  # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """创建跨境电商商业分析 crew。"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            tracing=True,
        )
