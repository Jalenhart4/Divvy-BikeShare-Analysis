import pandas as pd
import logging
import os
from scipy import stats


def load_cleaned_data(log):
    """
    Loads the cleaned data from a CSV file.

    Args:
        log (logging.Logger): Logger instance for logging information.

    Returns:
        pd.DataFrame: The loaded and cleaned DataFrame.
    """
    try:
        path = os.path.join('..', 'data', 'processed', 'cleaned_data.csv')
        df = pd.read_csv(path)
        log.info(f"Data loaded successfully from {path}")
        return df
    except Exception as e:
        log.error(f"Error loading data: {e}")
        raise


def descriptive_statistics(df, log):
    """
    Calculates and logs descriptive statistics for specific columns.

    Args:
        df (pd.DataFrame): The DataFrame for which to calculate statistics.
        log (logging.Logger): Logger instance for logging information.
    """
    try:
        log.info("Calculating descriptive statistics...")

        # Separate data into member and casual riders
        member_df = df[df['member_casual'] == 'member']
        casual_df = df[df['member_casual'] == 'casual']

        # Focus on specific columns: 'start_hour', 'month', 'ride_length'
        selected_columns = ['start_hour', 'month', 'ride_length']

        # Calculate descriptive statistics for each group
        members_stats = member_df[selected_columns].describe()
        casual_stats = casual_df[selected_columns].describe()

        # Calculate descriptive statistics for all records
        stats = df[selected_columns].describe()

        print("Descriptive statistics for all records")
        print(stats)
        print('------------------------------------------------------------------')
        print("Descriptive statistics for members")
        print(members_stats)
        print('------------------------------------------------------------------')
        print("Descriptive statistics for casual riders")
        print(casual_stats)
    except Exception as e:
        log.error(f"Error calculating descriptive statistics: {e}")
        raise


def correlation_analysis(df, log):
    """
    Performs a correlation analysis between numerical columns.

    Args:
        df (pd.DataFrame): The DataFrame for which to calculate correlations.
        log (logging.Logger): Logger instance for logging information.
    """
    try:
        log.info("Calculating correlation matrix...")

        # Create Start location and end location columns
        df['start_location_num'] = df['start_lat'] + df['start_lng']
        df['end_location_num'] = df['end_lat'] + df['end_lng']

        # Select only numeric columns for correlation analysis
        selected_columns = ['start_hour', 'month', 'ride_length', 'start_location_num', 'end_location_num']
        numeric_df = df[selected_columns]

        if numeric_df.empty:
            log.warning("No numeric columns available for correlation analysis.")
            return

        # Calculate correlation matrix
        corr_matrix = numeric_df.corr()
        print(corr_matrix)
    except Exception as e:
        log.error(f"Error calculating correlation matrix: {e}")
        raise


def t_test_member_vs_casual(df, log):
    """
    Performs a t-test to compare ride lengths between member and casual riders.

    Args:
        df (pd.DataFrame): The DataFrame containing the data.
        log (logging.Logger): Logger instance for logging information.
    """
    try:
        log.info("Performing t-test between member and casual riders...")

        # Split data into two groups
        member_ride_lengths = df[df['member_casual'] == 'member']['ride_length']
        casual_ride_lengths = df[df['member_casual'] == 'casual']['ride_length']

        # Perform t-test
        t_stat, p_value = stats.ttest_ind(member_ride_lengths, casual_ride_lengths, equal_var=False)

        print(f"T-test results: t-statistic = {t_stat:.4f}, p-value = {p_value:.4f}")
    except Exception as e:
        log.error(f"Error performing t-test: {e}")
        raise


def main():
    # Config
    pd.set_option('display.max_columns', None)
    pd.options.display.float_format = '{:20,.2f}'.format
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()

    # Load the cleaned data
    df = load_cleaned_data(logger)

    # Perform analyses
    descriptive_statistics(df, logger)
    correlation_analysis(df, logger)
    t_test_member_vs_casual(df, logger)


if __name__ == "__main__":
    main()
