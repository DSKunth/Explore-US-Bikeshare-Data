import time
import pandas as pd
import calendar

CITY_DATA = {'chicago': 'data\chicago.csv',
             'new york city': "data\city_new_york.csv",
             'washington': 'data\washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
   
    cities = ('chicago', 'new york city', 'washington')
    city = ''
    while city not in cities:
        city = input('\nWould you like to see data for Chicago, New York City, or Washington?\n').lower()
        if city not in cities:
            print('\nYou have entered an invalid CITY. Please select from Chicago, New York City or Washington.')
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    months = ('all', 'january', 'february', 'march', 'april', 'may', 'june')
    month = ''
    while month not in months:
        month = input('\nWhich month would you like to filter the data by: January, February, March, April, May, or June? \nEnter "all" if you would like to see data for months from January to June.\n').lower()
        if month not in months:
            print('\nYou have entered an invalid MONTH. Please select from January, February, March, April, May, June or all.')
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
    day = ''
    while day not in days:
        day = input('\nWhich day would you like to filter the data by: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? \nEnter "all" if you would like to see data for all days.\n').lower()
        if day not in days:
            print('\nYou have entered an invalid DAY. Please select from Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all.')
            continue
        else:
            break

    print('-'*120)
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
    
    # extract month from the Start Time column to create a month column
    df['Month'] = df['Start Time'].dt.month
   
    # extract day from the Start Time column to create a day_of_week column
    df['Day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable and create new dataframe
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['Month'] == month]

    # filter by day of week if applicable and create new dataframe
    if day != 'all':
        df = df[df['Day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
 
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['Month'].mode()[0]
    print('Most popular month of traveling:', calendar.month_name[common_month])

    # display the most common day of week
    common_day = df['Day_of_week'].mode()[0]
    print('Most popular day of traveling:', common_day)

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    common_hour = df['Hour'].mode()[0]
    print('Most popular hour of the day to start traveling:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*120)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('Most commonly used start station:', common_start)

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('Most commonly used end station:', common_end)

    # display most frequent combination of start station and end station trip
    df['Frequent Trip'] = df['Start Station'] + ' to ' + df['End Station']
    common_trip = df['Frequent Trip'].mode()[0]
    print('Most common trip from start station to end station:', common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*120)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time:', total_travel_time, 'seconds')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Average travel time:', mean_travel_time, 'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*120)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print('User Type Count:\n',user_type_count)

    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print('\nGender Count:\n', gender_count)
    except KeyError:
        print('\nGender Count: data not available.')

    # Display earliest, most recent, and most common year of birth
    try:
        birth_min = int(df['Birth Year'].min())
        print('\nEarliest year of birth:', birth_min)
    except KeyError:
        print('\nEarliest birth year: data not available.')

    try:
        birth_max = int(df['Birth Year'].max())
        print('Most recent year of birth:', birth_max)
    except KeyError:
        print('\nMost recent birth year: data not available.')

    try:
        birth_mode = int(df['Birth Year'].mode()[0])
        print('Most common year of birth:', birth_mode)
    except KeyError:
        print('\nMost common birth year: data not available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*120)


def display_data(df):
    """Displays raw data 5 rows at a time, if requested."""

    view_data = input('\nWould you like to view 5 rows of raw data? yes or no:\n').lower()
    if view_data != 'no':
        start_loc = 0
        while (start_loc < df['Start Time'].count() and view_data != 'no'):
            print(df.iloc[start_loc:start_loc+5])
            start_loc += 5
            more_data = input('\nWould you like to view 5 more rows of data? yes or no:\n').lower()
            if more_data != 'yes':
                break
                
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
