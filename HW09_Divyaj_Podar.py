"""Assignment 9 -> Project Part 1 of 4"""


"""importing libraries"""
import os
from collections import defaultdict
from prettytable import PrettyTable


def file_reading_gen(path, fields, sep=',', header=False):
    """returns a generator of tuple consisiting of fields per line of the txt"""
    #tries to open the file
    try:
        fp = open(path, 'r')
    except FileNotFoundError:
        raise FileNotFoundError(f"{os.path.basename(path)} cannot be opened")
    else:
        #opens the file and returns a generator that gives information about the fields per line
        with fp:
            for line, content in enumerate(fp):
                container = content.strip('\n').split(sep)
                if len(container) != fields:
                    raise ValueError (f"{os.path.basename(path)} has {len(container)} fields on line {line + 1} but expected {fields}")
                elif header==True and line == 0:
                    continue 
                else:
                    yield tuple(container)


class Grades:
    """Grades classes opens the grades.txt and categorizes data in student and ins summary"""
    def __init__(self, directory):
        """stores the data collected from the analyze_files"""
        self.directory = directory
        #student summary
        self.s_files_summary = dict()
        #instructor summary
        self.i_files_summary = dict()

        self.analyze_files()
        
    def analyze_files(self):
        """opens the txt file and categorizes the data into student or instructor"""
        gr = file_reading_gen(self.directory, 4, '\t')
        
        for s_cwid, course, grade, i_cwid in gr:
            
            #Using grades.txt to get s_cwid based coures and grades
            if s_cwid in self.s_files_summary:
                self.s_files_summary[s_cwid][course] = grade
            else:
                self.s_files_summary[s_cwid] = {course: grade}
            
            #Using grades.txt to get i_cwid based courses and number of students in that course    
            if i_cwid not in self.i_files_summary:
                self.i_files_summary[i_cwid] = {course: 1}
            elif course not in self.i_files_summary[i_cwid].keys():
                self.i_files_summary[i_cwid][course] = 1
            else:
                self.i_files_summary[i_cwid][course] += 1


class Student:
    """Students class stores the data from student.txt and grades.txt to summarize the files"""
    
    def __init__(self, directory):
        """Runs the analyze files method and stores the data"""
        self.directory = directory
        self.files_summary = dict()
        self.analyze_files()
        
    def analyze_files(self):
        """analyze files summarizes the data and exports it to self.files_summary for collection"""
        #path generator which automates the path generation
        student_path = os.path.join(self.directory, 'students.txt')
        grades_path = os.path.join(self.directory, "grades.txt")
        
        #importing student.txt and necessary information from grades.txt
        student_tuple = file_reading_gen(path=student_path, fields=3, sep='\t')
        #test if student.txt opens
        next(student_tuple)
        student_grades = Grades(grades_path).s_files_summary
        
        #exporting data to files summary in the form of {s_cwid: {student_name: ,major: , courses:[list]}
        for s_cwid, name, major in student_tuple:
            if s_cwid not in self.files_summary.keys():
                self.files_summary[s_cwid] = {'student_name': name, 'major': major}
                if s_cwid in student_grades.keys():
                    self.files_summary[s_cwid]['courses'] = sorted(student_grades[s_cwid])
            else:
                #raising value error when two student have the same cwid
                raise ValueError("The data has double Student CWID")
    
    def pretty_table(self):
        """creates a pretty table to data in the files_summary"""
        pt = PrettyTable(field_names=['CWID', 'Name', 'Completed Courses'])
    
        for s_cwid in self.files_summary:
            pt.add_row([s_cwid, self.files_summary[s_cwid]['student_name'], self.files_summary[s_cwid]['courses']])
        
        return pt

class Instructor:
    """Instructor class stores the data from instructors.txt and grades.txt to summarize the files"""
    
    def __init__(self, directory):
        """Runs the analyze files method and stores the data"""
        self.directory = directory 
        self.files_summary = dict()
        self.analyze_files()
        
    def analyze_files(self):
        """analyze files summarizes the data and exports it to self.files_summary for collection"""
        #path generator which automates the path generation
        ins_path = os.path.join(self.directory, 'instructors.txt')
        grades_path = os.path.join(self.directory, "grades.txt")
        
        #importing student.txt and necessary information from grades.txt
        ins_tuple = file_reading_gen(path=ins_path, fields=3, sep='\t')
        #test if instructor.txt opens
        next(ins_tuple)
        ins_courses = Grades(grades_path).i_files_summary
        
        #exporting data to files summary in the form of {i_cwid: {ins_name: ,dept: , class_taken: {course: numofstu}}
        for i_cwid, name, dept in ins_tuple:
            if i_cwid not in self.files_summary.keys():
                if  i_cwid in ins_courses.keys():
                    self.files_summary[i_cwid] = {'ins_name': name, 'dept': dept, 'class_taken': {}}

                    for course, nstu in ins_courses[i_cwid].items():
                        self.files_summary[i_cwid]['class_taken'][course] = nstu

                else:
                    #when the professor is not taking any courses according to the grades.txt we set course to none and no of stu to 0
                    self.files_summary[i_cwid] = {'ins_name': name, 'dept': dept, 'class_taken': {None: 0}}
            else:
                raise ValueError("The data has double Instructor CWID")

    
    def pretty_table(self):
        """creates a pretty table to data in the files_summary"""
        pt = PrettyTable(field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])
    
        for i_cwid in self.files_summary:
            for course, nstu in self.files_summary[i_cwid]['class_taken'].items():
                pt.add_row([i_cwid, self.files_summary[i_cwid]['ins_name'], self.files_summary[i_cwid]['dept'],                            course, nstu])
        return pt


class Repository: 
    """Repository refers to the students and instructor class to get required information"""
    def __init__(self, directory):
        if os.path.exists(directory):
            #creating a new instance of class Student
            self.student_summary = Student(directory)
            #creating a new instance of class Instructor
            self.instructor_summary = Instructor(directory)
        else: 
            raise FileNotFoundError("Invalid Directory")
    
    def summary_tables(self):
        """Returns the sumary table of Students and Instructors"""
        summary = f"Student Summary\n{self.student_summary.pretty_table()}\nInstructor Summary\n{self.instructor_summary.pretty_table()}"
        return summary


"""using main"""

if __name__ == '__main__':
    stevens = Repository("/Users/divyaj_podar/downloads/Stevens")
    print(stevens.summary_tables())



