# Divvy-BikeShare-Analysis
This case study was completed as part of the Google Data Analytics certificate program to showcase proficiency in the data analysis process. The focus of this project is on the Divvy bike-share program in Chicago, IL, analyzing data collected throughout 2023.
## Project Goals
The primary goal of this analysis is to understand how casual riders and members differ in their bike usage patterns. Specifically, the analysis aims to: 
- **Compare Ride Behaviors**: Examine differences in ride lengths, frequencies, and times between casual riders and members. 
-  **Identify Usage Trends**: Analyze patterns in bike usage across various times of day, days of the week, and seasons to determine how each group’s behavior varies. 
-  **Inform Business Decisions**: Provide insights that can help optimize bike-share operations and marketing strategies by understanding the distinct needs and preferences of casual riders versus members. 
## Project Overview 
The analysis involves: 
-  **Data Acquisition**: Gathering detailed ride data from the Cyclistic bike-share program. 
-  **Data Preparation**: Cleaning and processing the data to ensure it is ready for meaningful analysis. 
-  **Data Analysis**: Identifying and comparing usage patterns and trends between casual riders and members. 
-  **Data Visualization**: Using Power BI to create interactive visualizations that effectively communicate insights and support data-driven decision-making. 
## Data Acquisition and Preparation

### Data Acquisition

