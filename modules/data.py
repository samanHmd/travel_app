from datetime import datetime

flights_data = [
    {"flightNumber": "FL001","departureCity": "Montreal","arrivalCountry": "Italy","arrivalCity": "Rome","departureTime": datetime.strptime('2023-07-01 08:00:00', '%Y-%m-%d %H:%M:%S'),"flightPrice": 700},
    {"flightNumber": "FL002","departureCity": "Montreal","arrivalCountry": "USA","arrivalCity": "Los Angeles","departureTime": datetime.strptime('2023-07-01 08:00:00', '%Y-%m-%d %H:%M:%S'),"flightPrice": 600},
    {"flightNumber": "FL004","departureCity": "Montreal","arrivalCountry": "Germany","arrivalCity": "Berlin","departureTime": datetime.strptime('2023-07-01 08:00:00', '%Y-%m-%d %H:%M:%S'),"flightPrice": 900},
    {"flightNumber": "FL005","departureCity": "Montreal","arrivalCountry": "Spain","arrivalCity": "Madrid","departureTime": datetime.strptime('2023-07-01 08:00:00', '%Y-%m-%d %H:%M:%S'),"flightPrice": 700},


    #Paris
    # day 1
    {"flightNumber": "FL0101", "departureCity": "Montreal", "arrivalCountry":"France", "arrivalCity":  "Paris", "departureTime": datetime.strptime('2023-07-01 08:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 800},
    {"flightNumber": "FL0102", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Paris", "departureTime": datetime.strptime('2023-07-01 10:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 850},
    {"flightNumber": "FL0103", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Paris", "departureTime": datetime.strptime('2023-07-01 12:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 900},
    {"flightNumber": "FL0104", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Paris", "departureTime": datetime.strptime('2023-07-01 14:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 950},
    {"flightNumber": "FL0105", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Paris", "departureTime": datetime.strptime('2023-07-01 16:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 1000},
    # day 2
    {"flightNumber": "FL0201", "departureCity": "Montreal", "arrivalCountry":"France", "arrivalCity":  "Paris", "departureTime": datetime.strptime('2023-07-02 08:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 800},
    {"flightNumber": "FL0202", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Paris", "departureTime": datetime.strptime('2023-07-02 10:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 850},
    {"flightNumber": "FL0203", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Paris", "departureTime": datetime.strptime('2023-07-02 12:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 900},
    {"flightNumber": "FL0204", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Paris", "departureTime": datetime.strptime('2023-07-02 14:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 950},
    {"flightNumber": "FL0205", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Paris", "departureTime": datetime.strptime('2023-07-02 16:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 1000},
    # day 3
    {"flightNumber": "FL0301", "departureCity": "Montreal", "arrivalCountry":"France", "arrivalCity":  "Paris", "departureTime": datetime.strptime('2023-07-03 08:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 800},
    {"flightNumber": "FL0302", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Paris", "departureTime": datetime.strptime('2023-07-03 10:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 850},
    {"flightNumber": "FL0303", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Paris", "departureTime": datetime.strptime('2023-07-03 12:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 900},
    {"flightNumber": "FL0304", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Paris", "departureTime": datetime.strptime('2023-07-03 14:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 950},
    {"flightNumber": "FL0305", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Paris", "departureTime": datetime.strptime('2023-07-03 16:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 1000},
    #day 4
    {"flightNumber": "FL0401", "departureCity": "Montreal", "arrivalCountry":"France", "arrivalCity":  "Paris", "departureTime": datetime.strptime('2023-07-04 08:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 800},
    {"flightNumber": "FL0402", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Paris", "departureTime": datetime.strptime('2023-07-04 10:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 850},
    {"flightNumber": "FL0403", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Paris", "departureTime": datetime.strptime('2023-07-04 12:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 900},
    {"flightNumber": "FL0404", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Paris", "departureTime": datetime.strptime('2023-07-04 14:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 950},
    {"flightNumber": "FL0405", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Paris", "departureTime": datetime.strptime('2023-07-04 16:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 1000},
    #day 5
    {"flightNumber": "FL0501", "departureCity": "Montreal", "arrivalCountry":"France", "arrivalCity":  "Paris", "departureTime": datetime.strptime('2023-07-05 08:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 800},
    {"flightNumber": "FL0502", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Paris", "departureTime": datetime.strptime('2023-07-05 10:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 850},
    {"flightNumber": "FL0503", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Paris", "departureTime": datetime.strptime('2023-07-05 12:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 900},
    {"flightNumber": "FL0504", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Paris", "departureTime": datetime.strptime('2023-07-05 14:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 950},
    {"flightNumber": "FL0505", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Paris", "departureTime": datetime.strptime('2023-07-05 16:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 1000},



    #Marseille
    # day 1
    {"flightNumber": "FL1101", "departureCity": "Montreal", "arrivalCountry":"France", "arrivalCity":  "Marseille", "departureTime": datetime.strptime('2023-07-01 08:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 800},
    {"flightNumber": "FL1102", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Marseille", "departureTime": datetime.strptime('2023-07-01 10:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 850},
    {"flightNumber": "FL1103", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Marseille", "departureTime": datetime.strptime('2023-07-01 12:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 900},
    {"flightNumber": "FL1104", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Marseille", "departureTime": datetime.strptime('2023-07-01 14:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 950},
    {"flightNumber": "FL1105", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Marseille", "departureTime": datetime.strptime('2023-07-01 16:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 1000},
    # day 2
    {"flightNumber": "FL1201", "departureCity": "Montreal", "arrivalCountry":"France", "arrivalCity":  "Marseille", "departureTime": datetime.strptime('2023-07-02 08:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 800},
    {"flightNumber": "FL1202", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Marseille", "departureTime": datetime.strptime('2023-07-02 10:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 850},
    {"flightNumber": "FL1203", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Marseille", "departureTime": datetime.strptime('2023-07-02 12:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 900},
    {"flightNumber": "FL1204", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Marseille", "departureTime": datetime.strptime('2023-07-02 14:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 950},
    {"flightNumber": "FL1205", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Marseille", "departureTime": datetime.strptime('2023-07-02 16:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 1000},
    # day 3
    {"flightNumber": "FL1301", "departureCity": "Montreal", "arrivalCountry":"France", "arrivalCity":  "Marseille", "departureTime": datetime.strptime('2023-07-03 08:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 800},
    {"flightNumber": "FL1302", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Marseille", "departureTime": datetime.strptime('2023-07-03 10:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 850},
    {"flightNumber": "FL1303", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Marseille", "departureTime": datetime.strptime('2023-07-03 12:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 900},
    {"flightNumber": "FL1304", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Marseille", "departureTime": datetime.strptime('2023-07-03 14:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 950},
    {"flightNumber": "FL1305", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Marseille", "departureTime": datetime.strptime('2023-07-03 16:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 1000},
    #day 4
    {"flightNumber": "FL1401", "departureCity": "Montreal", "arrivalCountry":"France", "arrivalCity":  "Marseille", "departureTime": datetime.strptime('2023-07-04 08:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 800},
    {"flightNumber": "FL1402", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Marseille", "departureTime": datetime.strptime('2023-07-04 10:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 850},
    {"flightNumber": "FL1403", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Marseille", "departureTime": datetime.strptime('2023-07-04 12:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 900},
    {"flightNumber": "FL1404", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Marseille", "departureTime": datetime.strptime('2023-07-04 14:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 950},
    {"flightNumber": "FL1405", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Marseille", "departureTime": datetime.strptime('2023-07-04 16:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 1000},
    #day 5
    {"flightNumber": "FL1501", "departureCity": "Montreal", "arrivalCountry":"France", "arrivalCity":  "Marseille", "departureTime": datetime.strptime('2023-07-05 08:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 800},
    {"flightNumber": "FL1502", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Marseille", "departureTime": datetime.strptime('2023-07-05 10:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 850},
    {"flightNumber": "FL1503", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Marseille", "departureTime": datetime.strptime('2023-07-05 12:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 900},
    {"flightNumber": "FL1504", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Marseille", "departureTime": datetime.strptime('2023-07-05 14:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 950},
    {"flightNumber": "FL1505", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Marseille", "departureTime": datetime.strptime('2023-07-05 16:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 1000},






    #Lyon
    # day 1
    {"flightNumber": "FL2101", "departureCity": "Montreal", "arrivalCountry":"France", "arrivalCity":  "Lyon", "departureTime": datetime.strptime('2023-07-01 08:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 800},
    {"flightNumber": "FL2102", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Lyon", "departureTime": datetime.strptime('2023-07-01 10:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 850},
    {"flightNumber": "FL2103", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Lyon", "departureTime": datetime.strptime('2023-07-01 12:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 900},
    {"flightNumber": "FL2104", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Lyon", "departureTime": datetime.strptime('2023-07-01 14:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 950},
    {"flightNumber": "FL2105", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Lyon", "departureTime": datetime.strptime('2023-07-01 16:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 1000},
    # day 2
    {"flightNumber": "FL2201", "departureCity": "Montreal", "arrivalCountry":"France", "arrivalCity":  "Lyon", "departureTime": datetime.strptime('2023-07-02 08:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 800},
    {"flightNumber": "FL2202", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Lyon", "departureTime": datetime.strptime('2023-07-02 10:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 850},
    {"flightNumber": "FL2203", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Lyon", "departureTime": datetime.strptime('2023-07-02 12:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 900},
    {"flightNumber": "FL2204", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Lyon", "departureTime": datetime.strptime('2023-07-02 14:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 950},
    {"flightNumber": "FL2205", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Lyon", "departureTime": datetime.strptime('2023-07-02 16:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 1000},
    # day 3
    {"flightNumber": "FL2301", "departureCity": "Montreal", "arrivalCountry":"France", "arrivalCity":  "Lyon", "departureTime": datetime.strptime('2023-07-03 08:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 800},
    {"flightNumber": "FL2302", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Lyon", "departureTime": datetime.strptime('2023-07-03 10:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 850},
    {"flightNumber": "FL2303", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Lyon", "departureTime": datetime.strptime('2023-07-03 12:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 900},
    {"flightNumber": "FL2304", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Lyon", "departureTime": datetime.strptime('2023-07-03 14:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 950},
    {"flightNumber": "FL2305", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Lyon", "departureTime": datetime.strptime('2023-07-03 16:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 1000},
    #day 4
    {"flightNumber": "FL2401", "departureCity": "Montreal", "arrivalCountry":"France", "arrivalCity":  "Lyon", "departureTime": datetime.strptime('2023-07-04 08:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 800},
    {"flightNumber": "FL2402", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Lyon", "departureTime": datetime.strptime('2023-07-04 10:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 850},
    {"flightNumber": "FL2403", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Lyon", "departureTime": datetime.strptime('2023-07-04 12:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 900},
    {"flightNumber": "FL2404", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Lyon", "departureTime": datetime.strptime('2023-07-04 14:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 950},
    {"flightNumber": "FL2405", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Lyon", "departureTime": datetime.strptime('2023-07-04 16:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 1000},
    #day 5
    {"flightNumber": "FL2501", "departureCity": "Montreal", "arrivalCountry":"France", "arrivalCity":  "Lyon", "departureTime": datetime.strptime('2023-07-05 08:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 800},
    {"flightNumber": "FL2502", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Lyon", "departureTime": datetime.strptime('2023-07-05 10:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 850},
    {"flightNumber": "FL2503", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Lyon", "departureTime": datetime.strptime('2023-07-05 12:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 900},
    {"flightNumber": "FL2504", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Lyon", "departureTime": datetime.strptime('2023-07-05 14:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 950},
    {"flightNumber": "FL2505", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Lyon", "departureTime": datetime.strptime('2023-07-05 16:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 1000},






    #Nice
    # day 1
    {"flightNumber": "FL3101", "departureCity": "Montreal", "arrivalCountry":"France", "arrivalCity":  "Nice", "departureTime": datetime.strptime('2023-07-01 08:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 800},
    {"flightNumber": "FL3102", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Nice", "departureTime": datetime.strptime('2023-07-01 10:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 850},
    {"flightNumber": "FL3103", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Nice", "departureTime": datetime.strptime('2023-07-01 12:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 900},
    {"flightNumber": "FL3104", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Nice", "departureTime": datetime.strptime('2023-07-01 14:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 950},
    {"flightNumber": "FL3105", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Nice", "departureTime": datetime.strptime('2023-07-01 16:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 1000},
    # day 2
    {"flightNumber": "FL3201", "departureCity": "Montreal", "arrivalCountry":"France", "arrivalCity":  "Nice", "departureTime": datetime.strptime('2023-07-02 08:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 800},
    {"flightNumber": "FL3202", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Nice", "departureTime": datetime.strptime('2023-07-02 10:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 850},
    {"flightNumber": "FL3203", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Nice", "departureTime": datetime.strptime('2023-07-02 12:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 900},
    {"flightNumber": "FL3204", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Nice", "departureTime": datetime.strptime('2023-07-02 14:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 950},
    {"flightNumber": "FL3205", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Nice", "departureTime": datetime.strptime('2023-07-02 16:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 1000},
    # day 3
    {"flightNumber": "FL3301", "departureCity": "Montreal", "arrivalCountry":"France", "arrivalCity":  "Nice", "departureTime": datetime.strptime('2023-07-03 08:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 800},
    {"flightNumber": "FL3302", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Nice", "departureTime": datetime.strptime('2023-07-03 10:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 850},
    {"flightNumber": "FL3303", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Nice", "departureTime": datetime.strptime('2023-07-03 12:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 900},
    {"flightNumber": "FL3304", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Nice", "departureTime": datetime.strptime('2023-07-03 14:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 950},
    {"flightNumber": "FL3305", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Nice", "departureTime": datetime.strptime('2023-07-03 16:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 1000},
    #day 4
    {"flightNumber": "FL3401", "departureCity": "Montreal", "arrivalCountry":"France", "arrivalCity":  "Nice", "departureTime": datetime.strptime('2023-07-04 08:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 800},
    {"flightNumber": "FL3402", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Nice", "departureTime": datetime.strptime('2023-07-04 10:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 850},
    {"flightNumber": "FL3403", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Nice", "departureTime": datetime.strptime('2023-07-04 12:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 900},
    {"flightNumber": "FL3404", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Nice", "departureTime": datetime.strptime('2023-07-04 14:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 950},
    {"flightNumber": "FL3405", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Nice", "departureTime": datetime.strptime('2023-07-04 16:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 1000},
    #day 5
    {"flightNumber": "FL3501", "departureCity": "Montreal", "arrivalCountry":"France", "arrivalCity":  "Nice", "departureTime": datetime.strptime('2023-07-05 08:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 800},
    {"flightNumber": "FL3502", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Nice", "departureTime": datetime.strptime('2023-07-05 10:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 850},
    {"flightNumber": "FL3503", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Nice", "departureTime": datetime.strptime('2023-07-05 12:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 900},
    {"flightNumber": "FL3504", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Nice", "departureTime": datetime.strptime('2023-07-05 14:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 950},
    {"flightNumber": "FL3505", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Nice", "departureTime": datetime.strptime('2023-07-05 16:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 1000},






    #Bordeaux
    # day 1
    {"flightNumber": "FL4101", "departureCity": "Montreal", "arrivalCountry":"France", "arrivalCity":  "Bordeaux", "departureTime": datetime.strptime('2023-07-01 08:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 800},
    {"flightNumber": "FL4102", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Bordeaux", "departureTime": datetime.strptime('2023-07-01 10:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 850},
    {"flightNumber": "FL4103", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Bordeaux", "departureTime": datetime.strptime('2023-07-01 12:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 900},
    {"flightNumber": "FL4104", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Bordeaux", "departureTime": datetime.strptime('2023-07-01 14:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 950},
    {"flightNumber": "FL4105", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Bordeaux", "departureTime": datetime.strptime('2023-07-01 16:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 1000},
    # day 2
    {"flightNumber": "FL4201", "departureCity": "Montreal", "arrivalCountry":"France", "arrivalCity":  "Bordeaux", "departureTime": datetime.strptime('2023-07-02 08:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 800},
    {"flightNumber": "FL4202", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Bordeaux", "departureTime": datetime.strptime('2023-07-02 10:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 850},
    {"flightNumber": "FL4203", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Bordeaux", "departureTime": datetime.strptime('2023-07-02 12:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 900},
    {"flightNumber": "FL4204", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Bordeaux", "departureTime": datetime.strptime('2023-07-02 14:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 950},
    {"flightNumber": "FL4205", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Bordeaux", "departureTime": datetime.strptime('2023-07-02 16:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 1000},
    # day 3
    {"flightNumber": "FL4301", "departureCity": "Montreal", "arrivalCountry":"France", "arrivalCity":  "Bordeaux", "departureTime": datetime.strptime('2023-07-03 08:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 800},
    {"flightNumber": "FL4302", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Bordeaux", "departureTime": datetime.strptime('2023-07-03 10:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 850},
    {"flightNumber": "FL4303", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Bordeaux", "departureTime": datetime.strptime('2023-07-03 12:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 900},
    {"flightNumber": "FL4304", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Bordeaux", "departureTime": datetime.strptime('2023-07-03 14:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 950},
    {"flightNumber": "FL4305", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Bordeaux", "departureTime": datetime.strptime('2023-07-03 16:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 1000},
    #day 4
    {"flightNumber": "FL4401", "departureCity": "Montreal", "arrivalCountry":"France", "arrivalCity":  "Bordeaux", "departureTime": datetime.strptime('2023-07-04 08:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 800},
    {"flightNumber": "FL4402", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Bordeaux", "departureTime": datetime.strptime('2023-07-04 10:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 850},
    {"flightNumber": "FL4403", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Bordeaux", "departureTime": datetime.strptime('2023-07-04 12:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 900},
    {"flightNumber": "FL4404", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Bordeaux", "departureTime": datetime.strptime('2023-07-04 14:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 950},
    {"flightNumber": "FL4405", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Bordeaux", "departureTime": datetime.strptime('2023-07-04 16:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 1000},
    #day 5
    {"flightNumber": "FL4501", "departureCity": "Montreal", "arrivalCountry":"France", "arrivalCity":  "Bordeaux", "departureTime": datetime.strptime('2023-07-05 08:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 800},
    {"flightNumber": "FL4502", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Bordeaux", "departureTime": datetime.strptime('2023-07-05 10:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 850},
    {"flightNumber": "FL4503", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Bordeaux", "departureTime": datetime.strptime('2023-07-05 12:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 900},
    {"flightNumber": "FL4504", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Bordeaux", "departureTime": datetime.strptime('2023-07-05 14:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 950},
    {"flightNumber": "FL4505", "departureCity": "Montreal", "arrivalCountry": "France", "arrivalCity": "Bordeaux", "departureTime": datetime.strptime('2023-07-05 16:00:00', '%Y-%m-%d %H:%M:%S'), "flightPrice": 1000},



    
]



hotels_data = [
    {"hotelName": "Hotel Rome", "cityName": "Rome", "pricePerNight": 150},
    {"hotelName": "Hotel LA","cityName": "Los Angeles", "pricePerNight": 200},
    {"hotelName": "Hotel Berlin","cityName": "Berlin", "pricePerNight": 190},
    {"hotelName": "Hotel Madrid","cityName": "Madrid", "pricePerNight": 160},

    #Paris
    {"hotelName": "Hotel Paris","cityName": "Paris", "pricePerNight": 100},
    {"hotelName": "Hotel Grand","cityName": "Paris", "pricePerNight": 150},
    {"hotelName": "Hotel Delux","cityName": "Paris", "pricePerNight": 200},

    #Marseille
    {"hotelName": "Hotel Marseille","cityName": "Marseille", "pricePerNight": 100},
    {"hotelName": "Hotel Zation","cityName": "Marseille", "pricePerNight": 150},
    {"hotelName": "Hotel Vareghoux","cityName": "Marseille", "pricePerNight": 200},

    #Lyon
    {"hotelName": "Hotel Lyon","cityName": "Lyon", "pricePerNight": 100},
    {"hotelName": "Hotel Benzema","cityName": "Lyon", "pricePerNight": 150},
    {"hotelName": "Hotel De Bruyne","cityName": "Lyon", "pricePerNight": 200},

    #Nice
    {"hotelName": "Hotel Nice","cityName": "Nice", "pricePerNight": 100},
    {"hotelName": "Hotel Lewandowski","cityName": "Nice", "pricePerNight": 150},
    {"hotelName": "Hotel Mbappe","cityName": "Nice", "pricePerNight": 200},

    #Bordeaux
    {"hotelName": "Hotel Bordeaux","cityName": "Bordeaux", "pricePerNight": 100},
    {"hotelName": "Hotel Haaland","cityName": "Bordeaux", "pricePerNight": 150},
    {"hotelName": "Hotel Silva","cityName": "Bordeaux", "pricePerNight": 200},
]





activities_data = [
    {"activityName": "Hiking", "price": 10},
    {"activityName": "Biking", "price": 15},
    {"activityName": "Museum", "price": 20},
    {"activityName": "City Tour", "price": 40},
    {"activityName": "Running around the Hotel", "price": 80},
]

packages_data = [
    {"packageName": "Rome Tour", "daysCount": 5, "flight_id": 1, "hotel_ids": [1], "activity_ids": [1]},
    {"packageName": "LA Tour", "daysCount": 10, "flight_id": 2, "hotel_ids": [2], "activity_ids": [2,3,4,5]},
    {"packageName": "Berlin Tour", "daysCount": 3, "flight_id": 3, "hotel_ids": [3], "activity_ids": [4,1]},
    {"packageName": "Madrid Tour", "daysCount": 4, "flight_id": 4, "hotel_ids": [4], "activity_ids": [5]},
    {"packageName": "Paris Tour", "daysCount": 6, "flight_id": 5, "hotel_ids": [5], "activity_ids": [1,4]},
    {"packageName": "Nice Tour", "daysCount": 7, "flight_id": 30, "hotel_ids": [14], "activity_ids": [4,5]},
]