from HW10_Divyaj_Podar import Student, Instructor, Major, Repository
import unittest



class TestModuleSummarizer(unittest.TestCase):
    """class to test HW10_Divyaj_Podar"""

    def test_Student(self):
        """testing the class student using the student repository"""
        stevens = Repository('/Users/divyaj_podar/downloads/stevens_updated')
        self.assertEqual(stevens.student_dict['10103'].name, 'Baldwin, C')
        #checking segregator
        self.assertEqual(stevens.student_dict['10103'].completed_courses, {'CS 501', 'SSW 564', 'SSW 567', 'SSW 687'})
    
    def test_Major(self):
        """testing the class major using the student repository"""
        stevens = Repository('/Users/divyaj_podar/downloads/stevens_updated')
        #checking if requirement filler works
        self.assertEqual(stevens.major_dict['SFEN'].elective, {'CS 501', 'CS 513', 'CS 545'})
    
    def test_Instructor(self):
        """testing the class instructor using the student repository"""
        stevens = Repository('/Users/divyaj_podar/downloads/stevens_updated')
        self.assertEqual(stevens.instructor_dict['98765'].courses, {'SSW 567': 4, 'SSW 540': 3})


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)