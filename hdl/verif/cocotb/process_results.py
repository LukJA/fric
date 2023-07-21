import xml.etree.ElementTree as ET

tree = ET.parse('pytest_report.xml')
root = tree.getroot()

print('# Test Results')

## GENERATE SUMMARY
###################

modules = {}
failures = {}

print('### Summary')

print('| Test Name | Status | Message |')
print('| --------- | ------ | ------- |')
for test in root[0]:
    module_name = test.attrib['classname'].removeprefix('tests.')
    test_name = test.attrib['name']
    passed = len(test) == 0
    failure_message = "" if passed else test[0].attrib['message']

    print( # table entry for our summary
        f"| {module_name}::"f"{test_name} "
        f"| {'PASS' if passed else '**FAIL**'} "
        f"| {failure_message} |"
    )

    split_idx = module_name.rindex('.')
    mod_path = module_name[:split_idx].replace('.', '/')    
    mod_name = module_name[split_idx+1:]
    dir_name = test_name.replace('test_', '')
    result_filename = (
        f"sim_build/{mod_path}/{dir_name}/{test_name}.results.xml"
    )

    if mod_path not in modules:
        modules[mod_path] = []
        failures[mod_path] = 0

    modules[mod_path].append(
        {
            "test_name": test_name,
            "filename": result_filename
        }
    )

    if not passed:
        failures[mod_path] += 1


print("\n---\n")
print("### Results")

for item in modules:
    print("<details>")
    print("<summary>")
    print(f"Detailed results for <tt>{item}</tt> ")

    f = failures[item]
    if f:
        print(f"(<b>{f} failed tests</b>)")
    else:
        print(f"(no failed tests)")

    print("</summary>")

    for test in modules[item]:
        print(f"<h4>{test['test_name']}</h4>")

        try:
            test_tree = ET.parse(test['filename'])
        except:
            print("<h5>Internal error displaying test results.</h5>")
            continue

        test_root = test_tree.getroot()
        print("<table>")
        print("<tr><td><b>Test</b></td><td><b>Result</b></td></tr>")

        for subtest in test_root[0]:
            if subtest.tag == "testcase":
                st_name = subtest.attrib['name']
                st_passed = (
                    "<td bgcolor='green' style='color: white'>PASS</td>"
                    if len(subtest) == 0 else
                    "<td bgcolor='red' style='color: white'>FAIL</td>"
                )
                print(f"<tr><td>{st_name}</td>{st_passed}</tr>")
        print("</table>")
    print("<br />")
    
    print("</details>")
