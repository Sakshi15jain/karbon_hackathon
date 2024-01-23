import datetime


class FLAGS:
    GREEN = 1
    AMBER = 2
    RED = 0
    MEDIUM_RISK = 3  # display purpose only
    WHITE = 4  # data is missing for this field

def latest_financial_index(data: dict):
    """
    Determine the index of the latest standalone financial entry in the data.

    This function iterates over the "financials" list in the given data dictionary.
    It returns the index of the first financial entry where the "nature" key is equal to "STANDALONE".
    If no standalone financial entry is found, it returns 0.

    Parameters:
    - data (dict): A dictionary containing a list of financial entries under the "financials" key.

    Returns:
    - int: The index of the latest standalone financial entry or 0 if not found.
    """
    for index, financial in enumerate(data.get("financials")):
        if financial.get("nature") == "STANDALONE":
            return index
    return 0


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


def total_borrowing(data: dict, financial_index):
    """
    Calculate the ratio of total borrowings to total revenue for the financial data at the given index.

    This function sums the long-term and short-term borrowings from the balance sheet ("bs")
    section of the financial data. It then divides this sum by the total revenue, calculated
    by calling the total_revenue function.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for calculation.

    Returns:
    - float: The ratio of total borrowings to total revenue.
    """
    try:
        # Access the financial entry at the given index
        financial_entry = data.get("financials")[financial_index]
        
        # Calculate total borrowings from the balance sheet ("bs") section
        long_term_borrowings = financial_entry.get("bs", {}).get("lineItems", {}).get("longTermBorrowings", 0)
        short_term_borrowings = financial_entry.get("bs", {}).get("lineItems", {}).get("shortTermBorrowings", 0)
        
        total_borrowings = long_term_borrowings + short_term_borrowings
        
        # Calculate the ratio of total borrowings to total revenue
        total_revenue_value = total_revenue(data, financial_index)
        ratio = total_borrowings / total_revenue_value if total_revenue_value != 0 else 0
        
        return ratio
    except (KeyError, ValueError):
        # Handle potential key errors or value conversion errors
        return 0.0


def iscr_flag(data: dict, financial_index):
    """
    Determine the flag color based on the Interest Service Coverage Ratio (ISCR) value.

    This function calculates the ISCR value by calling the iscr function and then assigns a flag color
    based on the ISCR value. If the ISCR value is greater than or equal to 2, it assigns a GREEN flag,
    otherwise, it assigns a RED flag.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the ISCR calculation.

    Returns:
    - FLAGS.GREEN or FLAGS.RED: The flag color based on the ISCR value.
    """
    try:
        # Calculate ISCR value using the iscr function
        iscr_value = iscr(data, financial_index)
        
        # Assign flag color based on ISCR value
        return FLAGS.GREEN if iscr_value >= 2 else FLAGS.RED
    except (KeyError, ValueError):
        # Handle potential key errors or value conversion errors
        return FLAGS.RED


def total_revenue_5cr_flag(data: dict, financial_index):
    """
    Determine the flag color based on whether the total revenue exceeds 50 million.

    This function calculates the total revenue by calling the total_revenue function and then assigns
    a flag color based on the revenue amount. If the total revenue is greater than or equal to 50 million,
    it assigns a GREEN flag, otherwise, it assigns a RED flag.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the revenue calculation.

    Returns:
    - FLAGS.GREEN or FLAGS.RED: The flag color based on the total revenue.
    """
    try:
        # Calculate total revenue using the total_revenue function
        total_revenue_value = total_revenue(data, financial_index)
        
        # Assign flag color based on total revenue
        return FLAGS.GREEN if total_revenue_value >= 50000000 else FLAGS.RED
    except (KeyError, ValueError):
        # Handle potential key errors or value conversion errors
        return FLAGS.RED


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


def borrowing_to_revenue_flag(data: dict, financial_index):
    """
    Determine the flag color based on the ratio of total borrowings to total revenue.

    This function calculates the ratio of total borrowings to total revenue by calling the total_borrowing
    function and then assigns a flag color based on the calculated ratio. If the ratio is less than or equal
    to 0.25, it assigns a GREEN flag, otherwise, it assigns an AMBER flag.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the ratio calculation.

    Returns:
    - FLAGS.GREEN or FLAGS.AMBER: The flag color based on the borrowing to revenue ratio.
    """
    try:
        # Calculate borrowing to revenue ratio using the total_borrowing function
        ratio = total_borrowing(data, financial_index)
        
        # Assign flag color based on the ratio
        return FLAGS.GREEN if ratio <= 0.25 else FLAGS.AMBER
    except (KeyError, ValueError):
        # Handle potential key errors or value conversion errors
        return FLAGS.AMBER