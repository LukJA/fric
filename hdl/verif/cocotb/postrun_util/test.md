# Test Results
### Summary
| Test Name | Status | Message |
| --------- | ------ | ------- |
| arithmetic.test_arithmetic::test_posit_adder | PASS |  |
| henry_decoder.test_henry_decoder::test_priority_encoder | PASS |  |
| henry_decoder.test_henry_decoder::test_count_regime | PASS |  |
| luke_decoder.test_luke_decoder::test_dff | PASS |  |
| luke_decoder.test_luke_decoder::test_clo | **FAIL** | SystemExit: ERROR: Failed 1 of 1 tests. |
| luke_decoder.test_luke_decoder::test_clz | **FAIL** | SystemExit: ERROR: Failed 1 of 1 tests. |
| luke_decoder.test_luke_decoder::test_decoder | PASS |  |
| luke_decoder.test_luke_decoder::test_ffo | PASS |  |
| luke_decoder.test_luke_decoder::test_ffno | PASS |  |

---

### Results
<details>
<summary>
Detailed results for <tt>arithmetic</tt> 
(no failed tests)
</summary>
<h4>test_posit_adder</h4>
<table>
<tr><td><b>Test</b></td><td><b>Result</b></td><td><b>Message</b></td></tr>
<tr><td>test_posit_adder_top</td><td>PASS</td><td></td></tr>
</table>
<br />
</details>
<details>
<summary>
Detailed results for <tt>henry_decoder</tt> 
(no failed tests)
</summary>
<h4>test_priority_encoder</h4>
<table>
<tr><td><b>Test</b></td><td><b>Result</b></td><td><b>Message</b></td></tr>
<tr><td>test_16b_count</td><td>PASS</td><td></td></tr>
</table>
<h4>test_count_regime</h4>
<table>
<tr><td><b>Test</b></td><td><b>Result</b></td><td><b>Message</b></td></tr>
<tr><td>test_count_regime</td><td>PASS</td><td></td></tr>
</table>
<br />
</details>
<details>
<summary>
Detailed results for <tt>luke_decoder</tt> 
(<b>2 failed tests</b>)
</summary>
<h4>test_dff</h4>
<table>
<tr><td><b>Test</b></td><td><b>Result</b></td><td><b>Message</b></td></tr>
<tr><td>dff_test</td><td>PASS</td><td></td></tr>
</table>
<h4>test_clo</h4>
<table>
<tr><td><b>Test</b></td><td><b>Result</b></td><td><b>Message</b></td></tr>
<tr><td>count_leading_ones</td><td><b>FAIL</b></td><td>File "/Users/harryfranks/Projects/fric/hdl/verif/cocotb/tests/luke_decoder/clo/cocotb_test_clo.py", line 17, in count_leading_ones<br />assert dut.q.value == i</td></tr>
</table>
<h4>test_clz</h4>
<table>
<tr><td><b>Test</b></td><td><b>Result</b></td><td><b>Message</b></td></tr>
<tr><td>test_count_leading_zeros</td><td><b>FAIL</b></td><td>File "/Users/harryfranks/Projects/fric/hdl/verif/cocotb/tests/luke_decoder/clz/cocotb_test_clz.py", line 18, in test_count_leading_zeros<br />assert dut.q.value == i</td></tr>
</table>
<h4>test_decoder</h4>
<table>
<tr><td><b>Test</b></td><td><b>Result</b></td><td><b>Message</b></td></tr>
<tr><td>test_decoder_a</td><td>PASS</td><td></td></tr>
<tr><td>test_decoder_b</td><td>PASS</td><td></td></tr>
</table>
<h4>test_ffo</h4>
<table>
<tr><td><b>Test</b></td><td><b>Result</b></td><td><b>Message</b></td></tr>
<tr><td>test_count_leading_ones</td><td>PASS</td><td></td></tr>
</table>
<h4>test_ffno</h4>
<table>
<tr><td><b>Test</b></td><td><b>Result</b></td><td><b>Message</b></td></tr>
<tr><td>test_count_leading_ones</td><td>PASS</td><td></td></tr>
</table>
<br />
</details>
