from __future__ import annotations

"""Utility helpers for managing multilingual output."""

from enum import Enum
from typing import Dict, Optional


class Language(str, Enum):
    """Supported output languages for the application."""

    ZH = "zh"
    EN = "en"
    BOTH = "both"

    @classmethod
    def from_value(cls, value: Optional[str]) -> "Language":
        """Convert a string to a :class:`Language`, falling back to Chinese."""

        if not value:
            return cls.ZH
        try:
            return cls(value.lower())  # type: ignore[arg-type]
        except ValueError:
            return cls.ZH


DEFAULT_LANGUAGE: Language = Language.ZH


def combine_translations(zh_text: str, en_text: str, language: Language, joiner: str = " / ") -> str:
    """Return text in the requested language (or both)."""

    if language == Language.ZH:
        return zh_text or en_text
    if language == Language.EN:
        return en_text or zh_text

    # Language.BOTH – merge both but avoid duplicates.
    parts = []
    zh = zh_text.strip()
    en = en_text.strip()
    if zh:
        parts.append(zh)
    if en and en != zh:
        parts.append(en)
    if not parts:
        return en_text or zh_text
    return joiner.join(parts)


TRANSLATIONS: Dict[str, Dict[str, str]] = {
    # CLI prompts & instructions
    "cli.select_analysts": {
        "zh": "选择你的 AI 分析师。",
        "en": "Select your AI analysts.",
    },
    "cli.instructions": {
        "zh": "\n\n操作说明：\n1. 按空格键选择/取消分析师。\n2. 按 'a' 键全选/取消全选。\n3. 按回车键开始运行。\n",
        "en": "\n\nInstructions:\n1. Press Space to select/unselect analysts.\n2. Press 'a' to select/unselect all.\n3. Press Enter to run the hedge fund.\n",
    },
    "cli.select_llm": {
        "zh": "选择你要使用的大模型：",
        "en": "Select your LLM model:",
    },
    "cli.select_ollama_model": {
        "zh": "选择你要使用的 Ollama 本地模型：",
        "en": "Select your Ollama model:",
    },
    "cli.enter_custom_model": {
        "zh": "请输入自定义模型名称：",
        "en": "Enter the custom model name:",
    },
    "cli.interrupt": {
        "zh": "\n\n检测到中断，程序退出……",
        "en": "\n\nInterrupt received. Exiting...",
    },
    "cli.selected_analysts": {
        "zh": "已选择分析师：{names}",
        "en": "Selected analysts: {names}",
    },
    "cli.selected_model": {
        "zh": "已选择 {provider} 模型：{model}",
        "en": "Selected {provider} model: {model}",
    },
    "cli.using_ollama": {
        "zh": "正在使用 Ollama 进行本地推理。",
        "en": "Using Ollama for local LLM inference.",
    },
    "cli.validation.select_one": {
        "zh": "至少选择一位分析师。",
        "en": "You must select at least one analyst.",
    },
    "cli.invalid_start_date": {
        "zh": "开始日期必须是 YYYY-MM-DD 格式",
        "en": "Start date must be in YYYY-MM-DD format",
    },
    "cli.invalid_end_date": {
        "zh": "结束日期必须是 YYYY-MM-DD 格式",
        "en": "End date must be in YYYY-MM-DD format",
    },
    "cli.analysis_for": {
        "zh": "{ticker} 分析",
        "en": "Analysis for {ticker}",
    },
    # Display headers & labels
    "display.analysis_heading": {
        "zh": "分析：{ticker}",
        "en": "Analysis: {ticker}",
    },
    "display.agent_analysis_header": {
        "zh": "代理分析：{ticker}",
        "en": "Agent Analysis: {ticker}",
    },
    "display.trading_decision_header": {
        "zh": "交易决策：{ticker}",
        "en": "Trading Decision: {ticker}",
    },
    "display.portfolio_summary_header": {
        "zh": "投资组合汇总",
        "en": "Portfolio Summary",
    },
    "display.portfolio_strategy_header": {
        "zh": "组合策略说明",
        "en": "Portfolio Strategy",
    },
    "display.no_decisions": {
        "zh": "未生成任何交易决策",
        "en": "No trading decisions available",
    },
    "display.table.agent": {
        "zh": "代理",
        "en": "Agent",
    },
    "display.table.signal": {
        "zh": "信号",
        "en": "Signal",
    },
    "display.table.confidence": {
        "zh": "置信度",
        "en": "Confidence",
    },
    "display.table.reasoning": {
        "zh": "推理",
        "en": "Reasoning",
    },
    "display.table.action": {
        "zh": "操作",
        "en": "Action",
    },
    "display.table.quantity": {
        "zh": "数量",
        "en": "Quantity",
    },
    "display.table.ticker": {
        "zh": "标的",
        "en": "Ticker",
    },
    "display.table.portfolio_confidence": {
        "zh": "置信度",
        "en": "Confidence",
    },
    "display.portfolio_strategy_text": {
        "zh": "{text}",
        "en": "{text}",
    },
    "backtest.prefetch_start": {
        "zh": "\n正在预加载整个回测区间所需的数据……",
        "en": "\nPre-fetching data for the entire backtest period...",
    },
    "backtest.prefetch_complete": {
        "zh": "数据预加载完成。",
        "en": "Data pre-fetch complete.",
    },
    "backtest.start": {
        "zh": "\n开始执行回测……",
        "en": "\nStarting backtest...",
    },
    "backtest.warning.no_price_data": {
        "zh": "警告：{ticker} 在 {date} 没有价格数据",
        "en": "Warning: No price data for {ticker} on {date}",
    },
    "backtest.error.fetch_price_range": {
        "zh": "获取 {ticker} 在 {start} 至 {end} 期间的价格数据时出错：{error}",
        "en": "Error fetching price for {ticker} between {start} and {end}: {error}",
    },
    "backtest.warning.skip_day_missing_data": {
        "zh": "由于缺少价格数据，跳过 {date} 的交易日",
        "en": "Skipping trading day {date} due to missing price data",
    },
    "backtest.error.fetch_prices_day": {
        "zh": "获取 {date} 的价格数据时出错：{error}",
        "en": "Error fetching prices for {date}: {error}",
    },
    "backtest.no_portfolio_data": {
        "zh": "未找到投资组合数据，请先运行回测。",
        "en": "No portfolio data found. Please run the backtest first.",
    },
    "backtest.no_performance_data": {
        "zh": "没有可用于分析的绩效数据。",
        "en": "No valid performance data to analyze.",
    },
    "backtest.performance_summary": {
        "zh": "投资组合绩效摘要",
        "en": "Portfolio Performance Summary",
    },
    "backtest.total_return": {
        "zh": "总收益",
        "en": "Total Return",
    },
    "backtest.total_realized_gains": {
        "zh": "累计已实现盈亏",
        "en": "Total Realized Gains/Losses",
    },
    "backtest.chart.portfolio_value_title": {
        "zh": "投资组合价值随时间变化",
        "en": "Portfolio Value Over Time",
    },
    "backtest.chart.portfolio_value_ylabel": {
        "zh": "投资组合价值 (美元)",
        "en": "Portfolio Value ($)",
    },
    "backtest.chart.portfolio_value_xlabel": {
        "zh": "日期",
        "en": "Date",
    },
    "backtest.sharpe_ratio": {
        "zh": "夏普比率",
        "en": "Sharpe Ratio",
    },
    "backtest.max_drawdown": {
        "zh": "最大回撤：{value}%",
        "en": "Maximum Drawdown: {value}%",
    },
    "backtest.max_drawdown_with_date": {
        "zh": "最大回撤：{value}%（发生于 {date}）",
        "en": "Maximum Drawdown: {value}% (on {date})",
    },
    "backtest.win_rate": {
        "zh": "胜率",
        "en": "Win Rate",
    },
    "backtest.win_loss_ratio": {
        "zh": "盈亏比",
        "en": "Win/Loss Ratio",
    },
    "backtest.max_consecutive_wins": {
        "zh": "最长连续盈利天数",
        "en": "Max Consecutive Wins",
    },
    "backtest.max_consecutive_losses": {
        "zh": "最长连续亏损天数",
        "en": "Max Consecutive Losses",
    },
    "backtest.table.summary_heading": {
        "zh": "投资组合汇总",
        "en": "PORTFOLIO SUMMARY",
    },
    "backtest.table.cash_balance": {
        "zh": "现金余额",
        "en": "Cash Balance",
    },
    "backtest.table.position_value": {
        "zh": "总持仓市值",
        "en": "Total Position Value",
    },
    "backtest.table.total_value": {
        "zh": "资产总值",
        "en": "Total Value",
    },
    "backtest.table.return": {
        "zh": "收益率",
        "en": "Return",
    },
    "backtest.table.sharpe_ratio": {
        "zh": "夏普比率",
        "en": "Sharpe Ratio",
    },
    "backtest.table.sortino_ratio": {
        "zh": "索提诺比率",
        "en": "Sortino Ratio",
    },
    "backtest.table.max_drawdown": {
        "zh": "最大回撤",
        "en": "Max Drawdown",
    },
    "backtest.table.date": {
        "zh": "日期",
        "en": "Date",
    },
    "backtest.table.ticker": {
        "zh": "标的",
        "en": "Ticker",
    },
    "backtest.table.action": {
        "zh": "操作",
        "en": "Action",
    },
    "backtest.table.quantity": {
        "zh": "数量",
        "en": "Quantity",
    },
    "backtest.table.price": {
        "zh": "价格",
        "en": "Price",
    },
    "backtest.table.long_shares": {
        "zh": "多头持股",
        "en": "Long Shares",
    },
    "backtest.table.short_shares": {
        "zh": "空头持股",
        "en": "Short Shares",
    },
    "backtest.table.position_value_column": {
        "zh": "净持仓价值",
        "en": "Position Value",
    },
    "backtest.table.bullish": {
        "zh": "看多",
        "en": "Bullish",
    },
    "backtest.table.bearish": {
        "zh": "看空",
        "en": "Bearish",
    },
    "backtest.table.neutral": {
        "zh": "中性",
        "en": "Neutral",
    },
    "cli.cannot_proceed_ollama": {
        "zh": "无法继续：未检测到 Ollama 或所选模型。",
        "en": "Cannot proceed without Ollama and the selected model.",
    },
    "cli.selected_model_generic": {
        "zh": "\n已选择模型：{model}\n",
        "en": "\nSelected model: {model}\n",
    },
}


