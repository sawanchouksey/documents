''' Take input from user to calculate average temprature and how many days temprature 
    is greater than average temprature.
    1. take input from user how many days temprature?
    2. input temprature of all days i.e.
        a. day 1 temprature
        b. day 2 temprature
        .
        .
        .
        n. day n tempraure according to input 1.
    3. calculate the average temprature
    4. calculate the number of days temprature is greater then average temprature.  
'''

# take input from user how many days temprature
def takeInputTemprature():
    days = int(input("Please enter the number of days temprature you want to check:"))
    return days

# input temprature of all days
def takeEachDayTemprature(temp_list, no_of_days):
    for i in range(no_of_days):
        tempratureEachDay = float(input(f"Enter Days {i} Highest temprature:"))
        temp_list.append(tempratureEachDay)
    return temp_list

# calculate the average temprature
def calculateAvgTemprature(temp_list):
    if not temp_list:  # Check if the list is empty
        return 0  # Avoid division by zero
    total_sum = sum(temp_list)
    count = len(temp_list)
    averageTemprature = total_sum / count
    return averageTemprature 

# calculate the number of days temprature is greater then average temprature
def checkDaysTempratureAboveAvg(temp_list,average_temprature):
    new_list = []
    if not temp_list:
        return 0
    for i in temp_list:
        if i > average_temprature:
            dayNumber = f"day_{temp_list.index(i)}"
            new_list.append(dayNumber)
    return new_list
    
tempratureInDays = []

NoOfDays = takeInputTemprature()

tempratureInAllDays = takeEachDayTemprature(tempratureInDays,NoOfDays)

averageTempratureInAllDays = calculateAvgTemprature(tempratureInAllDays)

daysTempratureAboveAvg = checkDaysTempratureAboveAvg(tempratureInAllDays,averageTempratureInAllDays)

print(f"Temprature in {daysTempratureAboveAvg} is more than Average temprature.")

print(f"There are {len(daysTempratureAboveAvg)} days when temprature is more than Average temprature.")






