class Frame:
    """
        Represents an Ethernet frame.
    """

    HEADER_SIZE_IN_BYTES = 28
    NBR_OF_BYTES_BEFORE_MSG = 90

    def __init__(self):
        self.fields = {
            "bench_1" :     { "bits" : 64, "value" : "", "useless" : True },
            "frame_date" :  { "bits" : 64, "value" : "", }, 
            "bench_3" :     { "bits" : 32, "value" : "", }, 
            "bench_4" :     { "bits" : 12, "value" : "", "useless" : True }, 
            "bench_5" :     { "bits" : 4, "value" : "", }, 
            "bench_6" :     { "bits" : 16, "value" : "", "useless" : True }, 
            "frame_size" :  { "bits" : 32, "value" : "", }, 
            "MAC_dest" :    { "bits" : 48, "value" : "", }, 
            "MAC_src" :     { "bits" : 48, "value" : "", }, 
            "field_1" :     { "bits" : 16, "value" : "", }, 
            "field_2" :     { "bits" : 16, "value" : "", }, 
            "field_3" :     { "bits" : 16, "value" : "", }, 
            "field_4" :     { "bits" : 16, "value" : "", }, 
            "field_5" :     { "bits" : 16, "value" : "", }, 
            "field_6" :     { "bits" : 8, "value" : "", }, 
            "field_7" :     { "bits" : 8, "value" : "", "useless" : True }, 
            "field_8" :     { "bits" : 16, "value" : "", "useless" : True }, 
            "IP_src" :      { "bits" : 32, "value" : "", }, 
            "IP_dest" :     { "bits" : 32, "value" : "", }, 
            "field_9" :     { "bits" : 16, "value" : "", }, 
            "field_10" :    { "bits" : 16, "value" : "", }, 
            "field_11" :    { "bits" : 16, "value" : "", }, 
            "field_12" :    { "bits" : 16, "value" : "", "useless" : True }, 
            "field_13" :    { "bits" : 3, "value" : "", "useless" : True }, 
            "field_14" :    { "bits" : 1, "value" : "", }, 
            "field_15" :    { "bits" : 1, "value" : "", "useless" : True }, 
            "field_16" :    { "bits" : 3, "value" : "", }, 
            "field_17" :    { "bits" : 3, "value" : "", }, 
            "field_18" :    { "bits" : 5, "value" : "", }, 
            "field_19" :    { "bits" : 2, "value" : "", "useless" : True }, 
            "field_20" :    { "bits" : 14, "value" : "", }, 
            "field_21" :    { "bits" : 16, "value" : "", }, 
            "field_22" :    { "bits" : 4, "value" : "", "useless" : True }, 
            "field_23" :    { "bits" : 1, "value" : "", }, 
            "field_24" :    { "bits" : 1, "value" : "", "useless" : True }, 
            "field_25" :    { "bits" : 1, "value" : "", }, 
            "field_26" :    { "bits" : 1, "value" : "", }, 
            "field_27" :    { "bits" : 2, "value" : "", }, 
            "field_28" :    { "bits" : 6, "value" : "", }, 
            "field_29" :    { "bits" : 6, "value" : "", }, 
            "field_30" :    { "bits" : 10, "value" : "", }, 
            "field_31" :    { "bits" : 8, "value" : "", "useless" : True }, 
            "field_32" :    { "bits" : 8, "value" : "", }, 
            "field_33" :    { "bits" : 16, "value" : "", }, 
            "field_34" :    { "bits" : 16, "value" : "", }, 
            "field_35" :    { "bits" : 16, "value" : "", }, 
            "field_36" :    { "bits" : 16, "value" : "", "useless" : True }
        }

        self.message_type = ""
        self.packet_date = ""

        self.test_name = ""
        self.test_execution_date = ""
