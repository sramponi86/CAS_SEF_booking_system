import unittest
import importlib
import argparse

"""
Script for discovering unittest tests, similar to `python -m unittest discover`,
but that allows passing a list of test cases that are expected to fail.
"""

parser = argparse.ArgumentParser(description='Discover an run unit tests.')
parser.add_argument('--pattern', required=True, help='test discovery pattern')
parser.add_argument('--root', default='./', help='root dir for test discovery')
parser.add_argument('--expected-failures', default=None, help='file with test cases expected to fail')
args = parser.parse_args()


loader = unittest.TestLoader()
test_modules = loader.discover(args.root, pattern=args.pattern)

runner = unittest.TextTestRunner()

expected_failures = []

if args.expected_failures != None:
  with open(args.expected_failures, 'r') as fh:
    expected_failures = fh.read().splitlines() 

print(expected_failures)

for test_module in test_modules._tests:
  # print('type(test_module):', type(test_module))
  # print(test_module)
  for test_suite in test_module._tests:
    # print('  test_suite: ', test_suite)
    # print('  type(test_suite):', type(test_suite))
    # print('  test_suite._tests:', test_suite._tests)
    # print(' ', dir(test_suite))
    for test_case in test_suite._tests:
      # print('    test_case: ', test_case)
      # print('    test_case.id():', test_case.id())
      # print('    type(test_case):', type(test_case))
      if test_case.id() in expected_failures:
        print(f'Decorating {test_case.id()} as expected to fail')
        (package_name, class_name, method_name) = test_case.id().rsplit('.', 2)
        # print('    package_name:', class_name)
        # print('    class_name:', class_name)
        # print('    method_name:', method_name)
        clazz = getattr(importlib.import_module(package_name), class_name)
        setattr(clazz, method_name, unittest.expectedFailure(getattr(clazz, method_name)))

was_successful = True

for test_module in test_modules._tests:
  if test_module._tests != []:
    result = runner.run(test_module)
    was_successful = was_successful and result.wasSuccessful()

exit(not was_successful)
