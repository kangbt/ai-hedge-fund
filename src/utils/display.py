from colorama import Fore, Style
from tabulate import tabulate

from src.utils.analysts import get_analyst_order_map
from src.utils.language import (
    DEFAULT_LANGUAGE,
    Language,
    translate_action,
    translate_agent_name,
    translate_signal,
    translate_text,
)

import os
import json


def print_trading_output(result: dict, language: Language = DEFAULT_LANGUAGE) -> None:
    """
    Print formatted trading results with colored tables for multiple tickers.

    Args:
        result (dict): Dictionary containing decisions and analyst signals for multiple tickers
    """
    language = Language.from_value(language) if not isinstance(language, Language) else language

    decisions = result.get("decisions")
    if not decisions:
        message = translate_text("display.no_decisions", language, "No trading decisions available")
        print(f"{Fore.RED}{message}{Style.RESET_ALL}")
        return

    analyst_order = get_analyst_order_map()
    analyst_order["risk_management"] = len(analyst_order)

    # Print decisions for each ticker
    for ticker, decision in decisions.items():
        heading = translate_text("display.analysis_heading", language, ticker=ticker)
        print(f"\n{Fore.WHITE}{Style.BRIGHT}{heading}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{Style.BRIGHT}{'=' * 50}{Style.RESET_ALL}")

        # Prepare analyst signals table for this ticker
        table_rows = []
        for agent, signals in result.get("analyst_signals", {}).items():
            if ticker not in signals:
                continue

            # Skip Risk Management agent in the signals section
            if agent == "risk_management_agent":
                continue

            signal = signals[ticker]
            agent_key = agent.replace("_agent", "")
            agent_name = translate_agent_name(agent_key, language)
            signal_type = signal.get("signal", "").upper()
            confidence = signal.get("confidence", 0)

            signal_color = {
                "BULLISH": Fore.GREEN,
                "BEARISH": Fore.RED,
                "NEUTRAL": Fore.YELLOW,
            }.get(signal_type, Fore.WHITE)

            # Get reasoning if available
            reasoning_str = ""
            if "reasoning" in signal and signal["reasoning"]:
                reasoning = signal["reasoning"]

                # Handle different types of reasoning (string, dict, etc.)
                if isinstance(reasoning, str):
                    reasoning_str = reasoning
                elif isinstance(reasoning, dict):
                    # Convert dict to string representation
                    reasoning_str = json.dumps(reasoning, indent=2)
                else:
                    # Convert any other type to string
                    reasoning_str = str(reasoning)

                # Wrap long reasoning text to make it more readable
                wrapped_reasoning = ""
                current_line = ""
                # Use a fixed width of 60 characters to match the table column width
                max_line_length = 60
                for word in reasoning_str.split():
                    if len(current_line) + len(word) + 1 > max_line_length:
                        wrapped_reasoning += current_line + "\n"
                        current_line = word
                    else:
                        if current_line:
                            current_line += " " + word
                        else:
                            current_line = word
                if current_line:
                    wrapped_reasoning += current_line

                reasoning_str = wrapped_reasoning

            table_rows.append(
                [
                    analyst_order.get(agent_key, 999),
                    f"{Fore.CYAN}{agent_name}{Style.RESET_ALL}",
                    f"{signal_color}{translate_signal(signal_type, language)}{Style.RESET_ALL}",
                    f"{Fore.WHITE}{confidence}%{Style.RESET_ALL}",
                    f"{Fore.WHITE}{reasoning_str}{Style.RESET_ALL}",
                ]
            )

        # Sort the signals according to the predefined order
        table_data = [row[1:] for row in sorted(table_rows, key=lambda r: r[0])]

        agent_header = translate_text("display.agent_analysis_header", language, ticker=ticker)
        print(f"\n{Fore.WHITE}{Style.BRIGHT}{agent_header}{Style.RESET_ALL}")
        print(
            tabulate(
                table_data,
                headers=[
                    f"{Fore.WHITE}{translate_text('display.table.agent', language, 'Agent')}",
                    translate_text("display.table.signal", language, "Signal"),
                    translate_text("display.table.confidence", language, "Confidence"),
                    translate_text("display.table.reasoning", language, "Reasoning"),
                ],
                tablefmt="grid",
                colalign=("left", "center", "right", "left"),
            )
        )

        # Print Trading Decision Table
        action = decision.get("action", "").upper()
        action_color = {
            "BUY": Fore.GREEN,
            "SELL": Fore.RED,
            "HOLD": Fore.YELLOW,
            "COVER": Fore.GREEN,
            "SHORT": Fore.RED,
        }.get(action, Fore.WHITE)

        # Get reasoning and format it
        reasoning = decision.get("reasoning", "")
        # Wrap long reasoning text to make it more readable
        wrapped_reasoning = ""
        if reasoning:
            current_line = ""
            # Use a fixed width of 60 characters to match the table column width
            max_line_length = 60
            for word in reasoning.split():
                if len(current_line) + len(word) + 1 > max_line_length:
                    wrapped_reasoning += current_line + "\n"
                    current_line = word
                else:
                    if current_line:
                        current_line += " " + word
                    else:
                        current_line = word
            if current_line:
                wrapped_reasoning += current_line

        decision_data = [
            [
                translate_text("display.table.action", language, "Action"),
                f"{action_color}{translate_action(action, language)}{Style.RESET_ALL}",
            ],
            [
                translate_text("display.table.quantity", language, "Quantity"),
                f"{action_color}{decision.get('quantity')}{Style.RESET_ALL}",
            ],
            [
                translate_text("display.table.confidence", language, "Confidence"),
                f"{Fore.WHITE}{decision.get('confidence'):.1f}%{Style.RESET_ALL}",
            ],
            [
                translate_text("display.table.reasoning", language, "Reasoning"),
                f"{Fore.WHITE}{wrapped_reasoning}{Style.RESET_ALL}",
            ],
        ]

        decision_header = translate_text("display.trading_decision_header", language, ticker=ticker)
        print(f"\n{Fore.WHITE}{Style.BRIGHT}{decision_header}{Style.RESET_ALL}")
        print(tabulate(decision_data, tablefmt="grid", colalign=("left", "left")))

    # Print Portfolio Summary
    portfolio_header = translate_text("display.portfolio_summary_header", language)
    print(f"\n{Fore.WHITE}{Style.BRIGHT}{portfolio_header}{Style.RESET_ALL}")
    portfolio_data = []

    # Extract portfolio manager reasoning (common for all tickers)
    portfolio_manager_reasoning = None
    for ticker, decision in decisions.items():
        if decision.get("reasoning"):
            portfolio_manager_reasoning = decision.get("reasoning")
            break

    for ticker, decision in decisions.items():
        action = decision.get("action", "").upper()
        action_color = {
            "BUY": Fore.GREEN,
            "SELL": Fore.RED,
            "HOLD": Fore.YELLOW,
            "COVER": Fore.GREEN,
            "SHORT": Fore.RED,
        }.get(action, Fore.WHITE)
        portfolio_data.append(
            [
                f"{Fore.CYAN}{ticker}{Style.RESET_ALL}",
                f"{action_color}{translate_action(action, language)}{Style.RESET_ALL}",
                f"{action_color}{decision.get('quantity')}{Style.RESET_ALL}",
                f"{Fore.WHITE}{decision.get('confidence'):.1f}%{Style.RESET_ALL}",
            ]
        )

    headers = [
        f"{Fore.WHITE}{translate_text('display.table.ticker', language, 'Ticker')}",
        translate_text("display.table.action", language, "Action"),
        translate_text("display.table.quantity", language, "Quantity"),
        translate_text("display.table.portfolio_confidence", language, "Confidence"),
    ]

    # Print the portfolio summary table
    print(
        tabulate(
            portfolio_data,
            headers=headers,
            tablefmt="grid",
            colalign=("left", "center", "right", "right"),
        )
    )

    # Print Portfolio Manager's reasoning if available
    if portfolio_manager_reasoning:
        # Handle different types of reasoning (string, dict, etc.)
        reasoning_str = ""
        if isinstance(portfolio_manager_reasoning, str):
            reasoning_str = portfolio_manager_reasoning
        elif isinstance(portfolio_manager_reasoning, dict):
            # Convert dict to string representation
            reasoning_str = json.dumps(portfolio_manager_reasoning, indent=2)
        else:
            # Convert any other type to string
            reasoning_str = str(portfolio_manager_reasoning)

        # Wrap long reasoning text to make it more readable
        wrapped_reasoning = ""
        current_line = ""
        # Use a fixed width of 60 characters to match the table column width
        max_line_length = 60
        for word in reasoning_str.split():
            if len(current_line) + len(word) + 1 > max_line_length:
                wrapped_reasoning += current_line + "\n"
                current_line = word
            else:
                if current_line:
                    current_line += " " + word
                else:
                    current_line = word
        if current_line:
            wrapped_reasoning += current_line

        strategy_header = translate_text("display.portfolio_strategy_header", language)
        print(f"\n{Fore.WHITE}{Style.BRIGHT}{strategy_header}{Style.RESET_ALL}")
        localized_reasoning = translate_text(
            "display.portfolio_strategy_text",
            language,
            text=wrapped_reasoning,
        )
        print(f"{Fore.CYAN}{localized_reasoning}{Style.RESET_ALL}")


