import json
from rule import latest_financial_index, iscr_flag, total_revenue_5cr_flag, iscr, borrowing_to_revenue_flag
import sys
sys.path.append('/path/to/directory/containing/rules')


def total_revenue(data: dict, financial_index):
    """
    Calculate the total revenue from the financial data at the given index.

    This function accesses the "financials" list in the data dictionary at the specified index.
    It then retrieves the net revenue from the "pnl" (Profit and Loss) section under "lineItems".

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for calculation.

    Returns:
    - float: The net revenue value from the financial data.
    """
    try:
        # Access the financial entry at the given index
        financial_entry = data.get("financials")[financial_index]
        
        # Retrieve net revenue from the "pnl" section under "lineItems"
        net_revenue = financial_entry.get("pnl", {}).get("lineItems", {}).get("netRevenue", 0)
        
        return float(net_revenue)
    except (KeyError, ValueError):
        # Handle potential key errors or value conversion errors
        return 0.0


def iscr(data: dict, financial_index):
    """
    Calculate the Interest Service Coverage Ratio (ISCR) for the financial data at the given index.

    ISCR is a ratio that measures how well a company can cover its interest payments on outstanding debt.
    It is calculated as the sum of profit before interest and tax, and depreciation, increased by 1,
    divided by the sum of interest expenses increased by 1. The addition of 1 is to avoid division by zero.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the ISCR calculation.

    Returns:
    - float: The ISCR value.
    """
    try:
        # Access the financial entry at the given index
        financial_entry = data.get("financials")[financial_index]
        
        # Calculate ISCR
        profit_before_interest_and_tax = financial_entry.get("pnl", {}).get("lineItems", {}).get("profitBeforeInterestAndTax", 0)
        depreciation = financial_entry.get("pnl", {}).get("lineItems", {}).get("depreciation", 0)
        interest_expenses = financial_entry.get("pnl", {}).get("lineItems", {}).get("interestExpenses", 0)
        
        iscr_value = (profit_before_interest_and_tax + depreciation + 1) / (interest_expenses + 1)
        
        return iscr_value
    except (KeyError, ValueError):
        # Handle potential key errors or value conversion errors
        return 0.0


def probe_model_5l_profit(data: dict):
    """
    Evaluate various financial flags for the model.

    :param data: A dictionary containing financial data.
    :return: A dictionary with the evaluated flag values.
    """
    lastest_financial_index_value = latest_financial_index(data)

    total_revenue_5cr_flag_value = total_revenue_5cr_flag(
        data, lastest_financial_index_value
    )

    borrowing_to_revenue_flag_value = borrowing_to_revenue_flag(
        data, lastest_financial_index_value
    )

    iscr_flag_value = iscr_flag(data, lastest_financial_index_value)

    return {
        "flags": {
            "TOTAL_REVENUE_5CR_FLAG": total_revenue_5cr_flag_value,
            "BORROWING_TO_REVENUE_FLAG": borrowing_to_revenue_flag_value,
            "ISCR_FLAG": iscr_flag_value,
        }
    }


if __name__ == "__main__":
    with open("data.json", "r") as file:
        content = file.read()
        # convert to json
        data = json.loads(content)
        print(probe_model_5l_profit(data["data"]))