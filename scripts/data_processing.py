import logging
import os
import pandas as pd
import glob
from scipy import stats


def filter_outliers_with_z_score(df, column_name, threshold=3.0, log=None):
    """
    Filters out outliers based on Z-scores.

    Args:
        df (pd.DataFrame): The DataFrame to be filtered.
        column_name (str): The column name on which to compute Z-scores.
        threshold (float): The Z-score threshold to filter out outliers.
        log (logging.Logger): Optional Logger instance for logging information.

    Returns:
        pd.DataFrame: DataFrame with outliers removed.
    """
    try:
        # Compute Z-scores
        z_scores = stats.zscore(df[column_name])

        # Make a copy of the DataFrame to avoid modifying the original
        df_copy = df.copy()

        # Add Z-score column to the copy
        df_copy[column_name + '_z_score'] = z_scores

        # Filter based on Z-scores
        filtered_df = df_copy[abs(df_copy[column_name + '_z_score']) <= threshold].copy()

        if log:
            log.info(f"Filtered out {len(df) - len(filtered_df)} outliers based on Z-scores.")

        return filtered_df
    except Exception as e:
        if log:
            log.error(f"Error during Z-score filtering: {e}")
        raise


def filter_outliers_with_iqr(df, column_name, log=None):
    """
    Filters out outliers based on the IQR method.
    Drops Z score column from filtered dataframe when finished.

    Args:
        df (pd.DataFrame): The DataFrame to be filtered.
        column_name (str): The column name on which to compute the IQR.
        log (logging.Logger): Optional Logger instance for logging information.

    Returns:
        pd.DataFrame: DataFrame with outliers removed.
    """
    try:
        q1 = df[column_name].quantile(0.25)
        q3 = df[column_name].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        filtered_df = df[(df[column_name] >= lower_bound) & (df[column_name] <= upper_bound)].copy()

        if log:
            log.info(f"Filtered out {len(df) - len(filtered_df)} outliers based on IQR.")

        filtered_df.drop(columns=[column_name], inplace=True)
        return filtered_df
    except Exception as e:
        if log:
            log.error(f"Error during IQR filtering: {e}")
        raise


def calculate_ride_length(df, log):
    """
    Calculates the ride length in minutes, adds it as a new column to the DataFrame,
    and removes any rows with negative or zero ride lengths.

    Args:
        df (pd.DataFrame): The cleaned DataFrame with 'started_at' and 'ended_at' columns.
        log (logging.Logger): Logger instance for logging information.

    Returns:
        df (pd.DataFrame): The DataFrame with the new 'ride_length' column.
    """
    try:
        # Calculate ride lengths in minutes and round to 2 decimal points
        df['ride_length'] = (df['ended_at'] - df['started_at']).dt.total_seconds() / 60
        df['ride_length'] = df['ride_length'].round(2)

        # Count negative or zero ride lengths before filtering
        negative_count = (df['ride_length'] <= 0).sum()

        # Log the count of negative/invalid rides
        if log and negative_count > 0:
            log.info(f"Filtered out {negative_count} rides with negative or zero ride lengths.")

        # Filter out rows with negative or zero ride lengths
        df = df[df['ride_length'] > 0]

        return df

    except Exception as e:
        log.error(f"Error calculating ride lengths: {e}")
        raise


def load_data(log):
    """
        Retrieves and Cleans the input DataFrame by removing duplicates, handling missing values,
        converting date columns to datetime, and converting specified columns to categorical.

        Args:
        log (logging.Logger): Logger instance for logging information.

        Returns:
        data_combined (pd.DataFrame): The cleaned DataFrame.
    """
    try:
        path = os.path.join('..', 'data', 'raw', '*.csv')
        csv_files = glob.glob(path)
        data_list = [pd.read_csv(file) for file in csv_files]
        data_combined = pd.concat(data_list, ignore_index=True)
        log.info('Data loaded successfully!')
        return data_combined
    except Exception as e:
        log.error(f"Error loading data {e}!")
        raise


