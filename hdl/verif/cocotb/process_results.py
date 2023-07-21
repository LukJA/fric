import xml.etree.ElementTree as ET

tree = ET.parse('pytest_report.xml')
root = tree.getroot()

print('# Test Results')

print('| Test Name | Status | Message |')
print('| --------- | ------ | ------- |')
for test in root[0]:
    name = (
        f"{test.attrib['classname'].removeprefix('tests.')}::"
        f"{test.attrib['name']}"
    )
    passed = len(test) == 0
    failure_messages = (
        [""] if passed
        else [failure.attrib['message'] for failure in test]
    )

    print(f"| {name} | {'PASS' if passed else '**FAIL**'} | {failure_messages[0]} |")
