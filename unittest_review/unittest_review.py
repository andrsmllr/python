#!/bin/python

# Import the unittest package.
import unittest

# Define a new test case as a subclass of unittest.TestCase.
class SimpleTestCase(unittest.TestCase)
    def setUp(self):
        """Code in the setUp method is executed each time before a test case
        is executed."""
        a = list([1, 2, 3])
        b = a
        c = list([4, 5, 6])
        d = dict()
        pass
    
    def trearDown(self):
        """Code in the tearDown method is executed each time after a test case
        is executed."""
        pass
    
    def test_something(self):
        # Use the assert* functions to determine the outcome of a test.
        unittest.assertEqual(1,1)
        unittest.assertNotEqual(1,0)
        unittest.assertTrue(1 == 1)
        unittest.assertFalse(1 == 0)
        unittest.assertIs(a, b)
        unittest.assertIsNot(a, c)
        unittest.assertIsNone(None)
        unittest.assertIsNotNone(a)
        unittest.assertIn(1, a)
        unittest.assertNotIn(4, b)
        unittest.assertIsInstance(c, list)
        unittest.assertNotIsInstance(d, list)
        unittest.assertRaises()
        unittest.assertRaisesRegex()
        unittest.assertWarns()
        unittest.assertWarnsRegex()
        unittest.assertLogs()
        unittest.assertAlmostEqual()
        unittest.assertNotAlmostEqual()
        unittest.assertGreater()
        unittest.assertGreaterEqual()
        unittest.assertLess()
        unittest.assertLessEqual()
        unittest.assertRegex()
        unittest.assertNotRegex()
        unittest.assertCountEqual()
        
    def test_somethingWithSubTests(self):
        # Use subTest to execute a "sequence" of tests without aborting on
        # a single failing sub-test.
        for i in range(0,5):
            with self.subTest(i=i):
                self.assertEqual(i % 2, 0)
        
# Show available decorators.
class DecoratedTestCase(unittest.TestCase):
    # setUp will not be run if a test is skipped.
    def setUp(self):
        """Code in the setUp method is executed each time before a test case
        is executed."""
        
    # tearDown will not be run if a test is skipped.
    def trearDown(self):
        """Code in the tearDown method is executed each time after a test case
        is executed."""
    
    @unittest.skip("State reason for skipping test.")
    def test_something1(self):
        pass
    
    @unittest.skipIf(1 == 1, "State reason for skipping test.")
    def test_something2(self):
        pass
        
    @unittest.skipUnless(1 == 0, "State reason for skipping test.")
    def test_something3(self):
        pass
        
    # Mark a test as an expected failure, so it won't be run.
    @unittest.expectedFailure
    def test_something4(self):
        pass
        
    def test_something4(self):
        # A test can also be skipped manually by raising a SkipTest exception.
        raise unittest.SkipTest("State reason for skipping test.")

if __name__ == '__main__':
    simpleTestSuite =
        unittest.TestSuite(SimpleTestCase, DecoratedTestCase)
    
    simpleTestLoader = unittest.TestLoader()
    
    simpleTestResult = unittest.TestResult()
    
    simpleTestRunner = unittest.TestRunner()        