STATUS_TRANSLATIONS: Dict[str, str] = {
    "Analyzing Graham valuation": "正在分析格雷厄姆估值",
    "Analyzing activism potential": "正在分析激进投资潜力",
    "Analyzing balance sheet": "正在分析资产负债表",
    "Analyzing balance sheet and capital structure": "正在分析资产负债表与资本结构",
    "Analyzing book value growth": "正在分析账面价值增长",
    "Analyzing business predictability": "正在分析业务可预测性",
    "Analyzing business quality": "正在分析企业质量",
    "Analyzing cash flow": "正在分析现金流",
    "Analyzing cash yield and valuation": "正在分析现金收益率与估值",
    "Analyzing competitive moat": "正在分析竞争护城河",
    "Analyzing consistency": "正在分析盈利稳定性",
    "Analyzing contrarian sentiment": "正在分析逆向情绪",
    "Analyzing disruptive potential": "正在分析颠覆式潜力",
    "Analyzing downside protection": "正在分析下行保护",
    "Analyzing earnings stability": "正在分析盈利稳定性",
    "Analyzing financial health": "正在分析财务健康状况",
    "Analyzing financial strength": "正在分析财务实力",
    "Analyzing fundamentals": "正在分析基本面",
    "Analyzing growth": "正在分析增长情况",
    "Analyzing growth & momentum": "正在分析增长与动量",
    "Analyzing growth & quality": "正在分析增长与质量",
    "Analyzing growth and reinvestment": "正在分析增长与再投资",
    "Analyzing innovation-driven growth": "正在分析创新驱动增长",
    "Analyzing insider activity": "正在分析内部交易行为",
    "Analyzing management actions": "正在分析管理层动作",
    "Analyzing management efficiency & leverage": "正在分析管理效率与杠杆",
    "Analyzing management quality": "正在分析管理质量",
    "Analyzing margins & stability": "正在分析利润率与稳定性",
    "Analyzing moat strength": "正在分析护城河强度",
    "Analyzing price data": "正在分析价格数据",
    "Analyzing pricing power": "正在分析定价能力",
    "Analyzing profitability": "正在分析盈利能力",
    "Analyzing risk profile": "正在分析风险状况",
    "Analyzing risk-reward": "正在分析风险回报",
    "Analyzing sentiment": "正在分析市场情绪",
    "Analyzing trading patterns": "正在分析交易模式",
    "Analyzing valuation (Fisher style)": "正在进行费雪风格估值分析",
    "Analyzing valuation (focus on PEG)": "正在分析估值（重点关注 PEG）",
    "Analyzing valuation ratios": "正在分析估值指标",
    "Analyzing value": "正在分析价值",
    "Analyzing volatility": "正在分析波动率",
    "Assessing potential to double": "正在评估翻倍潜力",
    "Assessing relative valuation": "正在评估相对估值",
    "Calculating Munger-style valuation": "正在计算芒格式估值",
    "Calculating WACC and enhanced DCF": "正在计算加权资本成本与增强 DCF",
    "Calculating final signal": "正在计算最终信号",
    "Calculating intrinsic value": "正在计算内在价值",
    "Calculating intrinsic value & margin of safety": "正在计算内在价值与安全边际",
    "Calculating intrinsic value (DCF)": "正在通过 DCF 计算内在价值",
    "Calculating mean reversion": "正在计算均值回归",
    "Calculating momentum": "正在计算动量指标",
    "Calculating trend signals": "正在计算趋势信号",
    "Calculating valuation & high-growth scenario": "正在估算估值与高增长情景",
    "Calculating volatility- and correlation-adjusted limits": "正在计算波动率与相关性调整限额",
    "Combining signals": "正在综合分析师信号",
    "Done": "完成",
    "Failed: All valuation methods zero": "失败：所有估值方法结果为零",
    "Failed: Insufficient financial line items": "失败：财务科目数据不足",
    "Failed: Market cap unavailable": "失败：未获取到市值数据",
    "Failed: No financial metrics found": "失败：未获取到财务指标",
    "Failed: No price data found": "失败：未获取到价格数据",
    "Failed: No valid price data": "失败：价格数据无效",
    "Fetching company news": "正在获取公司新闻",
    "Fetching financial data": "正在获取财务数据",
    "Fetching financial line items": "正在获取财务科目",
    "Fetching financial metrics": "正在获取财务指标",
    "Fetching insider trades": "正在获取内部交易",
    "Fetching line items": "正在获取科目数据",
    "Fetching market cap": "正在获取市值",
    "Fetching price data and calculating volatility": "正在获取价格并计算波动率",
    "Fetching recent price data for momentum": "正在获取近期价格数据以计算动量",
    "Gathering comprehensive line items": "正在收集完整的财务科目",
    "Gathering financial line items": "正在汇总财务科目",
    "Generating Ben Graham analysis": "正在生成本·格雷厄姆分析",
    "Generating Bill Ackman analysis": "正在生成比尔·阿克曼分析",
    "Generating Cathie Wood analysis": "正在生成凯茜·伍德分析",
    "Generating Charlie Munger analysis": "正在生成查理·芒格分析",
    "Generating Damodaran analysis": "正在生成达莫达兰分析",
    "Generating Jhunjhunwala analysis": "正在生成琼君瓦拉分析",
    "Generating LLM output": "正在生成大模型输出",
    "Generating Pabrai analysis": "正在生成帕布莱分析",
    "Generating Peter Lynch analysis": "正在生成彼得·林奇分析",
    "Generating Phil Fisher-style analysis": "正在生成菲利普·费雪风格分析",
    "Generating Stanley Druckenmiller analysis": "正在生成斯坦利·德鲁肯米勒分析",
    "Generating Warren Buffett analysis": "正在生成沃伦·巴菲特分析",
    "Generating trading decisions": "正在生成交易决策",
    "Getting market cap": "正在获取市值",
    "Performing Druckenmiller-style valuation": "正在执行德鲁肯米勒风格估值",
    "Processing analyst signals": "正在处理分析师信号",
    "Statistical analysis": "正在进行统计分析",
    "Warning: Insufficient price data": "警告：价格数据不足",
    "Warning: No price data found": "警告：未找到价格数据",
}


