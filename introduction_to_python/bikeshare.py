#------------------------------------------------------ 
# Created By: KJN
# Created Date:  26/05/2022
# version: 0.1
# Title: Bikeshare_Project
# -----------------------------------------------------
import os
from time import sleep
import time
import pandas as pd
import numpy as np
pd.set_option('display.expand_frame_repr', False)

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def screen_clear():
    """
    Allows Clearing Of Users Screen, For A Better User Experience.
    """
    if os.name == 'posix':
       _ = os.system('clear')
    else:
       _ = os.system('cls')

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    screen_clear()
    print ('\nHello! & Welcome To The KJN Python Bike Share Project\n')
    sleep(2)
    screen_clear()
    print ('\nLet\'s explore some US bikeshare data Together!\n')
    sleep(3)

    screen_clear()
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Which City From The List Provided, Would You Like To Filter On Today?\n \n[Chicago, New York City or Washington]: ').lower()
        if city not in CITY_DATA:
          screen_clear()
          print('\nThe City You Entered Is Not From The List Provided\n') 
          sleep(2)
          screen_clear()
          print('\nPlease Re-enter Selecting A City From The Provided List\n')
          sleep(3)
          screen_clear()
          continue   
        else:
            break

    screen_clear()
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
      months = ['all', 'january', 'february', 'march', 'april', 'may', 'june' ]
      month = input('Which Month From The List Provided, Would You Like To Filter On Today?\n \n[January, February, March, April, May, June Or Type All For No Filtering]: ').lower()
      if month not in months:
        screen_clear()
        print('\nThe Month You Entered Is Not From The List Provided\n'),
        sleep(2)
        screen_clear()
        print('\nPlease Re-enter, Selecting A Month From The Provided List\n')
        sleep(3)
        screen_clear()
        continue
      else:
        break

    screen_clear()
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
      days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
      day = input('Which Day From The List Provided, Would You Like To Filter On Today?\n \n[Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday Or Type All For No Filtering: ').lower()
      if day not in days:
        screen_clear()
        print('\nThe Day You Entered Is Not From The List Provided\n')
        sleep(3)
        screen_clear()
        print('\nPlease Re-enter Selecting A Day From The Provided List\n')
        sleep(3)
        screen_clear()
        continue
      else:
        break
    
    screen_clear()
    print('Analysing Data')
    print('-'*40)
    sleep(2)
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
    sleep(1)

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Common Month:', popular_month)
    sleep(1)

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Common day:', popular_day)
    sleep(1)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Common Hour:', popular_hour)
    sleep(1)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    sleep(1)

    # TO DO: display most commonly used start station
    Start_Station = df['Start Station'].value_counts().idxmax()
    print('Most Commonly used start station:', Start_Station)
    sleep(1)

    # TO DO: display most commonly used end station
    End_Station = df['End Station'].value_counts().idxmax()
    print('Most Commonly used end station:', End_Station)
    sleep(1)

    # TO DO: display most frequent combination of start station and end station trip
    Combination_Station = df.groupby(['Start Station', 'End Station']).count()
    print('Most Commonly used combination of start station and end station trip:', Start_Station, " & ", End_Station)
    sleep(1)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    sleep(1)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    sleep(1)
        
    # TO DO: display total travel time
    Total_Travel_Time = sum(df['Trip Duration'])
    print('Total travel time:', Total_Travel_Time/86400, " Days")
    sleep(1)

    # TO DO: display mean travel time
    Mean_Travel_Time = df['Trip Duration'].mean()
    print('Mean travel time:', Mean_Travel_Time/60, " Minutes")
    sleep(1)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    sleep(1)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    sleep(1)

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    #print(user_types)
    print('User Types:\n', user_types)
    sleep(1)

    # TO DO: Display counts of gender
    try:
      gender_types = df['Gender'].value_counts()
      print('\nGender Types:\n', gender_types)
    except KeyError:
      print("\nGender Types:\nNo Data Is Available For This Search.")
    sleep(1)

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
      Earliest_Year = df['Birth Year'].min()
      print('\nEarliest Year:', Earliest_Year)
    except KeyError:
      print("\nEarliest Year:\nNo Data Is Available For This Search.")
    sleep(1)

    try:
      Most_Recent_Year = df['Birth Year'].max()
      print('\nMost Recent Year:', Most_Recent_Year)
    except KeyError:
      print("\nMost Recent Year:\nNo Data Is Available For This Search.")
    sleep(1)

    try:
      Most_Common_Year = df['Birth Year'].value_counts().idxmax()
      print('\nMost Common Year:', Most_Common_Year)
    except KeyError:
      print("\nMost Common Year:\nNo Data Is Available For This Search.")
    sleep(1)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    sleep(1)

def display_raw_data(df):
    """
    Function to display 5 rows of RAW data every time upon request by the user
    or restart program or quit.
    """
    row = 0
    rows_display = input('Would you like to display the first 5 rows of the RAW data? Yes, Restart, Quit : ').lower()
    while True:
        if rows_display == 'restart':
            break
        if rows_display == 'quit':
            quit()
        if rows_display == 'yes':
            print(df.iloc[row:row+5])
            rows_display = input('Would You Like To Display The Next 5 Rows Of The RAW Data? Yes, Restart, Quit: ').lower()
            row += 5
        else:
            rows_display = input('Invalid input\nWould You Like To Display The Next 5 Rows Of The RAW Data? Yes, Restart, Quit: ').lower()
            print(rows_display)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        screen_clear()
        display_raw_data(df)

if __name__ == "__main__":
	main()