The data for this analysis was obtained from the Cyclistic bike-share program. It includes detailed information on individual rides such as start and end times, starting and ending stations, rideable type (e.g., electric or classic bike), and rider type (either casual or member). The dataset spans from January 2023 to December 2023. You can access the monthly data in csv format here:
- [Index of bucket "divvy-tripdata"](https://divvy-tripdata.s3.amazonaws.com/index.html)

### Data Preparation

The data preparation process involved multiple steps to ensure the dataset was clean, consistent, and ready for analysis:

1. **Data Loading**:
    - All available CSV files containing ride data were loaded and concatenated into a single DataFrame using Python's Pandas library.
    - A logger was used to track the success or failure of the data loading process.

2. **Data Cleaning**:
    - **Handling Missing Values**: Missing values in categorical columns like station names and IDs were imputed with "Unknown," while missing values in numerical columns (latitude and longitude) were filled with 0.0.
    - **Data Type Conversion**: Key columns were converted to appropriate data types:
        - `started_at` and `ended_at` columns were converted to `datetime` format.
        - Categorical columns like `rideable_type`, `member_casual`, `start_station_name`, and `end_station_name` were converted to categorical data types.
    - **Duplicate Removal**: Duplicate entries were identified and removed to ensure that each ride was unique.

3. **Feature Engineering**:
    - **Ride Length Calculation**: A new column `ride_length` was added, calculated as the difference between `ended_at` and `started_at`, and expressed in minutes. Rides with negative or zero lengths were filtered out.
    - **Outlier Detection and Removal**: Outliers in the `ride_length` column were identified and removed using the Z-score method. Rides with a Z-score above or below a threshold of 3 were considered outliers and excluded from the dataset.
    - Extracted additional features: `start_hour` and `day_of_week` from `started_at`. 

4. **Data Saving**:
    - The cleaned and processed data was saved as a new CSV file to ensure it was ready for analysis. If the file already existed, the system logged that it was already saved to avoid overwriting.
    
### Tools Used

- **Python**: Data loading, cleaning, and processing were performed using Python, with the Pandas library handling the bulk of the operations.
- **SciPy**: Used for statistical operations, including the calculation of Z-scores for outlier detection.
- **Logging**: The Python `logging` module was used to track each step of the data preparation process, ensuring that issues could be traced and resolved.
- **Power BI**: For creating interactive and detailed visualizations from the cleaned data.

## Data Analysis 
After preparing the data, several analyses were performed to gain insights into bike-share usage patterns. The following steps detail the analysis process and includes visualizations created during the exploratory phase of the data analysis process. These visualizations help to uncover initial insights and patterns in the data, providing a foundation for more detailed analysis and final presentations.

**Data Loading and Configuration**: 
	- Loaded the cleaned data from a CSV file using Pandas. 
### Descriptive Statistics 
#### General Observations 
- **Ride Length**: 
	- Casual riders have a higher average ride length (12.05 minutes) compared to members (10.07 minutes). This indicates that casual riders tend to use the bikes for longer durations. 
- **Start Hour**: 
	- Casual riders start their rides slightly later in the day (mean start hour: 14.42) compared to members (mean start hour: 13.91). This may suggest different usage patterns between the two groups. 
- **Month**: 
	- There are minimal differences in the month of usage between casual riders and members, with averages being close (casual: 7.05, members: 6.96). 

#### Correlation Matrix Insights 
- **Ride Length Correlations**: 
	- Weak positive correlations exist between ride length and start hour (0.05) and start location number (0.06), indicating minor relationships between these variables. 
- **Location Numbers**: 
	- Start and end location numbers have a moderate correlation (0.11), suggesting some relationship between the start and end locations. 
#### T-Test Results 
- **T-statistic**: -283.4034
- **P-value**: 0.0000
### Exploratory Visualizations 
Before creating the final visualizations in Power BI, I performed an Exploratory Data Analysis (EDA) using Python. This involved generating various plots and charts to better understand the data's structure, distribution, and key patterns. These Python visualizations were instrumental in guiding the development of the more refined and interactive visualizations in Power BI. The insights gained from the EDA served as the foundation for the final analysis and recommendations.
- **Ride Length Distribution by Rider Type**: Boxplot showing distribution of ride lengths. 
- **Average Ride Length by Time of Day**: Line plot of average ride length by hour. 
- **Ride Counts by Time of Day**: Count plot illustrating ride frequencies. 
- **Popular Start Stations by Rider Type**: Bar chart of top start stations. 
- **Ride Frequency by Day of the Week**: Count plot by day of the week. 
- **Ride Time by Day of Week and Hour of Day**: Heatmap of average ride length. 
- **Seasonal Trends in Ride Length**: Line plot of ride length by season.

## Data interpretations and Insights

### Understanding Rider Behavior

After cleaning the data and performing exploratory data analysis, several patterns emerged that differentiate casual riders from members. This section delves into the key findings, offering insights that could inform strategic decisions for the bike-share program.

### Key Insights

1. **Ride Duration**: Casual riders tend to have longer ride durations compared to members. This suggests that casual riders may use the service more for leisure or exploration, whereas members might use it for commuting or shorter trips.

2. **Popular Times and Days**: Members predominantly use the service during weekdays, especially during rush hours, which aligns with a commuting pattern. Casual riders, on the other hand, show higher activity on weekends and holidays, indicating a preference for recreational use.

3. **Preferred Routes and Stations**: Members often frequent routes and stations that connect with business districts and residential areas, further supporting the commuting hypothesis. Casual riders, however, favor routes near tourist attractions and parks.


### Recommendations for Stakeholders
These findings indicate that the bike-share program could be enhanced through targeted strategies. For instance:

1.  **Marketing Department**: Develop promotional offers or seasonal packages targeting casual riders during weekends, holidays, and peak seasons. For example, consider introducing a **"Summer Pass"** that offers discounts for multiple rides during the summer months, capitalizing on the increased recreational usage.
    
2.  **Operations Team**: Optimize station availability in business districts during weekday rush hours to better serve members. Consider expanding or relocating stations near tourist attractions to accommodate the higher demand from casual riders.
    
3.  **Product Development**: Introduce features in the app that cater to both user types. For members, consider offering ride incentives or loyalty rewards for frequent commuting. For casual riders, provide curated ride experiences or route suggestions that highlight popular recreational areas.

By implementing these strategies, the bike-share program can better cater to the distinct needs of casual riders and members, ultimately improving overall satisfaction, increasing usage, and driving growth.


## Data Visualization 
After completing the initial analysis in Python, I used Power BI to create interactive and detailed visualizations. These visualizations offer a comprehensive view of the data, making it easier to identify patterns and insights. 

### Power BI Visualizations 
- **Seasonal Ridership Trends**: 
	- Description: This line chart compares the number of rides taken by casual riders and members across different seasons. The chart reveals that most rides, for both casual and member riders, occur during warmer seasons—spring, summer, and fall—with summer being the most popular. About a third of all rides in these warm seasons are from casual riders, while a higher proportion of winter rides come from members, indicating that members are more likely to ride year-round.
		 - ![Seasonal Ridership Trends](https://github.com/Jalenhart4/Divvy-BikeShare-Analysis/blob/main/visualizations/power%20BI/Total_Rides_Per_Season.PNG) 
- **Ride Frequency and Average Ride Time by Day of Week**: 
	- Description: This bar chart breaks down the number of rides taken by casual riders and members on each day of the week. The data shows that member ridership peaks during the weekdays and tapers off on the weekends, while casual ridership does the opposite, peaking on Saturday. Interestingly, as the number of rides increases for members, their average ride time decreases. For casual riders, both the number of rides and the average ride time increase on the weekends, supporting the idea that casual riders use the service more for leisure.
		 - ![Ride Frequency and Average Ride Time by Day of Wee](https://github.com/Jalenhart4/Divvy-BikeShare-Analysis/blob/main/visualizations/power%20BI/Ride_Frequency_and_Average_Ride_Time_by_Day_of_Week.PNG) 
- **Total Rides Per Hour**: 
	- Description: This line chart illustrates the number of rides taken by casual riders and members at different hours of the day. Member ridership peaks sharply at 8 AM and again at 5 PM, suggesting that members use the service primarily for commuting to and from work. Casual ridership, on the other hand, gradually increases throughout the day, peaking at 5 PM, which suggests a more leisurely use of the service during the most active parts of the day.
		 - ![Total Rides Per Hour](https://github.com/Jalenhart4/Divvy-BikeShare-Analysis/blob/main/visualizations/power%20BI/Total_Rides_Per_Hour.PNG) 
- **Average Ride Length by Time of Day**: 
	- Description: This line chart compares the average ride length by time of day for casual riders and members. The average ride length for members remains consistent throughout the day and night, whereas for casual riders, ride length is shorter in the early morning, drastically increases around 9 AM, peaks at 11 AM, and then gradually decreases for the rest of the day. This further supports the idea that casual riders are using the service for recreational purposes.
		 - ![Average Ride Length by Time of Day](https://github.com/Jalenhart4/Divvy-BikeShare-Analysis/blob/main/visualizations/power%20BI/Average_Ride_Length_By_Start_Hour.PNG) 
- **Average Ride Length by Day of Week and Start Hour**:
	- Description: This heatmap shows average ride lengths by both the hour of the day and the day of the week. It reveals that shorter rides generally occur in the early morning hours (4-9 AM) during weekdays, while the longest rides are typically during the weekends, peaking at the most active times. With casual ridership spiking on the weekends, there's a clear correlation between an increase in casual riders and longer ride times, further reinforcing the idea that casual riders use the service for recreation.
		- ![Average Ride Length by Time of Day and Start Hour](https://github.com/Jalenhart4/Divvy-BikeShare-Analysis/blob/main/visualizations/power%20BI/Average_Ride_Length_By_Day_Of_Week_And_Start_Hour.PNG) 
- **Bike Type Preferences**: 
	- Description: This chart highlights the preferences between classic bikes and electric bikes among casual riders and members. Members use both classic and electric bikes evenly. Casual riders, however, show a slight preference for electric bikes, using them about 1.25 times more often than classic bikes. This adds to the observation that casual riders tend to favor the convenience and fun of electric bikes for their recreational rides.
		- ![Bike Type Preferences by Rider Type](https://github.com/Jalenhart4/Divvy-BikeShare-Analysis/blob/main/visualizations/power%20BI/Bike_Type_Preferences.PNG)
- **Top Starting Stations**: 
	- Description: This horizontal bar chart displays the top 10 starting stations used by both casual riders and members. The top four starting stations are dominated by casual riders, while the remaining stations are mainly used by members, with one exception. This suggests that casual riders prefer specific locations for recreational activities, while members are more evenly distributed across stations, likely using the service for commuting.
		- ![Top Starting Stations](https://github.com/Jalenhart4/Divvy-BikeShare-Analysis/blob/main/visualizations/power%20BI/Top_Ten_Starting_Stations.PNG) 
- **Map of Top 10 Starting Stations**: 
	- Description: This map provides a geographical representation of the top 10 starting stations for both casual riders and members. The stations near lakes are predominantly used by casual riders, with significantly longer average ride lengths for this group. On the other hand, stations near business areas are primarily used by members. This visualization supports the idea that casual riders use the service for recreation, while members primarily use it for commuting purposes.
		- ![Map of Top 10 Starting Stations](https://github.com/Jalenhart4/Divvy-BikeShare-Analysis/blob/main/visualizations/power%20BI/Map_of_Top_Ten_Starting_Stations.PNG)