AGENT_NAME_TRANSLATIONS: Dict[str, str] = {
    "aswath_damodaran": "阿斯瓦斯·达莫达兰",
    "ben_graham": "本·格雷厄姆",
    "bill_ackman": "比尔·阿克曼",
    "cathie_wood": "凯茜·伍德",
    "charlie_munger": "查理·芒格",
    "michael_burry": "迈克尔·伯里",
    "mohnish_pabrai": "莫尼什·帕布莱",
    "peter_lynch": "彼得·林奇",
    "phil_fisher": "菲利普·费雪",
    "rakesh_jhunjhunwala": "拉凯什·琼君瓦拉",
    "stanley_druckenmiller": "斯坦利·德鲁肯米勒",
    "warren_buffett": "沃伦·巴菲特",
    "technical_analyst": "技术分析师",
    "fundamentals_analyst": "基本面分析师",
    "sentiment_analyst": "情绪分析师",
    "valuation_analyst": "估值分析师",
    "risk_management": "风险管理",
    "portfolio_manager": "投资组合经理",
}


SIGNAL_TRANSLATIONS: Dict[str, str] = {
    "BULLISH": "看多",
    "BEARISH": "看空",
    "NEUTRAL": "中性",
}


ACTION_TRANSLATIONS: Dict[str, str] = {
    "BUY": "买入",
    "SELL": "卖出",
    "HOLD": "观望",
    "SHORT": "做空",
    "COVER": "回补",
}


