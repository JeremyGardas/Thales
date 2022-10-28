# **Ethernet Frame Extractor (Python)**

### **How does it work ?**
* Extracts Ethernet frames from a binary file.

* Writes the results into a SQL database.

```
usage: main.py [-h] --binary BINARY_FILE [--full REPORT_FILE] [--short TEST_NAME TEST_EXECUTION_DATE]

optional arguments:
  -h, --help                             show this help message and exit
  --binary BINARY_FILE                   binary file containing frames
  --full REPORT_FILE                     test report file
  --short TEST_NAME TEST_EXECUTION_DATE  name and execution date of the test

examples:
  ./main.py --binary ethernet.bin --full test.rep
  ./main.py --binary ethernet.bin --short test_name "YY-MM-DD hh-mm-ss"

notes:
  [--full] and [--short] can't be used together.
```

# **Web Interface (PHP)**

### **How does it work ?**
* Reads the Ethernet frame content from a SQL database.

* Displays results in a user-friendly way.

* Allows the user to change the field names.

* Allows the user to create some transfert functions (to convert hexa values to labels)
