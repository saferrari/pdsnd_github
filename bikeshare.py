import time
import datetime
import calendar
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    while True: 
        city = input("\nWould you like to see data for Chicago, New York City, or Washington? ")
        city = city.lower()
        if city not in ('chicago', 'new york city', 'washington'):
            print("\nSorry your response was not valid. Please type Chicago, New York City, or Washington")
        else:
            break

    month_day = input("\nWould you like to filter the data by month, day, or not at all? If not at all please type none. ")
    # Checks to see if response if valid, if it is not, the user is asked to type either month, day, or none. Repeats until the user types a valid response.
    while True:
        if month_day.lower() not in ('month', 'day', 'none'):
            print("\nSorry your response was not valid. Pleae type month, day or none")
            month_day = input("\nWould you like to filter the data by month, day, or not at all? If not at all please type none. ")
        else:
            break
        

    # If fitering by month, asks for the month, and checks if the response is valid.              
    if month_day.lower() == 'month': 
        while True:
            month = input("\nWhich month - January, February, March, April, May, or June? ")
            month = month.lower()
            day = 'all'
            if month not in ('january', 'february', 'march', 'april', 'may', 'june'):
                print("\nSorry your response was not valid. Please type January, February, March, April, May or June")
            else:
                break
    # If filtering by day, asks for the day of the week and checks if the response is valid.
    elif month_day.lower() == 'day':
        while True:
            day = input("\nWhich day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? ")
            day = day.title()
            month = 'all'
            if day not in ('Monday', 'Tuesday', 'Wednesday', 'Thursday','Friday', 'Saturday', 'Sunday'):
                print("\nSorry your repsonse was not valid. Please select Monday, Tuesday, Wednesday, Thrusday, Friday, Saturday, or Sunday")
            else:
                break
    # Selects all data if no filter is applied
    elif month_day.lower() == 'none':
        month = 'all'
        day = 'all'
        
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # loads the data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # converts the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extracts the month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # filters by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
        
    if day != 'all':
        # filters by day of week
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    
    INPUT:
      dataframe (df): based on the city, month, and day filter options specified by the user
    
    OUTPUT:
      prints the statistics for most frequent month, weekday and hour of travel 
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # converts the Start Time column to datetime
    popular_month = df['month'].mode()[0]
    print('Most Popular Month is ',calendar.month_name[popular_month])
   
    # extracts  from the Start Time column to create an hour column
    popular_weekday = df['day_of_week'].mode()[0]
    print('Most Popular Weekday is ', popular_weekday)
  
    # extracts hour from the Start Time column to create an hour column and finds the hour that reoccurs the most
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour is', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Displays most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station is ", popular_start_station)

    # Displays most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station is ", popular_end_station)

    # Displays most frequent combination of start station and end station trip
    df['Start End Station'] = df['Start Station'] + " and " + df['End Station']
    popular_start_end_station = df['Start End Station'].mode()[0]
    print("The most frequent combination of start and end station trip is ", popular_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_trip_time = df['Trip Duration'].sum()
    total_trip_time = datetime.timedelta(seconds=int(total_trip_time))
    print("The total trip duration is ", total_trip_time)

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The mean travel time is {} seconds".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # Displays counts of user types
    user_types = df['User Type'].value_counts()
    print("User Type counts:\n", user_types)
  
    # Displays counts of gender
    try:
        gender = df['Gender'].value_counts()
        print("\nGender counts:\n",gender)
    except KeyError:
        print("No gender data exists")
       
    # Displays earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print("\nThe earliest birth year is {}\nThe most recent birth year is {}\nThe most common birth year is {}".format(earliest_birth_year, most_recent_birth_year, most_common_birth_year))
    except KeyError:
        print("No birth year data exists")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def data(df,i,j):
    """
    Prints 5 rows of raw data at a time, until the user tells it to stop

    Args:
        df - reindexed Pandas dataframe containing city data filtered by month and day
        (int) i - starting row number
        (int) j - ending row number  
    """
    raw_data = input('\nWould you like to see 5 lines of raw data? Type yes or no.\n')
    while True:  
        if raw_data.lower() == 'no':
            break
        if raw_data.lower() == 'yes':
            if j > df.shape[0] and i <= df.shape[0]:
                final_lines = df.loc[i:]
                print(final_lines)
                print('\nThere is no more data')
                break
            elif j <= df.shape[0]:
                line = df.loc[i:j]
                print(line)
                i += 5
                j += 5 
                if i >= df.shape[0]:
                    print('\nThere is no more data')
                    break
                raw_data = input('\nWould you like to see 5 more lines of raw data? Type yes or no.\n')
                continue
        if raw_data.lower not in ('yes', 'no'):
            raw_data = input('Sorry your response was not valid. Please type yes or no. ')
            
            
def main():
    
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        # Inputs used for the data fucntion.
        df = df.reset_index(drop=True) #resets the index of df 
        i = 0  # stating row number
        j = 4 # ending row number
        data(df,i,j)
              
        # restarts the propgram if user answers yes.
        restart = input('\nWould you like to restart? Type yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

