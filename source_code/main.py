from source_code.TagMapper import TagMapper

if __name__ == '__main__':
    flow_data_column_definition = ["version", "account-id", "interface-id", "srcaddr", "dstaddr", "srcport", "dstport",
                                   "protocol", "packets", "bytes", "start", "end", "action", "log-status"]

    tag_mapper = TagMapper("input_files/lookup_table.csv")
    tag_mapper.get_flow_tag_count(flow_data_column_definition, "input_files/flow_data_log", "output_files/tag_count")
    tag_mapper.get_port_protocol_combination(flow_data_column_definition, "input_files/flow_data_log",
                                             "output_files/protocol_combination")
