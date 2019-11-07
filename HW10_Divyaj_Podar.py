
"""Assignment 10, part 2 of project"""


"""Importing modules"""
import os
from collections import defaultdict
from prettytable import PrettyTable


#File reader

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


class Student:
    """Stores necessary information about 1 student at a time"""
    
    pt = ['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Electives']
    
    def __init__(self, cwid, name, major):
        """stores all the information about the student"""
        self.cwid = cwid
        self.name = name
        self.major = major
        self.courses = defaultdict(str)
        
        self.completed_courses = None
        self.remaining_required = None
        self.remaining_electives = None
        
    def course_filler(self, course, grade):
        """fills the self.courses in the __init__ function"""
        self.courses[course] = grade
    
    def course_seg(self, major_instance):
        """Uses instance of major and uses its method to sort the courses and store it"""
        self.completed_courses, self.remaining_required,        self.remaining_electives = major_instance.course_segergator(self.courses)
        
        
    def pretty_table(self, pt):
        """adds a row to the repository created student pretty table"""
        pt.add_row([self.cwid, self.name, self.major, sorted(self.completed_courses),                   self.remaining_required, self.remaining_electives])


class Instructor:
    
    pt = ['CWID', 'Name', 'Dept', 'Course', 'Students']
    
    def __init__(self, cwid, name, dept):
        """stores all the information about the instructor"""
        self.cwid = cwid
        self.name = name
        self.dept = dept
        self.courses = defaultdict(int)
        
    def course_filler(self, course):
        """fills the self. courses in the __init__ function"""
        self.courses[course] += 1
    
    def pretty_table(self, pt):
        """adds a row to the repository created instructor pretty table"""
        for course, num_students in self.courses.items():
            pt.add_row([self.cwid, self.name, self.dept, course, num_students])


# In[205]:


class Major:
    
    pt = ['Dept', 'Required', 'Electives']
    valid_grade = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']
    
    def __init__(self, major):
        """stores all the information about the major"""
        self.major = major
        self.valid_grade
        self.required = set()
        self.elective = set()
        
    def requirement_filler(self, req, course):
        """splits the courses in major into required or elective"""
        if req == 'R':
            self.required.add(course)
        elif req == 'E':
            self.elective.add(course)
    
    def course_segergator(self, courses):
        """sorts the courses in student into completed, required and elective"""
        completed_courses = set()
        remaining_required = self.required.copy()
        remaining_elective = self.elective.copy()
        
        for course, grade in courses.items():
            if grade in self.valid_grade:
                completed_courses.add(course)
                if course in self.elective:
                    remaining_elective = None
            
            if course in self.required and grade in self.valid_grade:
                remaining_required.remove(course)
        
        return completed_courses, remaining_required, remaining_elective

    def pretty_table(self, pt):
        """adds a row to the repository created major pretty table"""
        pt.add_row([self.major, sorted(self.required), sorted(self.elective)])
    

class Repository:
                
    def __init__(self, directory, p_table = False):
        """stores the keys and the instances of the class created and calls the methods"""
        self.directory = directory
        self.student_dict = dict()
        self.instructor_dict = dict()
        self.major_dict = dict()
        
        self.get_major()
        self.get_student()
        self.get_instructor()
        self.get_grades()
        self.req_elc()
        
        if p_table == True:
            self.pretty_tables()
    
    def pretty_tables(self):
        """prints the pretty tables conatining all the summary"""
        pt_maj = PrettyTable(field_names=Major.pt)
        for major in self.major_dict:
            self.major_dict[major].pretty_table(pt_maj)
        
        pt_stu = PrettyTable(field_names=Student.pt)
        for cwid in self.student_dict:
            self.student_dict[cwid].pretty_table(pt_stu)
        
        pt_ins = PrettyTable(field_names=Instructor.pt)
        for cwid in self.instructor_dict:
            self.instructor_dict[cwid].pretty_table(pt_ins)
        
        print (f'Majors Summary\n{pt_maj}\nStudent Summary\n{pt_stu}\nInstructor Summary\n{pt_ins}')
    
    def get_major(self):
        """opens majors.txt and creates major instances"""
        path = os.path.join(self.directory, 'majors.txt')
        
        
        mjr_details = file_reading_gen(path, 3, '\t', True)
        
        try:
            for major, req, course in mjr_details:
                if major not in self.major_dict:
                    self.major_dict[major] = Major(major)
                
                self.major_dict[major].requirement_filler(req, course)
        
        except ValueError:
            print(f"For major: {major}, number of fields != required number of fields")
        
        except FileNotFoundError:
            raise FileNotFoundError("majors.txt cannot be found/opened")
            
    def get_student(self):
        """opens students.txt and create student instances"""
        path = os.path.join(self.directory, 'students.txt')
        
        std_details = file_reading_gen(path, 3, sep=';', header=True)
        
        try:
            for cwid, name, major in std_details:
                if cwid not in self.student_dict:
                    self.student_dict[cwid] = Student(cwid, name, major)
                else:
                    print (f"DUPLICATE student CWID: {cwid}")
        
        except ValueError:
            print(f"For CWID: {cwid}, number of fields != required number of fields")
            
        except FileNotFoundError:
            raise FileNotFoundError("students.txt cannot be found/opened")
        
    def get_instructor(self):
        """opens instructors.txt and create instructor instances"""
        path = os.path.join(self.directory, 'instructors.txt')
        
        ins_details = file_reading_gen(path, 3, sep='|', header=True)
        
        try:
            for cwid, name, dept in ins_details:
                if cwid not in self.instructor_dict:
                    self.instructor_dict[cwid] = Instructor(cwid, name, dept)
                else:
                    print (f"DUPLICATE instructor CWID: {cwid}")
                    
        except ValueError:
            print(f"For CWID: {cwid}, number of fields != required number of fields")
            
        except FileNotFoundError:
            raise FileNotFoundError("instructors.txt cannot be found/opened")
        
    def get_grades(self):
        """opens grades.txt and populates other classes"""
        path = os.path.join(self.directory, 'grades.txt')
        
        grades_details = file_reading_gen(path, 4, sep='|', header=True)
        
        try:
            for s_cwid, course, grade, i_cwid in grades_details:
                if s_cwid in self.student_dict:
                    self.student_dict[s_cwid].course_filler(course, grade)
                if i_cwid in self.instructor_dict:
                    self.instructor_dict[i_cwid].course_filler(course)
        
        except ValueError:
            print(f"For s_cwid: {s_cwid}, number of fields != required number of fields")
        
        except FileNotFoundError:
            print ("grades.txt cannot be opened")
    
    def req_elc(self):
        """sorts the requirement of the courses"""
        for cwid in self.student_dict:
            student_info = self.student_dict[cwid]
            student_major = student_info.major
            
            try:
                student_info.course_seg(self.major_dict[student_major])
            except:
                print (f"Student with cwid {cwid} has a major {student_major} which is not in repository")


if __name__ == "__main__":
    stevens = Repository('/Users/divyaj_podar/downloads/stevens_updated', True)
