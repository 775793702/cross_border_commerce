# 跨境电商商业分析

顺序执行的 CrewAI 选品项目。给定品类和目标市场，选出一个商品机会，并说明其余候选为什么不做。

四个角色都使用 DeepSeek 官方 API 的 `deepseek-flash`。市场侦察和平台分析使用 Serper 搜索。

## 准备

复制 `.env.example` 为 `.env`，填入：

```
DEEPSEEK_API_KEY=
SERPER_API_KEY=
```

## 运行

在本目录执行：

```bash
uv run run_crew
```

直接回车会使用默认品类「宠物自动饮水机」和目标市场「美国 Amazon」。没有交互终端时也使用这两个默认值。

结果写到：

- `output/opportunities.json`
- `output/platform_analysis.json`
- `output/unit_economics.json`
- `output/decision.md`

这是课程练习，决策不能当作经营建议。

课程 CLI 固定 CrewAI 1.14.4。PyPI 上已有更新的版本，本项目仍使用 1.14.4，以便和 `reference/` 的写法一致。
