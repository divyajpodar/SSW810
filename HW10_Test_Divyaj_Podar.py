from HW10_Divyaj_Podar import Student, Instructor, Major, Repository
import unittest



class TestModuleSummarizer(unittest.TestCase):
    """class to test HW10_Divyaj_Podar"""

    def test_Student(self):
        """testing the class student using the student repository"""
        stevens = Repository('/Users/divyaj_podar/downloads/stevens_11')
        self.assertEqual(stevens.student_dict['10103'].name, 'Jobs, S')
        #checking segregator
        self.assertEqual(stevens.student_dict['10103'].completed_courses, {'CS 501', 'SSW 810'})
    
    def test_Major(self):
        """testing the class major using the student repository"""
        stevens = Repository('/Users/divyaj_podar/downloads/stevens_11')
        #checking if requirement filler works
        self.assertEqual(stevens.major_dict['SFEN'].elective, {'CS 501', 'CS 546'})
    
    def test_Instructor(self):
        """testing the class instructor using the student repository"""
        stevens = Repository('/Users/divyaj_podar/downloads/stevens_11')
        self.assertEqual(stevens.instructor_dict['98764'].courses, {'CS 546': 1})
    
    """
    NOT ABLE TO TEST IT UNLESS I GENERATE TUPLES IN ACTUAL PROGRAM WHICH MIGHT SLOW THE PROGRAM
    def test_Instructor_table_db(self):
        ""testing the method in class repository"
        stevens = Repository('/Users/divyaj_podar/downloads/stevens_11', True)
        self.assertEqual(print(stevens.instructor_table_db()), "Instructor Summary from Database\n+-------+------------+------+---------+----------+
|  CWID |    Name    | Dept |  Course | Students |
+-------+------------+------+---------+----------+
| 98764 |  Cohen, R  | SFEN |  CS 546 |    1     |
| 98763 | Rowland, J | SFEN | SSW 810 |    4     |
| 98763 | Rowland, J | SFEN | SSW 555 |    1     |
| 98762 | Hawking, S |  CS  |  CS 501 |    1     |
| 98762 | Hawking, S |  CS  |  CS 546 |    1     |
| 98762 | Hawking, S |  CS  |  CS 570 |    1     |
+-------+------------+------+---------+----------+")
"""


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)