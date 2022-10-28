import frame
import sql
import argparse
import os
import sys
import termcolor
import bitstring
import hexdump
import macaddress
import datetime
import re

class Extractor:
    """
        Represents the extractor.
    """

    def __init__(self):
        self.cmd_line_args = None
        self.all_frames = []
        self.current_frame = None
        self.sql_db = sql.SQL()
    
    def run(self) -> bool:
        """
            Runs the extractor.

            Return - true - in case of success,
                   - false - in case of error.
        """

        # 
        # Parses the cmd line arguments.
        #
        if not self.parse_cmd_line_args():
            return False
        
        #
        # Extracting the Ethernet frames.
        #
        print(termcolor.colored("[+]", "yellow"), "Extracting frames")

        if not self.extract_frames_from_file():
            print(termcolor.colored("[-]", "red"), "Error extracting frames")
            return False
        
        #
        # Inserts the frames into the SQL db.
        #
        print(termcolor.colored("[+]", "yellow"), "Adding frames to the database")
        
        if not self.insert_frames_into_db():
            return False

        print(termcolor.colored("[+]", "yellow"), "Done")
        return True

    def parse_cmd_line_args(self) -> bool:
        """
            Parses the cmd line arguments.

            Return - true - in case of success,
                   - false - in case of error.
        """

        parser = argparse.ArgumentParser(formatter_class=lambda prog: argparse.RawDescriptionHelpFormatter(prog, max_help_position=300),
                                        epilog="""
examples:
  {0} --binary ethernet.bin --full test.rep
  {0} --binary ethernet.bin --short test_name "YY-MM-DD hh-mm-ss"

notes:
  [--full] and [--short] can't be used together.""".format(sys.argv[0]))

        parser.add_argument("--binary", help="binary file containing frames", metavar="BINARY_FILE", required=True)
        parser.add_argument("--full", help="test report file", metavar="REPORT_FILE")
        parser.add_argument("--short", help="name and execution date of the test", metavar=("TEST_NAME", "TEST_EXECUTION_DATE"), nargs=2)

        args = parser.parse_args()

        ok = True

        #
        # Checks if the binary file can be read.
        #
        try:
            open(args.binary, "r").close()

        except:
            print("[--binary] the binary file can't be read")
            ok = False

        #
        # Makes sure that either [--short] or [--full] is used.
        #
        if args.short == None and args.full == None:
            print("[--short] or [--full] is required")
            ok = False

        #
        # Makes sure that [--short] & [--full] are not used together.
        #
        if args.short != None and args.full != None:
            print("[--short] and [--full] can't be used together")
            ok = False

        #
        # Checks that the test report file can be read (when used).
        #
        if args.full != None and not os.access(args.full, os.R_OK):
            print("[--full] the test report file can't be read")
            ok = False

        if not ok:
            print()
            parser.print_help()
            return False

        self.cmd_line_args = args

        return True

    def extract_frames_from_file(self) -> bool:
        """
            Extracts frames from the binary file.

            Return - true - in case of success,
                   - false - in case of error.
        """

        try:
            #
            # Reads the binary file bit by bit.
            #
            bit_stream = bitstring.ConstBitStream(filename=self.cmd_line_args.binary)

            #
            # Extracts all frames.
            #
            while bit_stream.pos < len(bit_stream):
                sys.stdout.write("\r" + termcolor.colored("[*]", "blue") + f" {len(self.all_frames) + 1}")
                sys.stdout.flush()

                self.current_frame = frame.Frame()

                self.find_test_name_and_execution_date()                
                
                #
                # Reads the header.
                #
                for field_name in list(self.current_frame.fields.keys())[:7]:
                    data = bit_stream.read(self.current_frame.fields[field_name]["bits"])

                    #
                    # Doesn't set its value if it's useless.
                    #
                    if "useless" not in self.current_frame.fields[field_name]:
                        self.current_frame.fields[field_name]["value"] = data
                    
                        #
                        # Hexa convertion of values.
                        #
                        self.current_frame.fields[field_name]["value"] = hex(int(self.current_frame.fields[field_name]["value"].bin, 2))

                #
                # Reads the known fields (MACs, IPs, ...).
                #
                bit_read_from_frame = 0
                for field_name in list(self.current_frame.fields.keys())[7:]:
                    if bit_read_from_frame + self.current_frame.fields[field_name]["bits"] <= int(self.current_frame.fields["frame_size"]["value"], 16) * 8:
                        bit_read_from_frame += self.current_frame.fields[field_name]["bits"]

                        data = bit_stream.read(self.current_frame.fields[field_name]["bits"])

                        #
                        # Doesn't set its value if it's useless.
                        #
                        if "useless" not in self.current_frame.fields[field_name]:
                            self.current_frame.fields[field_name]["value"] = data
                        
                            #
                            # Hexa convertion of values.
                            #
                            self.current_frame.fields[field_name]["value"] = hex(int(self.current_frame.fields[field_name]["value"].bin, 2))
                    else:
                        break
                
                #
                # Reads the msg (if any).
                #
                if (bit_read_from_frame / 8) < int(self.current_frame.fields["frame_size"]["value"], 16):
                    self.current_frame.msg = bit_stream.read((int(self.current_frame.fields["frame_size"]["value"], 16) * 8) - bit_read_from_frame)

                    #
                    # Creates a "hexdump" style representation of the msg.
                    #
                    self.current_frame.msg = hexdump.hexdump(self.current_frame.msg.bytes)

                #
                # Performs some modifications to the values to make them more human-readable.
                #
                self.calculate_frame_date()
                self.calculate_packet_date()
                self.calculate_MACs_and_IPs()
                self.calculate_msg_type()
                
                self.all_frames.append(self.current_frame)

        except:
            return False

        print()
        return True
    
    def insert_frames_into_db(self) -> bool:
        """
            Appends frames into the SQL db.

            Return - true - in case of success,
                   - false - in case of error.
        """

        #
        # Opens the DB.
        #
        if not self.sql_db.open_db():
            return False
        
        #
        # Inserts all frames.
        #
        i = 1
        for frame in self.all_frames:
            sys.stdout.write("\r" + termcolor.colored("[*]", "blue") + f" {i}")
            sys.stdout.flush()

            if not self.sql_db.insert_frame(frame):
                print(termcolor.colored("[-]", "red"), "Error inserting frames")
                return False
            
            i += 1
        
        print()
        
        return True

    def calculate_frame_date(self):
        """
            Calculates the frame date (since 01/01/1970 00:00:00).
        """

        #
        # Calculates.
        #
        epoch = datetime.datetime(1970, 1, 1)
        sec = datetime.timedelta(seconds=int(self.current_frame.fields["frame_date"]["value"], 16) / (10**10))

        self.current_frame.fields["frame_date"]["value"] = (epoch + sec).strftime('%Y-%m-%d %H:%M:%S.%f')

    def calculate_packet_date(self):
        """
            Calculates the packet date (since 01/01/2000 12:00:00).
        """

        #
        # Makes sure all fields have a value.
        #
        for field_name in [ "field_33", "field_34", "field_35" ]:
            if self.current_frame.fields[field_name]["value"] == "":
                return

        #
        # Calculates.
        #
        epoch = datetime.datetime(2000, 1, 1, 12)
        sec = datetime.timedelta(seconds=int(self.current_frame.fields["field_33"]["value"], 16) \
                                + int(self.current_frame.fields["field_34"]["value"], 16) \
                                + int(self.current_frame.fields["field_35"]["value"], 16) * (1/(2**16)))

        self.current_frame.packet_date = (epoch + sec).strftime('%Y-%m-%d %H:%M:%S.%f')

    def calculate_msg_type(self):
        """
            Calculates the msg type (MT).
        """

        #
        # Makes sure all fields have a value.
        #
        for field_name in [ "field_14", "field_18", "field_28", "field_29", "field_30" ]:
            if self.current_frame.fields[field_name]["value"] == "":
                return

        self.current_frame.message_type = "0x" + self.current_frame.fields["field_14"]["value"][2:] + \
                                                self.current_frame.fields["field_18"]["value"][2:] + \
                                                self.current_frame.fields["field_28"]["value"][2:] + \
                                                self.current_frame.fields["field_29"]["value"][2:] + \
                                                self.current_frame.fields["field_30"]["value"][2:] 

    def calculate_MACs_and_IPs(self):
        """
            Calculates MACs and IPs.
        """

        #
        # Handles MACs.
        #
        for field_name in [ "MAC_src", "MAC_dest" ]:
            #
            # Pads with 0s, to have 12 bytes.
            #
            self.current_frame.fields[field_name]["value"] = str.format('0x{:012x}', int(self.current_frame.fields[field_name]["value"], 16))
            
            #
            # From hex to MAC.
            #
            self.current_frame.fields[field_name]["value"] = str(macaddress.MAC(self.current_frame.fields[field_name]["value"][2:])).replace("-", ":").lower()

        #
        # Handles IPs.
        #
        for field_name in [ "IP_src", "IP_dest" ]:
            self.current_frame.fields[field_name]["value"] = self.current_frame.fields[field_name]["value"][2:]
            
            #
            # From hex to IP.
            #
            self.current_frame.fields[field_name]["value"] = '.'.join(str(int(i, 16)) for i in [self.current_frame.fields[field_name]["value"][i:i+2] for i in range(0, len(self.current_frame.fields[field_name]["value"]), 2)])

    def find_test_name_and_execution_date(self):
        """
            Finds the name and execution date of the test.
            And then adds the values to the corresponding fields in the current frame.
        """

        #
        # Reads from cmd line.
        # 
        if self.cmd_line_args.short != None:
            self.current_frame.test_name = self.cmd_line_args.short[0]
            self.current_frame.test_execution_date = self.cmd_line_args.short[1]
        
        #
        # Reads from report file.
        #
        elif self.cmd_line_args.full:
            with open(self.cmd_line_args.full) as file:
                for line in file:
                    #
                    # Similar to grep.
                    #
                    test_name_match = re.findall("^\\* Test\\s+: (.*)", line)
                    test_execution_date_match = re.findall("^\\* Execution begin date\\s+: \"(.*)\"", line)

                    if len(test_name_match) == 1:
                        self.current_frame.test_name = test_name_match[0]
                   
                    if len(test_execution_date_match) == 1:
                        self.current_frame.test_execution_date = test_execution_date_match[0]
