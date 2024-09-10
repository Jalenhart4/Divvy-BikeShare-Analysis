import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Configurations
pd.set_option('display.max_columns', None)
pd.options.display.float_format = '{:20,.2f}'.format
path = os.path.join('..', 'data', 'processed', 'cleaned_data.csv')
df = pd.read_csv(path)

# 1. Ride Length Distribution by Rider Type
plt.figure(figsize=(12, 6))
sns.boxplot(x='member_casual', y='ride_length', data=df)
plt.title('Ride Length Distribution by Rider Type')
plt.xlabel('Rider Type')
plt.ylabel('Ride Length (minutes)')
plt.savefig('../outputs/visualizations/Ride_length_distribution.png')
plt.show()

# 2. Average Ride Length by Time of Day
plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x='start_hour', y='ride_length', hue='member_casual', errorbar=None)
plt.title('Average Ride Length by Time of Day')
plt.xlabel('Hour of Day')
plt.ylabel('Average Ride Length (minutes)')
plt.xticks(range(0, 24))  # Show all hours
plt.savefig('../outputs/visualizations/Average_ride_length_by_hour.png')
plt.show()

# 3. Ride Counts by Time of Day
plt.figure(figsize=(12, 6))
sns.countplot(x='start_hour', hue='member_casual', data=df)
plt.title('Ride Counts by Time of Day')
plt.xlabel('Hour of Day')
plt.ylabel('Number of Rides')
plt.xticks(range(0, 24))  # Show all hours
plt.savefig('../outputs/visualizations/Total_rides_per_hour.png')
plt.show()

# 4. Popular Start Stations by Rider Type (excluding 'Unknown')
df_no_unknown_stations = df[df['start_station_name'] != 'Unknown']

# Calculate the top 10 start stations based on total rides (ignoring 'Unknown')
top_start_stations_total = df_no_unknown_stations['start_station_name'].value_counts().head(10).index

# Filter the DataFrame to include only the top 10 start stations
top_start_stations_df = df_no_unknown_stations[df_no_unknown_stations['start_station_name'].isin(top_start_stations_total)]

# Group by start station and rider type
top_start_stations = top_start_stations_df.groupby(['start_station_name', 'member_casual']).size().unstack(fill_value=0)

# Sort by the total number of rides for casual and member combined
top_start_stations['total'] = top_start_stations['casual'] + top_start_stations['member']
top_start_stations = top_start_stations.sort_values(by='total', ascending=False).drop(columns='total')

# Plot the graph
plt.figure(figsize=(12, 6))
top_start_stations.plot(kind='barh', stacked=True)
plt.title('Top 10 Start Stations by Rider Type (Excluding "Unknown")')
plt.xlabel('Number of Rides')
plt.ylabel('Start Station')
plt.savefig('../outputs/visualizations/Top_ten_start_stations.png')
plt.show()

# 5. Ride Frequency by Day of the Week
plt.figure(figsize=(12, 6))
sns.countplot(x='day_of_week', hue='member_casual', data=df, order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
plt.title('Ride Frequency by Day of the Week')
plt.xlabel('Day of the Week')
plt.ylabel('Number of Rides')
plt.savefig('../outputs/visualizations/Total_rides_by_day_of_week.png')
plt.show()

# 6. Ride time by Day of Week and Hour of day (heatmap)
plt.figure(figsize=(14, 8))
sns.heatmap(df.pivot_table(index='day_of_week', columns='start_hour', values='ride_length', aggfunc='mean').reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']),
            cmap='coolwarm', annot=False)
plt.title('Average Ride Length by Time of Day and Day of Week')
plt.xlabel('Hour of Day')
plt.ylabel('Day of Week')
plt.savefig('../outputs/visualizations/Ride_time_by_day_of_week_and_hour.png')
plt.show()

# 7. Seasonal trends in ride length by member type - use df filtered

plt.figure(figsize=(12, 6))
sns.lineplot(x='season', y='ride_length', hue='member_casual', data=df, errorbar=None, marker='o')
plt.title('Average Ride Length by Season')
plt.xlabel('Season')
plt.ylabel('Average Ride Length (minutes)')
plt.savefig('../outputs/visualizations/Seasonal_ride_time_by_member_type.png')
plt.show()
