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
#course input because we want only one course to study
course = int(input("select nmumber of course: "))
print("your course id is - ",saral_data["availableCourses"][course-1]["id"])
print(course,saral_data["availableCourses"][course-1]["name"])
print("")
course_id = saral_data["availableCourses"][course-1]["id"]
def calling_sec_api():
        # calling_second_api here we are hitting a perticuler api of courses
        course_id = saral_data["availableCourses"][course-1]["id"]
        if path.exists("parent/saral"+str(course_id)+".json")==True:
                with open("parent/saral"+str(course_id)+".json") as read_file:
                        data_of_sec_api= json.load(read_file)
                        return data_of_sec_api
        else:
                second_api = requests.get("http://saral.navgurukul.org/api/courses/"+str(course_id)+"/exercises")
                data= second_api.json()
                json_file2 = open("parent/saral"+str(course_id)+".json","w")
                json.dump(data,json_file2,indent=2)
                return data
data_of_sec_api=calling_sec_api()

def parents():
        # we are getting our courses name with their sub courses 
        count = 1
        for counter in data_of_sec_api["data"]:
                print("  "+str(count)+")",counter["name"])
                s_no = 1
                for iterate in data_of_sec_api["data"][count-1]["childExercises"]:
                        print("     "+str(s_no)+".",iterate["name"])
                        s_no = s_no + 1
                print("")
                count+=1
parents()
parent = int(input("select a parent"))
print()
print("0 -",data_of_sec_api["data"][parent-1]["name"])
def child():
        # here we have choosen one sub course of main course 
        s_no = 1
        for index in data_of_sec_api["data"][parent-1]["childExercises"]:
                print("   ",s_no,"-",index["name"])
                s_no = s_no + 1
child()
child = int(input("select the question"))
# by child we will get our slug
if child == 0:
        slug = data_of_sec_api["data"][parent-1]["slug"]
else:
        slug = data_of_sec_api["data"][parent-1]["childExercises"][child-1]["slug"]
def content():
        if path.exists("childcontent/slug"+str(child-1)+".json")==True:
               with open("parent/slug"+str(course_id)+".json") as read_content:
                        content_of_slug= json.load(read_content)
                        return content_of_slug
        else:
                get_content= requests.get("https://saral.navgurukul.org/api/courses/"+str(course_id)+"/exercise/getBySlug?slug="+str(slug))
                content_of_slug= get_content.json()
                json_file = open("childcontent/slug"+str(course_id)+".json","w")
                json.dump(content_of_slug,json_file,indent=2)
                return content_of_slug["content"]
print(content())