def print_backtest_results(table_rows: list, language: Language = DEFAULT_LANGUAGE) -> None:
    """Print the backtest results in a nicely formatted table"""

    language = Language.from_value(language) if not isinstance(language, Language) else language

    # Clear the screen
    os.system("cls" if os.name == "nt" else "clear")

    # Split rows into ticker rows and summary rows
    ticker_rows = []
    summary_rows = []

    summary_heading = translate_text("backtest.table.summary_heading", language, "PORTFOLIO SUMMARY")

    for row in table_rows:
        if isinstance(row[1], str) and summary_heading in row[1]:
            summary_rows.append(row)
        else:
            ticker_rows.append(row)

    # Display latest portfolio summary
    if summary_rows:
        # Pick the most recent summary by date (YYYY-MM-DD)
        latest_summary = max(summary_rows, key=lambda r: r[0])
        print(f"\n{Fore.WHITE}{Style.BRIGHT}{summary_heading}:{Style.RESET_ALL}")

        # Adjusted indexes after adding Long/Short Shares
        position_str = latest_summary[7].split("$")[1].split(Style.RESET_ALL)[0].replace(",", "")
        cash_str = latest_summary[8].split("$")[1].split(Style.RESET_ALL)[0].replace(",", "")
        total_str = latest_summary[9].split("$")[1].split(Style.RESET_ALL)[0].replace(",", "")

        cash_label = translate_text("backtest.table.cash_balance", language, "Cash Balance")
        position_label = translate_text("backtest.table.position_value", language, "Total Position Value")
        total_label = translate_text("backtest.table.total_value", language, "Total Value")
        return_label = translate_text("backtest.table.return", language, "Return")
        sharpe_label = translate_text("backtest.table.sharpe_ratio", language, "Sharpe Ratio")
        sortino_label = translate_text("backtest.table.sortino_ratio", language, "Sortino Ratio")
        max_drawdown_label = translate_text("backtest.table.max_drawdown", language, "Max Drawdown")

        print(f"{cash_label}: {Fore.CYAN}${float(cash_str):,.2f}{Style.RESET_ALL}")
        print(f"{position_label}: {Fore.YELLOW}${float(position_str):,.2f}{Style.RESET_ALL}")
        print(f"{total_label}: {Fore.WHITE}${float(total_str):,.2f}{Style.RESET_ALL}")
        print(f"{return_label}: {latest_summary[10]}")

        # Display performance metrics if available
        if latest_summary[11]:  # Sharpe ratio
            print(f"{sharpe_label}: {latest_summary[11]}")
        if latest_summary[12]:  # Sortino ratio
            print(f"{sortino_label}: {latest_summary[12]}")
        if latest_summary[13]:  # Max drawdown
            print(f"{max_drawdown_label}: {latest_summary[13]}")

    # Add vertical spacing
    print("\n" * 2)

    headers = [
        translate_text("backtest.table.date", language, "Date"),
        translate_text("backtest.table.ticker", language, "Ticker"),
        translate_text("backtest.table.action", language, "Action"),
        translate_text("backtest.table.quantity", language, "Quantity"),
        translate_text("backtest.table.price", language, "Price"),
        translate_text("backtest.table.long_shares", language, "Long Shares"),
        translate_text("backtest.table.short_shares", language, "Short Shares"),
        translate_text("backtest.table.position_value_column", language, "Position Value"),
        translate_text("backtest.table.bullish", language, "Bullish"),
        translate_text("backtest.table.bearish", language, "Bearish"),
        translate_text("backtest.table.neutral", language, "Neutral"),
    ]

    # Print the table with just ticker rows
    print(
        tabulate(
            ticker_rows,
            headers=headers,
            tablefmt="grid",
            colalign=(
                "left",  # Date
                "left",  # Ticker
                "center",  # Action
                "right",  # Quantity
                "right",  # Price
                "right",  # Long Shares
                "right",  # Short Shares
                "right",  # Position Value
                "right",  # Bullish
                "right",  # Bearish
                "right",  # Neutral
            ),
        )
    )

    # Add vertical spacing
    print("\n" * 4)


