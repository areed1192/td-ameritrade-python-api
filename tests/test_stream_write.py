import csv
import json

CSV_PATH = "my_test.csv"

with open(r"samples\responses\sample_level_two_options.json","r") as BookFile:
    data = json.load(BookFile)
    print(data)
    data = data[0]['data']


approved_writes_level_2 = ['OPTIONS_BOOK']

# open the new CSV file in write mode, `newline` makes sure we don't have extra blank rows.
with open(CSV_PATH, mode = "w", newline='') as stream_file:
    
    # create the writer.
    stream_writer = csv.writer(stream_file)

    # check if it's a list, this should always be the case.
    if isinstance(data, list):

        for service_result in data:
                                    
            # A Service response should have the following keys.
            service_name = service_result['service']
            service_timestamp = service_result['timestamp']
            service_command = service_result['command']
            service_contents = service_result['content']

            if service_name in approved_writes_level_2:

                for service_content in service_contents:
                    
                    symbol = service_content['key']
                    book_timestamp = service_content['1']
                    book_bid = service_content['2']
                    book_ask = service_content['3']

                    for index, activity_section in enumerate(book_bid):
                        
                        section_id = str(book_timestamp) + "_" + str(index)
                        price = activity_section['0']
                        total_size = activity_section['1']
                        total_count = activity_section['2']
                        book_data_collection = activity_section['3']

                        for book_data in book_data_collection:

                            mpid = book_data["0"]
                            size = book_data["1"]
                            _time = book_data["2"]

                            data = [service_name, service_timestamp, service_command, "book_bid", section_id, 
                                    "book_bid_price", price, 
                                    "book_bid_size", total_size, 
                                    "book_bid_otal_count", total_count, 
                                    "book_bid_section_mpid", mpid, 
                                    "book_bid_section_size", size, 
                                    "book_bid_section_time", _time]

                            stream_writer.writerow(data)

                    for index, activity_section in enumerate(book_ask):
                        
                        section_id = str(book_timestamp) + "_" + str(index)
                        price = activity_section['0']
                        total_size = activity_section['1']
                        total_count = activity_section['2']
                        book_data_collection = activity_section['3']

                        for book_data in book_data_collection:

                            mpid = book_data["0"]
                            size = book_data["1"]
                            _time = book_data["2"]

                            data = [service_name, service_timestamp, service_command, "book_ask", section_id, 
                                    "book_ask_price", price, 
                                    "book_ask_size", total_size, 
                                    "book_ask_total_count", total_count, 
                                    "book_ask_section_mpid", mpid, 
                                    "book_ask_section_size", size, 
                                    "book_ask_section_time", _time]

                            stream_writer.writerow(data)                           

            else: 
                data = [service_name, service_timestamp, service_command, 'null','null','null']
                stream_writer.writerow(data)
