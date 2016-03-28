# Calculate the duration of course from start date and end date
def duration_of_course(start,end):
    difference_in_days = (end - start).days
    if difference_in_days%7!=0:
        return difference_in_days//7+1
    return difference_in_days//7