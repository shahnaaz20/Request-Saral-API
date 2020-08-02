import requests
import json
import os
from os import path
def getting_courses():
        #here we are checking if file exist then it will just read the file and give us data
        if os.path.isfile("saral.json")==True:
                with open("saral.json","r") as read_file:
                        saral = json.load(read_file)
                        return saral
        else:
                #we are hitting the api to get data
                get_api = requests.get("http://saral.navgurukul.org/api/courses")
                saral = get_api.json()
                json_file = open("saral.json","w")
                json.dump(saral,json_file,indent=2)
                return saral
saral_data = getting_courses()
def saral_courses():
    index = 0
    # from this loop we are taking whole corsses name with it course id
    while index < len(saral_data["availableCourses"]):
        print(index+1,saral_data["availableCourses"][index]["name"],"id -",saral_data["availableCourses"][index]["id"])
        index = index + 1
saral_courses()
#course input because we want see a particular course
course = int(input("select nmumber of course: "))
print("your course id is - ",saral_data["availableCourses"][course-1]["id"])
print(course,saral_data["availableCourses"][course-1]["name"])
print("")
course_id = saral_data["availableCourses"][course-1]["id"]
def calling_sec_api(courses_id):
                second_api = requests.get("http://saral.navgurukul.org/api/courses/"+str(courses_id)+"/exercises")
                data= second_api.json()
                json_file2 = open("saral1.json","w")
                json.dump(data,json_file2,indent=2)
                return data
data_of_sec_api=calling_sec_api(course_id)


def parents():
        # we are getting our courses name with their sub courses 
        count = 1
        for i in data_of_sec_api["data"]:
                print("  "+str(count)+")",i["name"])
                s_no = 1
                for counter in data_of_sec_api["data"][count-1]["childExercises"]:
                        print("     "+str(s_no)+".",counter["name"])
                        s_no = s_no + 1
                print("")
                count+=1
parents()
up_down = input("if u want to see previous courses gai press up/down:  ")
if up_down == "up":
        saral_courses()
        course = int(input("select nmumber of course: "))
        course_id = saral_data["availableCourses"][course-1]["id"]
        data_of_sec_api=calling_sec_api(course_id)
        print(course,saral_data["availableCourses"][course-1]["name"])
        parents()
parent = int(input("select a parent"))
print()
print("0 -",data_of_sec_api["data"][parent-1]["name"])
def child():
        # here we have choosen one sub course of main course 
        count = 1
        for index in data_of_sec_api["data"][parent-1]["childExercises"]:
                print("   ",count,"-",index["name"])
                count=count + 1
child()
child = int(input("select the question"))
# by child we will get our slug
if child == 0:
        slug = data_of_sec_api["data"][parent-1]["slug"]
else:
        slug = data_of_sec_api["data"][parent-1]["childExercises"][child-1]["slug"]
def content(slugs):
                get_content= requests.get("https://saral.navgurukul.org/api/courses/"+str(course_id)+"/exercise/getBySlug?slug="+str(slugs))
                content_of_slug= get_content.json()
                json_file = open("slug.json","w")
                json.dump(content_of_slug,json_file,indent=2)
                return content_of_slug["content"]
print(content(slug))
slug_list= []
slug = data_of_sec_api["data"][parent-1]["slug"]
slug_list.append(content(slug))
for index in data_of_sec_api["data"][parent-1]["childExercises"]:
        my_slug = index["slug"]
        slug_list.append(content(my_slug))
i = 1
while i <= len(slug_list):
        prev_next = input("if you want to go previous then press p/n: ")
        if prev_next=="p":
                child  = child - 1
                if child < len(slug_list):
                        if child == -1:
                                print("page_not_found")
                                break
                        print(slug_list[child])
        elif prev_next=="n":
                child=child+1
                if child>=0:
                        if child==len(slug_list):
                                print("page_not_found")
                                break
                        print(slug_list[child])
        else:
                print("invalid input  ")
                break
        i = i + 1