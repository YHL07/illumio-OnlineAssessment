# Lookup Table Matching

### Assumption:
1. the lookup table file has three columns: dstport,protocol,tag.
2. lookup table csv files, and flow data log files are always well-formatted.
3. This program supports flow data logs other than version 2, but we assume that flow data logs always have these columns: srcporet, dstport,protocol.
4. Since matching should be case-insensitive, the tag count output file has the tag printed as lower case.
5. For internet protocols, only the protocols listed in the python's socket package are supported.
6. Program will generate two files. One for tag_count, the other for port/protocol combination. 
7. The term "port/protocol" means aggregation of "srcport/protocol" and "dstport/protocol".
8. There is no duplicate rows in lookup table file.

### How to run:
    Main function:
    ./source_code/main.py 

    Unit tests:
    ./tests/test_tag_mapper.py

### Explanation:
#### Data Structure: 
Class "TagMapper" is used to solve these two problems. To initialize a new TagMapper object, user needs to pass the path of lookup_table csv file into the constructor. 
Inside the contractor, TagMapper analyzes the content of the lookup table, and persists a data structure <code>lookup_table_map</code> as its member variable. 
<code>lookup_table_map</code> is a HashMap. Its key is the string concatenation of the value of srcport and the value of protocol. Its value is a list of tags. 
<code>lookup_table_map</code> is used to maintain the mapping relationship between (srcport, protocol) and tags. For example, {'25,6': ['sv_p1', 'email']} means
the tuple of (srcport=25, protocol="tcp") maps to two tags: "sv_p1", "email".
#### Function: 
To get the tag count, user needs to call <code>TagMapper.get_flow_tag_count(flow_data_column_definition, input_file_path, output_file_path)</code> . 
The function iterates all the rows in flow_data_log. For each row, we can easily get a list of tags that this row belongs to, by querying <code>lookup_table_map</code>, then calculate the counts of the tags.

To get the port/protocol combination, user needs to call <code>TagMapper.get_port_protocol_combination(flow_data_column_definition, input_file_path, output_file_path)</code>. 
It uses a HashMap <code>port_protocol_combination_map</code> to store the mapping between (port, protocol) and its counts. We iterate each row of the flow_data_log. For each row, 
we have two tuples: (dstport, protocol), (srcport, protocol). We used them to update the corresponding values in <code>port_protocol_combination_map</code>.

### Testing done:
1. Tested the normal functionality. Given a flow_data_log and lookup table file, program can generate tag_count file and port/protocol combination file.
2. Tested the case that lookup table is missing headers. In this case, program will throw an exception with the message of "Header format invalid".
3. Tested the case-insensitivity for tags. "sv_P1" and "SV_p1" are considered as the same tag. In the output file, they are represented as lower case "sv_p1".
4. Tested the scenario that a tag is mapped to multiple different (dstport, protocol) tuple.
5. Tested the scenario that one (dstport, protocol) tuple is mapped to multiple tags.

### Complexity:
Time Complexity O(nm) <br/>
Space Complexity O(nm). <br/>
where n is the number of records in the flow_data_log, m is the number of distinct tags(case-insensitive)