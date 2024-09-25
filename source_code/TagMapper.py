import csv
import logging
import socket


class TagMapper:
    tag_field_name = "tag"
    protocol_field_name = "protocol"
    srcport_field_name = "srcport"
    dstport_field_name = "dstport"
    untagged_field_name = "untagged"
    lookup_table_map_key_separator = ","
    protocol_combination_separator = ","
    lookup_table_map_keys = []
    tags = []
    tag_count_output_headers = ["Tag", "Counts"]
    port_combination_output_headers = ["Port", "Protocol", "Count"]
    lookup_table_map = {}
    protocol_number_name_map = {'51': 'ah', '7': 'cbt', '60': 'dstopts', '8': 'egp', '50': 'esp',
                                '44': 'fragment', '3': 'ggp', '0': 'ip', '78': 'iclfxbm', '1': 'icmp',
                                '58': 'icmpv6', '22': 'idp', '2': 'igmp', '9': 'igp', '4': 'ipv4',
                                '41': 'ipv6', '115': 'l2tp', '256': 'max', '77': 'nd', '59': 'none',
                                '113': 'pgm', '103': 'pim', '12': 'pup', '255': 'raw', '27': 'rdp',
                                '43': 'routing', '132': 'sctp', '5': 'st', '6': 'tcp', '17': 'udp'}
    logger = logging.getLogger(__name__)

    def __init__(self, lookup_table_file_path):
        self.__read_lookup_table(lookup_table_file_path)
        return

    def __validate_lookup_table_header(self, lookup_table_csv):
        if len(lookup_table_csv.fieldnames) != 3 or set(lookup_table_csv.fieldnames) != {self.dstport_field_name,
                                                                                         self.protocol_field_name,
                                                                                         self.tag_field_name}:
            self.logger.error("Header format invalid")
            raise Exception("Header format invalid")

    def __read_lookup_table(self, lookup_table_file_path):
        with open(lookup_table_file_path, mode='r') as f:
            lookup_table_csv = csv.DictReader(f)

            # validation of header
            self.__validate_lookup_table_header(lookup_table_csv)

            tag_set = set()
            tag_set.add(self.untagged_field_name)

            # construct lookup_table_map with format of {<<dstport>, <protocol>>: [<tag>]}
            for row in lookup_table_csv:
                current_tag = row[self.tag_field_name].lower()
                key = row[self.dstport_field_name] + self.lookup_table_map_key_separator + str(
                    self.__get_protocol_number_from_name(row[self.protocol_field_name]))
                if self.lookup_table_map.__contains__(key):
                    self.lookup_table_map[key].append(current_tag)
                else:
                    self.lookup_table_map[key] = [current_tag]
                tag_set.add(current_tag)
            self.tags.extend(tag_set)

    def __get_protocol_name_from_number(self, number):
        return self.protocol_number_name_map[number]

    def __get_protocol_number_from_name(self, name):
        return socket.getprotobyname(name)

    # returns the tag count
    def get_flow_tag_count(self, flow_data_column_definition, input_file_path, output_file_path):
        tag_count_map = {}
        # init tag_count_map with 0 values
        for tag in self.tags:
            tag_count_map[tag] = 0

        with open(input_file_path, mode='r') as f:
            flow_data = csv.DictReader(f, delimiter=' ', fieldnames=flow_data_column_definition)
            for row in flow_data:
                # construct query key, format: <<dstport>, <protocol>>
                key = row[self.dstport_field_name] + self.lookup_table_map_key_separator + row[self.protocol_field_name]
                if self.lookup_table_map.__contains__(key):
                    tag_list = self.lookup_table_map[key]
                    for tag in tag_list:
                        tag_count_map[tag] += 1
                else:
                    tag_count_map[self.untagged_field_name] += 1

        with open(output_file_path, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.tag_count_output_headers)
            for tag_key in tag_count_map:
                writer.writerow([tag_key, tag_count_map[tag_key]])

    def get_port_protocol_combination(self, flow_data_column_definition, input_file_path, output_file_path):
        port_protocol_combination_map = {}
        with open(input_file_path, mode='r') as f:
            flow_data = csv.DictReader(f, delimiter=' ', fieldnames=flow_data_column_definition)
            for row in flow_data:
                # collect dstport-protocol combination
                key = row[
                          self.dstport_field_name] + self.protocol_combination_separator + self.__get_protocol_name_from_number(
                    row[self.protocol_field_name])
                if port_protocol_combination_map.__contains__(key):
                    port_protocol_combination_map[key] += 1
                else:
                    port_protocol_combination_map[key] = 1

                # collect srcport-protocol combination
                key = row[
                          self.srcport_field_name] + self.protocol_combination_separator + self.__get_protocol_name_from_number(
                    row[self.protocol_field_name])
                if port_protocol_combination_map.__contains__(key):
                    port_protocol_combination_map[key] += 1
                else:
                    port_protocol_combination_map[key] = 1

        with open(output_file_path, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.port_combination_output_headers)
            for key in port_protocol_combination_map:
                ls = key.split(self.protocol_combination_separator)
                writer.writerow([ls[0], ls[1], port_protocol_combination_map[key]])