def translate_text(key: str, language: Language, fallback: Optional[str] = None, **kwargs) -> str:
    """Translate a predefined text key."""

    translations = TRANSLATIONS.get(key)
    if not translations:
        base = fallback or ""
        return combine_translations(base, base, language)

    zh_text = translations.get("zh", fallback or "")
    en_text = translations.get("en", fallback or "")
    formatted_zh = zh_text.format(**kwargs)
    formatted_en = en_text.format(**kwargs)
    return combine_translations(formatted_zh, formatted_en, language)


def translate_status(status: str, language: Language) -> str:
    """Translate progress status messages."""

    if language == Language.EN:
        return status
    zh = STATUS_TRANSLATIONS.get(status, status)
    if language == Language.ZH:
        return zh
    return combine_translations(zh, status, Language.BOTH)


def translate_agent_name(agent_key: str, language: Language) -> str:
    """Return localized agent names."""

    base = agent_key.replace("_", " ").title()
    zh = AGENT_NAME_TRANSLATIONS.get(agent_key, base)
    en = base
    return combine_translations(zh, en, language)


def translate_signal(signal: str, language: Language) -> str:
    """Translate signal names."""

    signal_upper = signal.upper()
    zh = SIGNAL_TRANSLATIONS.get(signal_upper, signal_upper)
    en = signal_upper
    return combine_translations(zh, en, language)


def translate_action(action: str, language: Language) -> str:
    """Translate trading actions."""

    action_upper = action.upper()
    zh = ACTION_TRANSLATIONS.get(action_upper, action_upper)
    en = action_upper
    return combine_translations(zh, en, language)


def language_to_metadata(language: Language) -> str:
    """Serialize language to store inside metadata."""

    return language.value