def format_backtest_row(
    date: str,
    ticker: str,
    action: str,
    quantity: float,
    price: float,
    long_shares: float = 0,
    short_shares: float = 0,
    position_value: float = 0,
    bullish_count: int = 0,
    bearish_count: int = 0,
    neutral_count: int = 0,
    is_summary: bool = False,
    total_value: float = None,
    return_pct: float = None,
    cash_balance: float = None,
    total_position_value: float = None,
    sharpe_ratio: float = None,
    sortino_ratio: float = None,
    max_drawdown: float = None,
    language: Language = DEFAULT_LANGUAGE,
) -> list[any]:
    """Format a row for the backtest results table"""
    language = (
        language if isinstance(language, Language) else Language.from_value(language)
    )

    action_color = {
        "BUY": Fore.GREEN,
        "COVER": Fore.GREEN,
        "SELL": Fore.RED,
        "SHORT": Fore.RED,
        "HOLD": Fore.WHITE,
    }.get(action.upper(), Fore.WHITE)

    if is_summary:
        summary_heading = translate_text(
            "backtest.table.summary_heading", language, "PORTFOLIO SUMMARY"
        )
        return_color = Fore.GREEN if (return_pct or 0) >= 0 else Fore.RED
        return [
            date,
            f"{Fore.WHITE}{Style.BRIGHT}{summary_heading}{Style.RESET_ALL}",
            "",  # Action
            "",  # Quantity
            "",  # Price
            "",  # Long Shares
            "",  # Short Shares
            f"{Fore.YELLOW}${(total_position_value or 0):,.2f}{Style.RESET_ALL}",
            f"{Fore.CYAN}${(cash_balance or 0):,.2f}{Style.RESET_ALL}",
            f"{Fore.WHITE}${(total_value or 0):,.2f}{Style.RESET_ALL}",
            f"{return_color}{(return_pct or 0):+.2f}%{Style.RESET_ALL}",
            (
                f"{Fore.YELLOW}{(sharpe_ratio or 0):.2f}{Style.RESET_ALL}"
                if sharpe_ratio is not None
                else ""
            ),
            (
                f"{Fore.YELLOW}{(sortino_ratio or 0):.2f}{Style.RESET_ALL}"
                if sortino_ratio is not None
                else ""
            ),
            (
                f"{Fore.RED}{abs(max_drawdown or 0):.2f}%{Style.RESET_ALL}"
                if max_drawdown is not None
                else ""
            ),
        ]

    localized_action = translate_action(action.upper(), language)
    return [
        date,
        f"{Fore.CYAN}{ticker}{Style.RESET_ALL}",
        f"{action_color}{localized_action}{Style.RESET_ALL}",
        f"{action_color}{quantity:,.0f}{Style.RESET_ALL}",
        f"{Fore.WHITE}${price:,.2f}{Style.RESET_ALL}",
        f"{Fore.GREEN}{long_shares:,.0f}{Style.RESET_ALL}",
        f"{Fore.RED}{short_shares:,.0f}{Style.RESET_ALL}",
        f"{Fore.YELLOW}${position_value:,.2f}{Style.RESET_ALL}",
        f"{Fore.GREEN}{bullish_count}{Style.RESET_ALL}",
        f"{Fore.RED}{bearish_count}{Style.RESET_ALL}",
        f"{Fore.BLUE}{neutral_count}{Style.RESET_ALL}",
    ]
