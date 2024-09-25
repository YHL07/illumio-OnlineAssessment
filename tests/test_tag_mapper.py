import csv
import unittest

from source_code.TagMapper import TagMapper


class TagMapperTests(unittest.TestCase):

    def test_happy_path(self):
        flow_data_column_definition = ["version", "account-id", "interface-id", "srcaddr", "dstaddr", "srcport",
                                       "dstport",
                                       "protocol", "packets", "bytes", "start", "end", "action", "log-status"]
        flow_data_log_file_path = "input_files/happy_path/flow_data_log"
        tag_count_output_file_path = "output_files/tag_count"
        protocol_combination_output_file_path = "output_files/protocol_combination"

        tag_mapper = TagMapper("input_files/happy_path/lookup_table.csv")

        tag_mapper.get_flow_tag_count(flow_data_column_definition, flow_data_log_file_path,
                                      tag_count_output_file_path)
        tag_mapper.get_port_protocol_combination(flow_data_column_definition, flow_data_log_file_path,
                                                 protocol_combination_output_file_path)

        with open(tag_count_output_file_path, mode='r') as f:
            tag_count_lines = csv.DictReader(f)
            self.assertEqual(tag_count_lines.fieldnames, ["Tag", "Counts"])
            actual = []
            expected = [{'Tag': 'sv_p6', 'Counts': '4'}, {'Tag': 'untagged', 'Counts': '1'},
                        {'Tag': 'sv_p4', 'Counts': '4'}, {'Tag': 'sv_p1', 'Counts': '8'},
                        {'Tag': 'sv_p5', 'Counts': '4'}, {'Tag': 'sv_p2', 'Counts': '4'},
                        {'Tag': 'sv_p3', 'Counts': '0'}]
            for line in tag_count_lines:
                actual.append(line)
            self.assertCountEqual(actual, expected)
            self.assertEqual(tag_count_lines.line_num, 8)

        with open(protocol_combination_output_file_path, mode='r') as f:
            protocol_combination_lines = csv.DictReader(f)
            self.assertEqual(protocol_combination_lines.fieldnames, ["Port", "Protocol", "Count"])
            actual = []
            expected = [{'Port': '123', 'Protocol': 'tcp', 'Count': '4'},
                        {'Port': '443', 'Protocol': 'tcp', 'Count': '2'},
                        {'Port': '23', 'Protocol': 'tcp', 'Count': '2'},
                        {'Port': '25', 'Protocol': 'tcp', 'Count': '2'},
                        {'Port': '110', 'Protocol': 'tcp', 'Count': '2'},
                        {'Port': '456', 'Protocol': 'tcp', 'Count': '4'},
                        {'Port': '456', 'Protocol': 'udp', 'Count': '4'},
                        {'Port': '443', 'Protocol': 'udp', 'Count': '1'},
                        {'Port': '23', 'Protocol': 'udp', 'Count': '1'},
                        {'Port': '25', 'Protocol': 'udp', 'Count': '1'},
                        {'Port': '110', 'Protocol': 'udp', 'Count': '2'},
                        {'Port': '789', 'Protocol': 'udp', 'Count': '1'}]
            for line in protocol_combination_lines:
                actual.append(line)
            self.assertCountEqual(actual, expected)
            self.assertEqual(protocol_combination_lines.line_num, 13)

    def test_invalid_lookup_table_header(self):
        with self.assertRaises(Exception, msg="Header format invalid"):
            TagMapper("input_files/invalid_header/lookup_table_invalid_header.csv")


if __name__ == '__main__':
    unittest.main()
