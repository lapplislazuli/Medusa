#### This File Contains Dictionaries and Helpers ######
## its goal is to make labels human-readble,
## and help us to map gtsrb -> gi Label and vice versa


### Original GTSRB #####
### Yes, its englisch ... ### 
GTSRB_INT_TO_LABEL = {
    0: '20_speed',
    1: '30_speed',
    2: '50_speed',
    3: '60_speed',
    4: '70_speed',
    5: '80_speed',
    6: '80_lifted',
    7: '100_speed',
    8: '120_speed',
    9: 'no_overtaking_general',
    10: 'no_overtaking_trucks',
    11: 'right_of_way_crossing',
    12: 'right_of_way_general',
    13: 'give_way',
    14: 'stop',
    15: 'no_way_general',
    16: 'no_way_trucks',
    17: 'no_way_one_way',
    18: 'attention_general',
    19: 'attention_left_turn',
    20: 'attention_right_turn',
    21: 'attention_curvy',
    22: 'attention_bumpers',
    23: 'attention_slippery',
    24: 'attention_bottleneck',
    25: 'attention_construction',
    26: 'attention_traffic_light',
    27: 'attention_pedestrian',
    28: 'attention_children',
    29: 'attention_bikes',
    30: 'attention_snowflake',
    31: 'attention_deer',
    32: 'lifted_general',
    33: 'turn_right',
    34: 'turn_left',
    35: 'turn_straight',
    36: 'turn_straight_right',
    37: 'turn_straight_left',
    38: 'turn_right_down',
    39: 'turn_left_down',
    40: 'turn_circle',
    41: 'lifted_no_overtaking_general',
    42: 'lifted_no_overtaking_trucks'
}

GTSRB_GERMAN_LABEL_TO_INT = {
	'Zulässige Höchstgeschwindigkeit (20)': 0,
    'Zulässige Höchstgeschwindigkeit (30)': 1,
    "Zulässige Höchstgeschwindigkeit (50)": 2,
    "Zulässige Höchstgeschwindigkeit (60)": 3,
    "Zulässige Höchstgeschwindigkeit (70)": 4,
    "Zulässige Höchstgeschwindigkeit (80)": 5,
    "Ende der zulässigen Höchstgeschwindigkeit (80)": 6, #Nicht sicher
    "Zulässige Höchstgeschwindigkeit (100)": 7,
    "Zulässige Höchstgeschwindigkeit (120)": 8,
    "Überholverbot für Kraftfahrzeuge aller Art": 9,
    "Überholverbot für Kraftfahrzeuge mit einer zulässigen Gesamtmasse über 3,5t": 10,
    "Einmalige Vorfahrt": 11,
    "Vorfahrt": 12,
    "Vorfahrt gewähren": 13,
    "Stop": 14, #Nicht sicher
    "Verbot für Fahrzeuge aller Art": 15,
    "Verbot für Kraftfahrzeuge mit einer zulässigen Gesamtmasse von 3,5t": 16,
    "Verbot der Einfahrt": 17,
    "Gefahrenstelle": 18,
    "Kurve (links)": 19,
    "Kurve (rechts)": 20, 
    "Doppelkurve (zunächst links)": 21,
    "Unebene Fahrbahn": 22,
    "Schleudergefahr bei Nässe oder Schmutz": 23,
    "Verengung der Fahrbahn (rechts)": 24, #Nicht sicher
    "Baustelle": 25,
    "Ampel": 26, #Nicht sicher
    "Fußgänger": 27,
    "Kinder": 28, #Nicht sicher
    "Fahrradfahrer": 29,
    "Glatteis": 30, #Nicht sicher
    "Wildwechsel": 31,
    "Ende aller Streckenverbote": 32,
    "Ausschließlich rechts": 33,
    "Ausschließlich links": 34, #Nicht sicher
    "Ausschließlich geradeaus": 35,
    "Ausschließlich geradeaus und rechts": 36, #Nicht sicher
    "Ausschließlich geradeaus und links": 37, #Nicht sicher
    "Rechts vorbei": 38,
    "Links vorbei": 39,
    "Kreisverkehr": 40,
    "Ende des Überholverbotes für Kraftfahrzeuge aller Art": 41,
    "Ende des Überholverbotes für Kraftfahrzeuge mit einer zulässigen Gesamtmasse über 3,5t": 42
}



### Read from Mongo 
### See Database/GetAllClasses.txt for the simple how-to
MONGO_LBL=[
        "Ende aller Streckenverbote",
        "Gefahrenstelle",
        "Rechts vorbei",
        "Vorfahrt gewähren",
        "Zulässige Höchstgeschwindigkeit (30)",
        "Zulässige Höchstgeschwindigkeit (20)",
        "Zulässige Höchstgeschwindigkeit (50)",
        "Zulässige Höchstgeschwindigkeit (70)",
        "Baustelle",
        "Überholverbot für Kraftfahrzeuge mit einer zulässigen Gesamtmasse über 3,5t",
        "Vorfahrt",
        "Einmalige Vorfahrt",
        "Verbot der Einfahrt",
        "Kurve (links)",
        "Ende des Überholverbotes für Kraftfahrzeuge mit einer zulässigen Gesamtmasse über 3,5t",
        "Verbot für Kraftfahrzeuge mit einer zulässigen Gesamtmasse von 3,5t",
        "Kreisverkehr",
        "Zulässige Höchstgeschwindigkeit (60)",
        "Wildwechsel",
        "Ausschließlich geradeaus",
        "Kurve (rechts)",
        "Schleudergefahr bei Nässe oder Schmutz",
        "Ende des Überholverbotes für Kraftfahrzeuge aller Art",
        "Links vorbei",
        "Fahrradfahrer",
        "Zulässige Höchstgeschwindigkeit (100)",
        "Zulässige Höchstgeschwindigkeit (80)",
        "Ausschließlich rechts",
        "Überholverbot für Kraftfahrzeuge aller Art",
        "Doppelkurve (zunächst links)",
        "Verbot für Fahrzeuge aller Art",
        "Fußgänger",
        "Unebene Fahrbahn"
        ]

