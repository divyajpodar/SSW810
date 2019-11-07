from HW09_Divyaj_Podar import Grades, Student, Instructor, Repository
import unittest

class TestModuleSummarizer(unittest.TestCase):
    """class to test HW09_Divyaj_Podar"""

    def test_Grades(self):
        grades = Grades('/Users/divyaj_podar/downloads/Stevens/grades.txt')
        student = {'10115': {'SSW 567': 'A', 'SSW 564': 'B+', 'SSW 687': 'A', 'CS 545': 'A'},
                    '10172': {'SSW 555': 'A', 'SSW 567': 'A-'},
                    '10175': {'SSW 567': 'A', 'SSW 564': 'A', 'SSW 687': ''}}
        self.assertEqual(grades.s_files_summary['10172'], student['10172'])
        self.assertEqual(grades.s_files_summary['10175']['SSW 687'], '')
        self.assertRaises(FileNotFoundError, Grades, '/Users/divyaj_podar/downloads/Stevens/WRONGFILE.txt')

    def test_Student(self):
        students = Student('/Users/divyaj_podar/downloads/Stevens')
        s_data = {'10175': {'student_name': 'Erickson, D', 'major': 'SFEN', 'courses': ['SSW 564', 'SSW 567', 'SSW 687']},\
                    '10183': {'student_name': 'Chapman, O', 'major': 'SFEN', 'courses': ['SSW 689']},\
                    '11399': {'student_name': 'Cordova, I', 'major': 'SYEN', 'courses': ['SSW 540']}}
        self.assertEqual(students.files_summary['11399']['student_name'], 'Cordova, I')
        self.assertEqual(students.files_summary['10183'], s_data['10183'])
        self.assertRaises(FileNotFoundError, Student, '/Users/divyaj_podar/downloads/NYU')
        self.assertRaises(ValueError, Student, '/Users/divyaj_podar/downloads/Rutgers')

    def test_Instructor(self):
        instructor = Instructor('/Users/divyaj_podar/downloads/Stevens')
        i_data = {'98763': {'ins_name': 'Newton, I', 'dept': 'SFEN', 'class_taken': {'SSW 555': 1, 'SSW 689': 1}},
                    '98762': {'ins_name': 'Hawking, S', 'dept': 'SYEN', 'class_taken': {None: 0}},}
        self.assertEqual(instructor.files_summary['98762']['class_taken'][None], 0)
        self.assertEqual(instructor.files_summary['98763']['class_taken'], i_data['98763']['class_taken'])
        self.assertRaises(FileNotFoundError, Instructor, '/Users/divyaj_podar/downloads/NYU')
        self.assertRaises(ValueError, Instructor, '/Users/divyaj_podar/downloads/Rutgers')

    def test_Repository(self):
        self.assertRaises(FileNotFoundError, Repository, '/Users/divyaj_podar/downloads/WRONGDIRECTORY')




if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)