import time
import pandas as pd
import numpy as np

# This project asks the user to specify the city they would like to see statitics aboutfor the bike rental service
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Which city would you like to to analyze the data for? chicago, new york, or washington? Please select one ')
    while city not in(CITY_DATA.keys()):
        print('You have provided an invalid city name')
        city = input('Which city would you like to to analyze the data for? chicago, new york, or washington? Please select one ').lower()
    # get user input for filter type (month, day or both).
    filter = input('Please select the filter of the data you would like to analyze - by month, day or both? ').lower()
    while filter not in(['month', 'day', 'both']):
        print('You have provided an invalid filter input')
        filter = input('Please select the filter of the data you would like to analyze - by month, day or both? ').lower()
    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    if filter == 'month' or filter == 'both':
        month  = input('Please select the month would you like to analyze the data for - January, February, March, April, May, or June? \n').lower()
        while month not in months:
            print('You provided an invalid month input')
            month = input('Please select the month would you like to analyze the data for - January, February, March, April, May, or June? \n').lower()
    else:
        month = 'all'

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    if filter == 'day' or filter == 'both':
        day = input('Which day would you like to analyze the data for? please select - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? ').title()
        while day not in days:
            print('You have entered an incorrect day input')
            day = input('Which day would you like to analyze the data for? please select - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? ').title()
    else:
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print("Displaying the most common month: ", df['month'].mode()[0], "\n")

    # display the most common day of week
    print("Displaying the most common day of week: ", df['day_of_week'].mode()[0], "\n")
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print(f'The most common start hour is: {most_common_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f'The most common start station is: {common_start_station}')

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f'The most common end station is: {common_end_station}')

    # display most frequent combination of start station and end station trip
    popular_trip = df['Start Station'] + ' to ' + df['End Station']
    print(f'The most frequent combination of trips is: from {popular_trip.mode()[0]}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    from datetime import timedelta as td
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time - we need the proper conversions to break it down into different units
    total_travel_duration = (pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])).sum()
    days =  total_travel_duration.days
    hours = total_travel_duration.seconds // (60*60)
    minutes = total_travel_duration.seconds % (60*60) // 60
    seconds = total_travel_duration.seconds % (60*60) % 60
    print(f'Total travel time is: {days} days {hours} hours {minutes} minutes {seconds} seconds in this city')

    # display mean travel time
    average_travel_time = (pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])).mean()
    days =  average_travel_time.days
    hours = average_travel_time.seconds // (60*60)
    minutes = average_travel_time.seconds % (60*60) // 60
    seconds = average_travel_time.seconds % (60*60) % 60
    print(f'Mean travel time is: {days} days {hours} hours {minutes} minutes {seconds} seconds in this city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts())
    print('\n\n')

    # Display counts of gender
    if 'Gender' in(df.columns):
        print(df['Gender'].value_counts())
        print('\n\n')


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in(df.columns):
        year = df['Birth Year'].fillna(0).astype('int64')
        print(f'Earliest birth year is: {year.min()}\n most recent is: {year.max()}\n and most comon birth year is: {year.mode()[0]}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Ask the user if he wants to showcase raw data/ print 5 rows at time"""
    raw_data = input(' What about showcasing the next 5 raws of data? Please type yes or no ')
    if raw_data.lower() == 'yes':
        count = 0
        while True:
            print(df.iloc[count: count+5])
            count += 5
            ask = input('What about the next 5 raws? Please type yes or no \n')
            if ask.lower() != 'yes':
                break
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