def clean_data(df, log):
    """
        Cleans the input DataFrame by removing duplicates, handling missing values,
        converting date columns to datetime, and converting specified columns to categorical.

        Args:
            df (pd.DataFrame): The raw DataFrame to be cleaned.
            log (logging.Logger): Logger instance for logging information.

        Returns:
            df (pd.DataFrame): The cleaned DataFrame.
    """
    df.info(max_cols=None, show_counts=True)
    # Columns with missing values:
    # start_station_name - category
    # start_station_id - object
    # end_station_name - category
    # end_station_id - object
    # end_lat - float64
    # end_lng - float64

    categorical_columns = [
        "start_station_name",
        "end_station_name",
        "rideable_type",
        "member_casual"
    ]

    for col in categorical_columns:
        df[col] = pd.Categorical(df[col])
        log.info(f"Converted {col} column to category data type.")

    df['started_at'] = pd.to_datetime(df['started_at'])
    df['ended_at'] = pd.to_datetime(df['ended_at'])
    log.info('Converted started_at & ended_at columns to datetime type.')

    # Extract the hour and day of the week from 'started_at'
    df['start_hour'] = df['started_at'].dt.hour
    df['day_of_week'] = df['started_at'].dt.day_name()
    df['month'] = df['started_at'].dt.month
    log.info('Extracted start_hour, day_of_week, and month columns from started_at column')

    # Extract and calculate season based on month column
    df['season'] = df['month'].apply(lambda x: 'Winter' if x in [12, 1, 2]
    else 'Spring' if x in [3, 4, 5]
    else 'Summer' if x in [6, 7, 8]
    else 'Fall')

    # Impute missing values for categorical, id, and name columns with 'Unknown'
    df['start_station_name'] = df['start_station_name'].cat.add_categories(['Unknown'])
    df['end_station_name'] = df['end_station_name'].cat.add_categories(['Unknown'])
    df['start_station_name'] = df['start_station_name'].fillna('Unknown')
    df['end_station_name'] = df['end_station_name'].fillna('Unknown')
    df['start_station_id'] = df['start_station_id'].fillna('Unknown')
    df['end_station_id'] = df['end_station_id'].fillna('Unknown')
    log.info('Added "Unknown" to missing values.')

    # Impute missing values for numerical columns with 0.0
    df.fillna({'end_lat': 0.0, 'end_lng': 0.0}, inplace=True)
    log.info("Added a default end_lat & end_lng of 0.0 for missing values.")

    df.drop_duplicates(inplace=True, keep="first")
    log.info("Dropped duplicate values.")
    log.info('Data Cleaned Successfully!')
    return df


def save_data(df, log):
    """
        Saves the cleaned DataFrame to a CSV file if it doesn't already exist.

        Args:
            df (pd.DataFrame): The cleaned DataFrame to be saved.
            log (logging.Logger): Logger instance for logging information.
    """
    output_file_path = os.path.join('..', 'data', 'processed', 'cleaned_data.csv')
    try:
        if os.path.exists(output_file_path):
            log.info('This file has already been saved')
        else:
            df.to_csv(output_file_path, index=False)
            log.info(f'Data saved to {output_file_path}')
    except Exception as e:
        log.error(f"Error saving data: {e}")


def main():
    # Config
    pd.options.display.float_format = '{:20,.2f}'.format
    pd.set_option('display.max_columns', None)
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()

    # Data Processing
    loaded_data = load_data(logger)
    cleaned_data = clean_data(loaded_data, logger)
    cleaned_data_with_ride_length = calculate_ride_length(cleaned_data, logger)
    cleaned_and_filtered_data = filter_outliers_with_z_score(cleaned_data_with_ride_length, 'ride_length', log=logger)
    final_df = filter_outliers_with_iqr(cleaned_and_filtered_data, 'ride_length_z_score', log=logger)

    # Save processed data to csv file
    save_data(final_df, logger)


if __name__ == "__main__":
    main()
