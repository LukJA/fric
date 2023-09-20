import xml.etree.ElementTree as ET

from pathlib import Path


root_filepath = (Path(__file__).parent / '..').resolve()

tree = ET.parse(root_filepath / 'pytest_report.xml')
root = tree.getroot()

print('# Test Results')

######################
## GENERATE SUMMARY ##
######################

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
    result_filename = str(
        root_filepath /
        f"sim_build/{mod_name}/{test_name}/{test_name}.results.xml"
    )

    if mod_path not in modules:
        modules[mod_path] = []
        failures[mod_path] = 0

    modules[mod_path].append(
        {
            "test_name": test_name,
            "filename": result_filename,
        }
    )

    if not passed:
        failures[mod_path] += 1


print("\n---\n")
print("### Results")


for item in modules:  # pylint: disable=C0206
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
        except Exception as e:
            print(f"<h5>Internal error displaying test results: {e}.</h5>")
            continue

        test_root = test_tree.getroot()
        print("<table>")
        print("<tr><td><b>Test</b></td><td><b>Result</b></td><td><b>Message</b></td></tr>")

        errors = {}
        to_process = {}

        log_filepath = root_filepath / f"logs/generated/{item}/{test['test_name']}.log"

        with open(log_filepath) as logfile:
            for i, line in enumerate(logfile):
                if 'failed' in line:
                    test_name = line.split(' ')[-2]
                    line_no = i + 2

                    errors[test_name] = ""
                    to_process[line_no] = test_name
                    to_process[line_no+1] = test_name
                    to_process[line_no+2] = test_name
                    
                if i in to_process:
                    if errors[to_process[i]] == "":
                        errors[to_process[i]] = line.strip()
                    else:
                        errors[to_process[i]] += '<br />' + line.strip()
                    del to_process[i]

        for subtest in test_root[0]:
            if subtest.tag == "testcase":
                st_name = subtest.attrib['name']

                if len(subtest) == 0:
                    print(
                        f"<tr>"
                        f"<td>{st_name}</td>"
                        f"<td>PASS</td>"
                        f"<td></td>"
                        f"</tr>"
                    )
                else:
                    print(
                        f"<tr>"
                        f"<td>{st_name}</td>"
                        f"<td><b>FAIL</b></td>"
                        f"<td>{errors[st_name]}</td>"
                        f"</tr>"
                    )
                
        print("</table>")

    print("<br />")
    
    print("</details>")
