#database
courses=['Mathematics','Physics','Chemistry','Sociology','Biology','Physiology','Philosophy','Comp Science']
c_id=[1,2,3,4,5,6,7,8]
strt_morning=[10,11,11,10,10,11,10,11]
strt_afternoon=[13,14,15,14,13,13,15,14]

#intro and table of courses
print("Welcome To Jantar Mantar Open University Courses")
print('Please choose your course list today to prepare a Schedule:(you must choose upto 5 courses)')
print('Course List: ')
i=0
print('C_id\t Course\t\t\t  Morning\t Afternoon')
for i in range(8):
    print(str(c_id[i])+'\t'+ courses[i] + ' \t\t' + "  " + str(strt_morning[i]) + '\t\t ' + str(strt_afternoon[i]))
print('Every Class has a Duration of 1hr each')

#entry of courses for the day
choices=[]
print("Please enter the C_id of Courses you wish to attend: ")
for i in range(0,5):
    response=int(input())
    if response in c_id:
        choices.append(response)
    else:
        print('Invalid Course ID..please re enter the courses with proper course IDs')
        exit(1)
print("Your choices are: ",choices)

#working of schedule maker by dividing into morning and afternoon shifts 
schedule_morn=[]
for i in choices:
    if strt_morning[i-1] not in schedule_morn:
        schedule_morn.append(strt_morning[i-1])
    elif strt_morning[i-1] in schedule_morn:
        print("The C_id: "+str(i)+" is clashing with C_id: "+str(choices[schedule_morn.index(strt_morning[i-1])])+" for the morning shift")
        print("Shifting it to a Afternoon shift")
schedule_aftnoon=[]
choice_2nd=choices[2::]
for i in choice_2nd:
    if strt_afternoon[i-1] not in schedule_aftnoon:
        schedule_aftnoon.append(strt_afternoon[i-1])
    elif strt_afternoon[i-1] in schedule_aftnoon:
        print("The C_id: "+str(i)+" is clashing with C_id: "+str(choice_2nd[schedule_aftnoon.index(strt_afternoon[i-1])])+" for the afternoon shift")
        print("Two or More Course time clashing...Please redo the course selection")
        exit(1)
schedule_fin=schedule_morn+schedule_aftnoon

#printing final schedule
print('\nSchedule:')
print('C_id\t Course\t\t\t  Start Time')
for i in range(0,5):
    for j in range(0,5-i-1):
        if schedule_fin[j]>schedule_fin[j+1]:
            schedule_fin[j],schedule_fin[j+1]=schedule_fin[j+1],schedule_fin[j]
            choices[j],choices[j+1]=choices[j+1],choices[j]
j=0
for i in choices:
    print(str(c_id[i-1])+'\t'+ courses[i-1] + ' \t\t' + "  " + str(schedule_fin[j]))
    j+=1

#word of advice and signing off
print("All courses have a duration of 1hr, please don't be late to join the classes..")
print("Happy Learning!!")