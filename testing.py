import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import plotly.express as px

# Define deviation thresholds for specific equipment
equipment_thresholds = ({
    # Reaction Area
    "3-P-101": {"Driving End Temp": 60, "Driven End Temp": 80, "RMS Velocity (mm/s)": 4},
    "3-P-102-A": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.5},
    "3-P-102-B": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.5},
    "3-P-103-A": {"Driving End Temp": 58, "Driven End Temp": 58, "RMS Velocity (mm/s)": 4},
    "3-P-103-B": {"Driving End Temp": 58, "Driven End Temp": 58, "RMS Velocity (mm/s)": 4},
    "3-P-201": {"Driving End Temp": 65, "Driven End Temp": 65, "RMS Velocity (mm/s)": 4.8},
    "3-P-202": {"Driving End Temp": 63, "Driven End Temp": 63, "RMS Velocity (mm/s)": 4.6},
    "3-P-203": {"Driving End Temp": 50, "Driven End Temp": 50, "RMS Velocity (mm/s)": 4},
    "3-P-204": {"Driving End Temp": 55, "Driven End Temp": 55, "RMS Velocity (mm/s)": 4.5},
    "3-P-205": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.7},
    "3-P-206": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.2},
    "3-P-208": {"Driving End Temp": 59, "Driven End Temp": 59, "RMS Velocity (mm/s)": 4.1},
    "3-P-209": {"Driving End Temp": 61, "Driven End Temp": 61, "RMS Velocity (mm/s)": 4.3},
    "3-P-301-A": {"Driving End Temp": 70, "Driven End Temp": 70, "RMS Velocity (mm/s)": 6},
    "3-P-301-B": {"Driving End Temp": 65, "Driven End Temp": 65, "RMS Velocity (mm/s)": 5.5},
    "3-P-301-C": {"Driving End Temp": 68, "Driven End Temp": 68, "RMS Velocity (mm/s)": 5.8},
    "3-K-101-A": {"Driving End Temp": 58, "Driven End Temp": 58, "RMS Velocity (mm/s)": 4.2},
    "3-K-101-B": {"Driving End Temp": 58, "Driven End Temp": 58, "RMS Velocity (mm/s)": 4.2},
    "3-K-301-A": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.6},
    "3-K-301-B": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.6},
    "3-P-302-A": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.5},
    "3-P-302-B": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.5},
    "3-P-302-C": {"Driving End Temp": 58, "Driven End Temp": 58, "RMS Velocity (mm/s)": 4.3},
    "3-P-303-A": {"Driving End Temp": 57, "Driven End Temp": 57, "RMS Velocity (mm/s)": 4},
    "3-P-303-B": {"Driving End Temp": 57, "Driven End Temp": 57, "RMS Velocity (mm/s)": 4},
    "3-P-304-A": {"Driving End Temp": 58, "Driven End Temp": 58, "RMS Velocity (mm/s)": 4.3},
    "3-P-304-B": {"Driving End Temp": 58, "Driven End Temp": 58, "RMS Velocity (mm/s)": 4.3},
    "3-P-305-A": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.5},
    "3-P-305-B": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.5},
    "3-P-306-A": {"Driving End Temp": 63, "Driven End Temp": 63, "RMS Velocity (mm/s)": 4.8},
    "3-P-306-B": {"Driving End Temp": 63, "Driven End Temp": 63, "RMS Velocity (mm/s)": 4.8},
    "3-M-301": {"Driving End Temp": 65, "Driven End Temp": 65, "RMS Velocity (mm/s)": 5},
    "3-M-201": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.7},
    "3-M-203": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.5},
    "3-M-205": {"Driving End Temp": 61, "Driven End Temp": 61, "RMS Velocity (mm/s)": 4.5},
    "3-M-207": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.4},
    "3-M-209": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.4},
    "3-P-401-A": {"Driving End Temp": 65, "Driven End Temp": 65, "RMS Velocity (mm/s)": 5},
    "3-P-401-B": {"Driving End Temp": 65, "Driven End Temp": 65, "RMS Velocity (mm/s)": 5},
    "3-K-102": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.7},
    "3-K-401": {"Driving End Temp": 64, "Driven End Temp": 64, "RMS Velocity (mm/s)": 4.8},
    "3-K-402": {"Driving End Temp": 64, "Driven End Temp": 64, "RMS Velocity (mm/s)": 4.8},
 # Distillation Area
    "3-P-901-A": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.8},
    "3-P-901-B": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.8},
    "3-P-902-A": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.5},
    "3-P-902-B": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.5},
    "3-P-903-A": {"Driving End Temp": 65, "Driven End Temp": 65, "RMS Velocity (mm/s)": 5},
    "3-P-903-B": {"Driving End Temp": 65, "Driven End Temp": 65, "RMS Velocity (mm/s)": 5},
    "3-P-903-C": {"Driving End Temp": 67, "Driven End Temp": 67, "RMS Velocity (mm/s)": 5.3},
    "3-P-904-A": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.5},
    "3-P-904-B": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.5},
    "3-P-905-A": {"Driving End Temp": 58, "Driven End Temp": 58, "RMS Velocity (mm/s)": 4.2},
    "3-P-905-B": {"Driving End Temp": 58, "Driven End Temp": 58, "RMS Velocity (mm/s)": 4.2},
    "3-P-906-A": {"Driving End Temp": 63, "Driven End Temp": 63, "RMS Velocity (mm/s)": 4.7},
    "3-P-906-B": {"Driving End Temp": 63, "Driven End Temp": 63, "RMS Velocity (mm/s)": 4.7},
    "3-P-907-A": {"Driving End Temp": 64, "Driven End Temp": 64, "RMS Velocity (mm/s)": 4.9},
    "3-P-907-B": {"Driving End Temp": 64, "Driven End Temp": 64, "RMS Velocity (mm/s)": 4.9},
    "3-P-909-A": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.5},
    "3-P-909-B": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.5},
    "3-P-910-A": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.7},
    "3-P-910-B": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.7},
    "3-P-911-A": {"Driving End Temp": 66, "Driven End Temp": 66, "RMS Velocity (mm/s)": 5.2},
    "3-P-911-B": {"Driving End Temp": 66, "Driven End Temp": 66, "RMS Velocity (mm/s)": 5.2},
    "3-P-912-A": {"Driving End Temp": 64, "Driven End Temp": 64, "RMS Velocity (mm/s)": 4.8},
    "3-P-912-B": {"Driving End Temp": 64, "Driven End Temp": 64, "RMS Velocity (mm/s)": 4.8},
    "3-P-914-A": {"Driving End Temp": 58, "Driven End Temp": 58, "RMS Velocity (mm/s)": 4.2},
    "3-P-914-B": {"Driving End Temp": 58, "Driven End Temp": 58, "RMS Velocity (mm/s)": 4.2},
    "3-P-916-A": {"Driving End Temp": 65, "Driven End Temp": 65, "RMS Velocity (mm/s)": 5.1},
    "3-P-916-B": {"Driving End Temp": 65, "Driven End Temp": 65, "RMS Velocity (mm/s)": 5.1},
    "3-P-917": {"Driving End Temp": 63, "Driven End Temp": 63, "RMS Velocity (mm/s)": 4.6},
    "3-K-901": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.5},
    "3-K-1001-A": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.7},
    "3-K-1001-B": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.7},
    "3-K-1001-C": {"Driving End Temp": 63, "Driven End Temp": 63, "RMS Velocity (mm/s)": 4.9},
    "3-P-1001-A": {"Driving End Temp": 64, "Driven End Temp": 64, "RMS Velocity (mm/s)": 4.8},
    "3-P-1001-B": {"Driving End Temp": 64, "Driven End Temp": 64, "RMS Velocity (mm/s)": 4.8},
    "3-P-1001-C": {"Driving End Temp": 65, "Driven End Temp": 65, "RMS Velocity (mm/s)": 5},
    "3-P-1001-D": {"Driving End Temp": 65, "Driven End Temp": 65, "RMS Velocity (mm/s)": 5},
    "3-P-1001-E": {"Driving End Temp": 63, "Driven End Temp": 63, "RMS Velocity (mm/s)": 4.7},
    "3-P-1001-F": {"Driving End Temp": 63, "Driven End Temp": 63, "RMS Velocity (mm/s)": 4.7},
    "3-P-1011": {"Driving End Temp": 64, "Driven End Temp": 64, "RMS Velocity (mm/s)": 4.9},
    "3-P-1101-A": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.7},
    "3-P-1101-B": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.7},
    "3-P-920-A": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.5},
    "3-P-920-B": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.5},
    "3-P-1102-A": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.7},
    "3-P-1102-B": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.7},
    "3-P-1121": {"Driving End Temp": 63, "Driven End Temp": 63, "RMS Velocity (mm/s)": 4.6},
    "3-P-1122": {"Driving End Temp": 63, "Driven End Temp": 63, "RMS Velocity (mm/s)": 4.6},
    "3-P-1201-A": {"Driving End Temp": 65, "Driven End Temp": 65, "RMS Velocity (mm/s)": 5.2},
    "3-P-1201-B": {"Driving End Temp": 65, "Driven End Temp": 65, "RMS Velocity (mm/s)": 5.2},
    "3-P-1202-A": {"Driving End Temp": 64, "Driven End Temp": 64, "RMS Velocity (mm/s)": 4.8},
    "3-P-1202-B": {"Driving End Temp": 64, "Driven End Temp": 64, "RMS Velocity (mm/s)": 4.8},
    "3-RUP-901": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.6},
    "3-RUK-901": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.6},
# Finishing Area
    "3-P-501-A": {"Driving End Temp": 58, "Driven End Temp": 58, "RMS Velocity (mm/s)": 4.2},
    "3-P-501-B": {"Driving End Temp": 58, "Driven End Temp": 58, "RMS Velocity (mm/s)": 4.2},
    "3-P-502-A": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.5},
    "3-P-502-B": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.5},
    "3-P-503-A": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.7},
    "3-P-503-B": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.7},
    "3-P-504-A": {"Driving End Temp": 63, "Driven End Temp": 63, "RMS Velocity (mm/s)": 4.8},
    "3-P-504-B": {"Driving End Temp": 63, "Driven End Temp": 63, "RMS Velocity (mm/s)": 4.8},
    "3-P-601-A": {"Driving End Temp": 65, "Driven End Temp": 65, "RMS Velocity (mm/s)": 5.2},
    "3-P-601-B": {"Driving End Temp": 65, "Driven End Temp": 65, "RMS Velocity (mm/s)": 5.2},
    "3-P-601-C": {"Driving End Temp": 64, "Driven End Temp": 64, "RMS Velocity (mm/s)": 4.9},
    "3-P-601-D": {"Driving End Temp": 64, "Driven End Temp": 64, "RMS Velocity (mm/s)": 4.9},
    "3-P-602-A": {"Driving End Temp": 63, "Driven End Temp": 63, "RMS Velocity (mm/s)": 4.8},
    "3-P-602-B": {"Driving End Temp": 63, "Driven End Temp": 63, "RMS Velocity (mm/s)": 4.8},
    "3-P-602-C": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.7},
    "3-P-602-D": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.7},
    "3-P-603-A": {"Driving End Temp": 61, "Driven End Temp": 61, "RMS Velocity (mm/s)": 4.6},
    "3-P-603-B": {"Driving End Temp": 61, "Driven End Temp": 61, "RMS Velocity (mm/s)": 4.6},
    "3-P-604-A": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.5},
    "3-P-604-B": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.5},
    "3-P-604-C": {"Driving End Temp": 59, "Driven End Temp": 59, "RMS Velocity (mm/s)": 4.4},
    "3-P-604-D": {"Driving End Temp": 59, "Driven End Temp": 59, "RMS Velocity (mm/s)": 4.4},
    "3-P-605-1": {"Driving End Temp": 58, "Driven End Temp": 58, "RMS Velocity (mm/s)": 4.3},
    "3-P-605-2": {"Driving End Temp": 58, "Driven End Temp": 58, "RMS Velocity (mm/s)": 4.3},
    "3-P-606-1": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.7},
    "3-P-606-2": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.7},
    "3-P-607-1": {"Driving End Temp": 61, "Driven End Temp": 61, "RMS Velocity (mm/s)": 4.6},
    "3-P-607-2": {"Driving End Temp": 61, "Driven End Temp": 61, "RMS Velocity (mm/s)": 4.6},
    "3-P-608-1": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.5},
    "3-P-608-2": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.5},
    "3-P-609-1": {"Driving End Temp": 58, "Driven End Temp": 58, "RMS Velocity (mm/s)": 4.3},
    "3-P-609-2": {"Driving End Temp": 58, "Driven End Temp": 58, "RMS Velocity (mm/s)": 4.3},
    "3-P-610-1": {"Driving End Temp": 57, "Driven End Temp": 57, "RMS Velocity (mm/s)": 4.2},
    "3-P-610-2": {"Driving End Temp": 57, "Driven End Temp": 57, "RMS Velocity (mm/s)": 4.2},
    "3-P-611-1": {"Driving End Temp": 63, "Driven End Temp": 63, "RMS Velocity (mm/s)": 4.8},
    "3-P-611-2": {"Driving End Temp": 63, "Driven End Temp": 63, "RMS Velocity (mm/s)": 4.8},
    "3-P-612-1": {"Driving End Temp": 64, "Driven End Temp": 64, "RMS Velocity (mm/s)": 4.9},
    "3-P-612-2": {"Driving End Temp": 64, "Driven End Temp": 64, "RMS Velocity (mm/s)": 4.9},
    "3-K-602-A": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.7},
    "3-K-602-B": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.7},
    "3-K-602-C": {"Driving End Temp": 63, "Driven End Temp": 63, "RMS Velocity (mm/s)": 4.8},
    "3-K-603-1": {"Driving End Temp": 64, "Driven End Temp": 64, "RMS Velocity (mm/s)": 4.9},
    "3-K-603-2": {"Driving End Temp": 64, "Driven End Temp": 64, "RMS Velocity (mm/s)": 4.9},
    "3-K-605-A": {"Driving End Temp": 65, "Driven End Temp": 65, "RMS Velocity (mm/s)": 5.1},
    "3-K-605-B": {"Driving End Temp": 65, "Driven End Temp": 65, "RMS Velocity (mm/s)": 5.1},
    "3-K-605-C": {"Driving End Temp": 64, "Driven End Temp": 64, "RMS Velocity (mm/s)": 4.9},
    "3-K-605-D": {"Driving End Temp": 64, "Driven End Temp": 64, "RMS Velocity (mm/s)": 4.9},
    "3-K-605-E": {"Driving End Temp": 63, "Driven End Temp": 63, "RMS Velocity (mm/s)": 4.8},
    "3-K-605-F": {"Driving End Temp": 63, "Driven End Temp": 63, "RMS Velocity (mm/s)": 4.8},
    "3-K-605-G": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.7},
    "3-K-606-A": {"Driving End Temp": 61, "Driven End Temp": 61, "RMS Velocity (mm/s)": 4.6},
    "3-K-606-B": {"Driving End Temp": 61, "Driven End Temp": 61, "RMS Velocity (mm/s)": 4.6},
    "3-K-606-C": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.5},
    "3-K-606-D": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.5},
    "3-K-606-E": {"Driving End Temp": 59, "Driven End Temp": 59, "RMS Velocity (mm/s)": 4.4},
    "3-K-606-F": {"Driving End Temp": 59, "Driven End Temp": 59, "RMS Velocity (mm/s)": 4.4},
    "3-K-606-G": {"Driving End Temp": 58, "Driven End Temp": 58, "RMS Velocity (mm/s)": 4.3},
    "3-K-701-A": {"Driving End Temp": 63, "Driven End Temp": 63, "RMS Velocity (mm/s)": 4.8},
    "3-K-701-B": {"Driving End Temp": 63, "Driven End Temp": 63, "RMS Velocity (mm/s)": 4.8},
    "3-K-701-C": {"Driving End Temp": 64, "Driven End Temp": 64, "RMS Velocity (mm/s)": 4.9},
    "3-K-701-D": {"Driving End Temp": 64, "Driven End Temp": 64, "RMS Velocity (mm/s)": 4.9},
    "3-K-701-E": {"Driving End Temp": 65, "Driven End Temp": 65, "RMS Velocity (mm/s)": 5},
    "3-K-701-F": {"Driving End Temp": 65, "Driven End Temp": 65, "RMS Velocity (mm/s)": 5},
    "3-K-704-A": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.7},
    "3-K-704-B": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.7},
    "3-K-801-A": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.5},
    "3-K-801-B": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.5},
    "3-K-802-A": {"Driving End Temp": 63, "Driven End Temp": 63, "RMS Velocity (mm/s)": 4.8},
    "3-K-802-B": {"Driving End Temp": 63, "Driven End Temp": 63, "RMS Velocity (mm/s)": 4.8},
    "3-K-802-C": {"Driving End Temp": 64, "Driven End Temp": 64, "RMS Velocity (mm/s)": 4.9},
    "3-M-501": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.7},
    "3-M-502": {"Driving End Temp": 61, "Driven End Temp": 61, "RMS Velocity (mm/s)": 4.6},
    "3-M-503": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.5},
    "3-M-504": {"Driving End Temp": 58, "Driven End Temp": 58, "RMS Velocity (mm/s)": 4.3},
    "3-M-505": {"Driving End Temp": 63, "Driven End Temp": 63, "RMS Velocity (mm/s)": 4.8},
 # Butene Area
    "2-P-2101-A": {"Driving End Temp": 55, "Driven End Temp": 55, "RMS Velocity (mm/s)": 3.8},
    "2-P-2101-B": {"Driving End Temp": 55, "Driven End Temp": 55, "RMS Velocity (mm/s)": 3.8},
    "2-P-2301-A": {"Driving End Temp": 58, "Driven End Temp": 58, "RMS Velocity (mm/s)": 4.2},
    "2-P-2301-B": {"Driving End Temp": 58, "Driven End Temp": 58, "RMS Velocity (mm/s)": 4.2},
    "2-P-2302-A": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.5},
    "2-P-2302-B": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.5},
    "2-P-2306-A": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.7},
    "2-P-2306-B": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.7},
    "2-P-2201-A": {"Driving End Temp": 63, "Driven End Temp": 63, "RMS Velocity (mm/s)": 4.8},
    "2-P-2201-B": {"Driving End Temp": 63, "Driven End Temp": 63, "RMS Velocity (mm/s)": 4.8},
    "2-P-2202-A": {"Driving End Temp": 64, "Driven End Temp": 64, "RMS Velocity (mm/s)": 4.9},
    "2-P-2202-B": {"Driving End Temp": 64, "Driven End Temp": 64, "RMS Velocity (mm/s)": 4.9},
    "2-P-2203-A": {"Driving End Temp": 65, "Driven End Temp": 65, "RMS Velocity (mm/s)": 5.0},
    "2-P-2203-B": {"Driving End Temp": 65, "Driven End Temp": 65, "RMS Velocity (mm/s)": 5.0},
    "2-P-2304-A": {"Driving End Temp": 63, "Driven End Temp": 63, "RMS Velocity (mm/s)": 4.8},
    "2-P-2304-B": {"Driving End Temp": 63, "Driven End Temp": 63, "RMS Velocity (mm/s)": 4.8},
    "2-P-2305-A": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.7},
    "2-P-2305-B": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.7},
    "2-P-2401-A": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.5},
    "2-P-2401-B": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.5},
    "2-P-2601-A": {"Driving End Temp": 58, "Driven End Temp": 58, "RMS Velocity (mm/s)": 4.3},
    "2-P-2601-B": {"Driving End Temp": 58, "Driven End Temp": 58, "RMS Velocity (mm/s)": 4.3},
    "2-P-2701": {"Driving End Temp": 57, "Driven End Temp": 57, "RMS Velocity (mm/s)": 4.2},
    "2-P-2501-A": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.7},
    "2-P-2501-B": {"Driving End Temp": 62, "Driven End Temp": 62, "RMS Velocity (mm/s)": 4.7},
    "2-P-2502-A": {"Driving End Temp": 61, "Driven End Temp": 61, "RMS Velocity (mm/s)": 4.6},
    "2-P-2502-B": {"Driving End Temp": 61, "Driven End Temp": 61, "RMS Velocity (mm/s)": 4.6},
    "2-P-2602-A": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.5},
    "2-P-2602-B": {"Driving End Temp": 60, "Driven End Temp": 60, "RMS Velocity (mm/s)": 4.5},
    "2-P-2303-A": {"Driving End Temp": 58, "Driven End Temp": 58, "RMS Velocity (mm/s)": 4.3},
    "2-P-2303-B": {"Driving End Temp": 58, "Driven End Temp": 58, "RMS Velocity (mm/s)": 4.3},
})
# Define the file path at the top of the script
file_path = "condition_data.csv"

# Ensure the file exists or create it with a default structure
if not os.path.exists(file_path):
    # Define a default structure
    default_data = pd.DataFrame(columns=[
        "Date", "Area", "Equipment", "Is Running", "Driving End Temp",
        "Driven End Temp", "Oil Level", "Abnormal Sound", "Leakage",
        "Observation", "RMS Velocity (mm/s)", "Peak Acceleration (g)",
        "Displacement (µm)", "Gearbox Temp", "Gearbox Oil Level",
        "Gearbox Leakage", "Gearbox Abnormal Sound", "Gearbox RMS Velocity (mm/s)",
        "Gearbox Peak Acceleration (g)", "Gearbox Displacement (µm)"
    ])
    default_data.to_csv(file_path, index=False)

# Load data from the file
def load_data(file_path):
    if not os.path.exists(file_path):
        return pd.DataFrame()  # Return an empty DataFrame if the file is missing
    return pd.read_csv(file_path)

# Add Utility Functions Here
def calculate_kpis(file_path):
    """Calculate KPIs and return data for charts."""
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        st.warning(f"No data file found at {file_path}. Showing default KPI values.")
        return {
            "compliance_rate": "No Data",
            "avg_temp": "No Data",
            "running_percentage": "No Data",
            "data": pd.DataFrame()  # Return an empty DataFrame for charts
        }

    # Load the CSV file
    data = pd.read_csv(file_path)
    if data.empty:
        st.warning("The data file is empty. Showing default KPI values.")
        return {
            "compliance_rate": "No Data",
            "avg_temp": "No Data",
            "running_percentage": "No Data",
            "data": pd.DataFrame()  # Return an empty DataFrame for charts
        }

    # Calculate KPIs
    compliance_rate = data["Is Running"].mean() * 100
    avg_temp = data[["Driving End Temp", "Driven End Temp"]].mean().mean()
    running_percentage = (data["Is Running"].sum() / len(data)) * 100

    # Return KPIs and data
    return {
        "compliance_rate": f"{compliance_rate:.2f}%",
        "avg_temp": f"{avg_temp:.2f}°C",
        "running_percentage": f"{running_percentage:.2f}%",
        "data": data
    }

# Set page title
st.set_page_config(page_title="Indorama Petrochemicals Ltd", layout="wide")

# Main Page Functionality
if "page" not in st.session_state:
    st.session_state.page = "main"

if st.session_state.page == "main":
        #Main Page
    st.title("INDORAMA PETROCHEMICALS LTD")
    st.subheader("Your Gateway to Enhanced Maintenance Efficiency")

    # Footer Section
    st.write("---")  # Separator line
    st.write("### 📜 Footer Information")

    st.write("""
        - **Application Version**: 1.0.0  
        - **Developer**: [Nwaoba Kenneth / PE Mechanical]  
        - **Contact Support**: [nwaoba00@gmail.com](mailto:support@yourcompany.com)
        """)

    st.write("""
        This application is designed to improve condition monitoring and maintenance tracking for Indorama Petrochemicals Ltd.
        For assistance or feedback, please reach out via the support link above.
        """)


    # Greeting Based on Time
    current_hour = datetime.now().hour
    if current_hour < 12:
        greeting = "Good Morning!"
    elif 12 <= current_hour < 18:
        greeting = "Good Afternoon!"
    else:
        greeting = "Good Evening!"

    st.header(greeting)

    # Display KPIs
    st.subheader("Key Performance Indicators (KPIs)")
    kpis = calculate_kpis(file_path)
    col1, col2, col3 = st.columns(3)
    col1.metric("Compliance Rate", kpis["compliance_rate"])
    col2.metric("Average Temperature", kpis["avg_temp"])
    col3.metric("Running Equipment", kpis["running_percentage"])

    # Function to check for deviations
    def check_deviations(data, equipment_thresholds):
        """
        Identify equipment with deviations exceeding thresholds.
        """
        deviations = []
        for _, row in data.iterrows():
            equipment = row["Equipment"]
            if equipment in equipment_thresholds:
                thresholds = equipment_thresholds[equipment]
                if (
                        row["Driving End Temp"] > thresholds["Driving End Temp"] or
                        row["Driven End Temp"] > thresholds["Driven End Temp"] or
                        row["RMS Velocity (mm/s)"] > thresholds["RMS Velocity (mm/s)"]
                ):
                    deviations.append(row)
        return pd.DataFrame(deviations)

    # Function to detect weekly deviations and generate a report
    def detect_weekly_deviations(file_path, equipment_thresholds, start_date, end_date):
        """
        Detect significant deviations for the current week and generate a printable report.
        """
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            return pd.DataFrame(), "No data available for analysis."

        data = pd.read_csv(file_path)
        if data.empty:
            return pd.DataFrame(), "No data available for analysis."

        # Convert Date column to datetime and filter data
        data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
        data = data.dropna(subset=["Date"])  # Drop rows with invalid dates
        filtered_data = data[(data["Date"] >= pd.to_datetime(start_date)) & (data["Date"] <= pd.to_datetime(end_date))]

        if filtered_data.empty:
            return pd.DataFrame(), "No significant deviations detected for the selected week."

        deviations = []

        # Check for deviations based on thresholds
        grouped = filtered_data.groupby("Equipment")
        for equipment, group in grouped:
            if equipment in equipment_thresholds:
                thresholds = equipment_thresholds[equipment]
                if (
                        (group["Driving End Temp"] > thresholds["Driving End Temp"]).any()
                        or (group["Driven End Temp"] > thresholds["Driven End Temp"]).any()
                        or (group["RMS Velocity (mm/s)"] > thresholds["RMS Velocity (mm/s)"]).any()
                ):
                    deviations.append(group)

        deviation_data = pd.concat(deviations) if deviations else pd.DataFrame()

        if deviation_data.empty:
            return pd.DataFrame(), "All equipment is operating within defined thresholds for the week."

        return deviation_data, "Major deviations detected for the selected week."


    # Weekly Report and AI Insights Section
    st.subheader("Weekly Report and Insights")

    # Unique keys for date inputs
    start_date = st.date_input(
        "Select Start Date",
        value=datetime.now() - timedelta(days=7),
        key="weekly_report_start_date",
    )
    end_date = st.date_input(
        "Select End Date",
        value=datetime.now(),
        key="weekly_report_end_date",
    )

    # Generate report button
    if st.button("Generate Weekly Report with Insights", key="generate_ai_weekly_report_button"):
        deviation_data, message = detect_weekly_deviations(file_path, equipment_thresholds, start_date, end_date)

        # Display message
        st.write(message)

        if not deviation_data.empty:
            # Show deviation table
            st.subheader("Equipment with Major Deviations")
            st.dataframe(deviation_data)

            # Downloadable Report
            st.write("#### Download Weekly Report")
            csv = deviation_data.to_csv(index=False)
            st.download_button("Download Report as CSV", data=csv, file_name="weekly_report.csv", mime="text/csv")

            # AI Insights Based on Weekly Data
            st.write("## Insights & Recommendations")
            recommendations = []
            for _, row in deviation_data.iterrows():
                equipment = row["Equipment"]

                # Example AI recommendation rules
                if "Driving End Temp" in deviation_data.columns and row["Driving End Temp"] > equipment_thresholds.get(
                        equipment, {}).get("Driving End Temp", float('inf')):
                    recommendations.append(
                        f"🔧 **{equipment}**: Driving End Temp exceeds threshold. Maintenance recommended.")

                if "Oil Level" in deviation_data.columns and row["Oil Level"] == "Low":
                    recommendations.append(f"🛢️ **{equipment}**: Oil level is low. Consider refilling.")

                if "RMS Velocity (mm/s)" in deviation_data.columns and row[
                    "RMS Velocity (mm/s)"] > equipment_thresholds.get(equipment, {}).get("RMS Velocity (mm/s)",
                                                                                         float('inf')):
                    recommendations.append(f"📊 **{equipment}**: High vibration detected. Inspect for potential issues.")

            # Display recommendations
            if recommendations:
                st.write("### 🔍 Recommendations Based on Weekly Data")
                for rec in recommendations:
                    st.info(rec)
            else:
                st.success(
                    "✅ No immediate issues detected in the weekly data. All equipment operating within thresholds.")
        else:
            st.warning("No significant deviations detected for the selected week.")


    # Ensure data is available from KPI calculation
    data = kpis["data"]

    if not data.empty:  # Check if the data is available
        st.write("---")
        st.subheader("Running Equipment by Area")

        # Calculate the percentage of running equipment per area
        if "Area" in data.columns and "Is Running" in data.columns:
            running_percentage_by_area = (
                    data.groupby("Area")["Is Running"].mean() * 100
            ).reset_index()
            running_percentage_by_area.rename(
                columns={"Is Running": "Running Percentage (%)"}, inplace=True
            )

            # Display the table
            st.table(running_percentage_by_area)
        else:
            st.warning("The dataset does not contain 'Area' or 'Is Running' columns.")
    else:
        st.warning("No data available to calculate running equipment percentages.")

    # Add KPI Charts
    data = kpis["data"]
    if not data.empty:  # Check if data is available
        st.write("---")
        st.subheader("KPI Charts")

        import plotly.express as px

        # Average Temperature Trend
        if "Driving End Temp" in data.columns and "Driven End Temp" in data.columns:
            # Calculate the average temperature
            data["Avg Temp"] = data[["Driving End Temp", "Driven End Temp"]].mean(axis=1)

            # Aggregate average temperature by date
            avg_temp_trend = data.groupby("Date", as_index=False)["Avg Temp"].mean()

            st.write("### Average Temperature Trend")

            # Create a Plotly line chart
            fig = px.line(
                avg_temp_trend,
                x="Date",
                y="Avg Temp",
                title="Average Temperature Trend Over Time",
                labels={"Avg Temp": "Average Temperature (°C)", "Date": "Date"},
                markers=True,  # Adds markers for each data point
            )

            # Enhance chart aesthetics
            fig.update_traces(line=dict(width=2))
            fig.update_layout(
                title_font_size=18,
                xaxis_title_font_size=14,
                yaxis_title_font_size=14,
                hovermode="x unified",  # Combine hover info
            )

            st.plotly_chart(fig)
        else:
            st.warning("Temperature data (Driving End or Driven End) is missing in the dataset.")


        # Running Equipment Count
        if "Is Running" in data.columns and "Area" in data.columns:
            running_equipment_by_area = data.groupby(["Date", "Area"])["Is Running"].sum().reset_index()
            st.write("### Running Equipment Count by Area")

            # Create the bar chart with Plotly
            fig = px.bar(
                running_equipment_by_area,
                x="Date",
                y="Is Running",
                color="Area",
                title="Running Equipment Count by Area",
                labels={"Is Running": "Running Equipment Count"},
            )
            fig.update_layout(barmode="stack")
            st.plotly_chart(fig)
        else:
            st.warning("The dataset does not contain 'Is Running' or 'Area' columns.")

    else:
        st.warning("No data available for KPI charts.")


    # Next Button to Navigate
    if st.button("Next"):
        st.session_state.page = "monitoring"

elif st.session_state.page == "monitoring":

    def load_data(file_path):
        """Load data from a CSV file."""
        if not os.path.exists(file_path):
            return pd.DataFrame()  # Return an empty DataFrame if file doesn't exist
        return pd.read_csv(file_path)


    def filter_data(df, equipment, start_date, end_date):
        """Filter data by equipment and date range."""
        df["Date"] = pd.to_datetime(df["Date"])  # Convert Date column to datetime
        filtered_df = df[
            (df["Equipment"] == equipment) &
            (df["Date"] >= pd.to_datetime(start_date)) &
            (df["Date"] <= pd.to_datetime(end_date))
            ]
        return filtered_df

    # Tabs for Condition Monitoring and Report
    tab1, tab2 = st.tabs(["Condition Monitoring", "Report"])

    with tab1:
        st.header("Condition Monitoring Data Entry")

        # Equipment lists for each area
        equipment_lists = {
            "Reaction": [
                "3-P-101", "3-P-102-A", "3-P-102-B", "3-P-103-A", "3-P-103-B",
                "3-P-201", "3-P-202", "3-P-203", "3-P-204", "3-P-205", "3-P-206",
                "3-P-208", "3-P-209", "3-P-301-A", "3-P-301-B", "3-P-301-C",
                "3-K-101-A", "3-K-101-B", "3-K-301-A", "3-K-301-B", "3-P-301-A",
                "3-P-301-B", "3-P-301-C", "3-P-302-A", "3-P-302-B", "3-P-302-C",
                "3-P-303-A", "3-P-303-B", "3-P-304-A", "3-P-304-B", "3-P-305-A",
                "3-P-305-B", "3-P-306-A", "3-P-306-B", "3-M-301", "3-M-201",
                "3-M-203", "3-M-205", "3-M-207", "3-M-209", "3-P-401-A", "3-P-401-B", "3-K-102", "3-K-401", "3-K-402"
            ],
            "Distillation": [
                "3-P-901-A", "3-P-901-B", "3-P-902-A", "3-P-902-B", "3-P-903-A",
                "3-P-903-B", "3-P-903-C", "3-P-904-A", "3-P-904-B", "3-P-905-A",
                "3-P-905-B", "3-P-906-A", "3-P-906-B", "3-P-907-A", "3-P-907-B",
                "3-P-909-A", "3-P-909-B", "3-P-910-A", "3-P-910-B", "3-P-911-A",
                "3-P-911-B", "3-P-912-A", "3-P-912-B", "3-P-914-A", "3-P-914-B",
                "3-P-916-A", "3-P-916-B", "3-P-917", "3-K-901", "3-K-1001-A",
                "3-K-1001-B", "3-K-1001-C", "3-P-1001-A", "3-P-1001-B", "3-P-1001-C",
                "3-P-1001-D", "3-P-1001-E", "3-P-1001-F", "3-P-1011", "3-P-1101-A",
                "3-P-1101-B", "3-P-920-A", "3-P-920-B", "3-P-1102-A", "3-P-1102-B",
                "3-P-1121", "3-P-1122", "3-P-1201-A", "3-P-1201-B", "3-P-1202-A",
                "3-P-1202-B", "3-RUP-901", "3-RUK-901"
            ],
            "Finishing": [
                "3-P-501-A", "3-P-501-B", "3-P-502-A", "3-P-502-B", "3-P-503-A",
                "3-P-503-B", "3-P-504-A", "3-P-504-B", "3-P-601-A", "3-P-601-B",
                "3-P-601-C", "3-P-601-D", "3-P-602-A", "3-P-602-B", "3-P-602-C",
                "3-P-602-D", "3-P-603-A", "3-P-603-B", "3-P-604-A", "3-P-604-B",
                "3-P-604-C", "3-P-604-D", "3-P-605-1", "3-P-605-2", "3-P-606-1",
                "3-P-606-2", "3-P-607-1", "3-P-607-2", "3-P-608-1", "3-P-608-2",
                "3-P-609-1", "3-P-609-2", "3-P-610-1", "3-P-610-2", "3-P-611-1",
                "3-P-611-2", "3-P-612-1", "3-P-612-2", "3-K-602-A", "3-K-602-B",
                "3-K-602-C", "3-K-603-1", "3-K-603-2", "3-K-605-A", "3-K-605-B",
                "3-K-605-C", "3-K-605-D", "3-K-605-E", "3-K-605-F", "3-K-605-G",
                "3-K-606-A", "3-K-606-B", "3-K-606-C", "3-K-606-D", "3-K-606-E",
                "3-K-606-F", "3-K-606-G", "3-K-701-A", "3-K-701-B", "3-K-701-C",
                "3-K-701-D", "3-K-701-E", "3-K-701-F", "3-K-704-A", "3-K-704-B",
                "3-K-801-A", "3-K-801-B", "3-K-802-A", "3-K-802-B", "3-K-802-C",
                "3-M-501", "3-M-502", "3-M-503", "3-M-504", "3-M-505"
            ],
            "Butene": [
                "2-P-2101-A", "2-P-2101-B", "2-P-2301-A", "2-P-2301-B",
                "2-P-2302-A", "2-P-2302-B", "2-P-2306-A", "2-P-2306-B",
                "2-P-2201-A", "2-P-2201-B", "2-P-2202-A", "2-P-2202-B",
                "2-P-2203-A", "2-P-2203-B", "2-P-2304-A", "2-P-2304-B",
                "2-P-2305-A", "2-P-2305-B", "2-P-2401-A", "2-P-2401-B",
                "2-P-2601-A", "2-P-2601-B", "2-P-2701", "2-P-2501-A",
                "2-P-2501-B", "2-P-2502-A", "2-P-2502-B", "2-P-2602-A",
                "2-P-2602-B", "2-P-2303-A", "2-P-2303-B"
            ]
        }

        # Persistent fields
        date = st.date_input("Date", key="date")
        area = st.selectbox("Select Area", options=list(equipment_lists.keys()), key="area")
        equipment_options = equipment_lists.get(area, [])
        equipment = st.selectbox("Select Equipment", options=equipment_options, key="equipment")


        # Tick box for "Is the equipment running?"
        is_running = st.checkbox("Is the equipment running?", key="is_running")

        # Data Entry Fields
        if is_running:
            de_temp = st.number_input("Driving End Temperature (°C)", min_value=0.0, max_value=200.0, step=0.1,
                                      key="de_temp")
            dr_temp = st.number_input("Driven End Temperature (°C)", min_value=0.0, max_value=200.0, step=0.1,
                                      key="dr_temp")
            oil_level = st.selectbox("Oil Level", ["Normal", "Low", "High"], key="oil_level")
            abnormal_sound = st.selectbox("Abnormal Sound", ["No", "Yes"], key="abnormal_sound")
            leakage = st.selectbox("Leakage", ["No", "Yes"], key="leakage")
            observation = st.text_area("Observations", key="observation")

            # Vibration Monitoring
            st.subheader("Vibration Monitoring")
            vibration_rms_velocity = st.number_input("RMS Velocity (mm/s)", min_value=0.0, max_value=100.0, step=0.1,
                                                     key="vibration_rms_velocity")
            vibration_peak_acceleration = st.number_input("Peak Acceleration (g)", min_value=0.0, max_value=10.0,
                                                          step=0.1,
                                                          key="vibration_peak_acceleration")
            vibration_displacement = st.number_input("Displacement (µm)", min_value=0.0, max_value=1000.0, step=0.1,
                                                     key="vibration_displacement")

            # Gearbox Inputs
            gearbox = st.checkbox("Does the equipment have a gearbox?", key="gearbox")
            if gearbox:
                gearbox_temp = st.number_input("Gearbox Temperature (°C)", min_value=0.0, max_value=200.0, step=0.1,
                                               key="gearbox_temp")
                gearbox_oil = st.selectbox("Gearbox Oil Level", ["Normal", "Low", "High"], key="gearbox_oil")
                gearbox_leakage = st.selectbox("Gearbox Leakage", ["No", "Yes"], key="gearbox_leakage")
                gearbox_abnormal_sound = st.selectbox("Gearbox Abnormal Sound", ["No", "Yes"], key="gearbox_abnormal_sound")
                # Vibration Monitoring for gearbox
                st.subheader("Gearbox_Vibration Monitoring")
                gearbox_vibration_rms_velocity = st.number_input("Gearbox RMS Velocity (mm/s)", min_value=0.0, max_value=100.0,
                                                         step=0.1,
                                                         key="gearbox_vibration_rms_velocity")
                gearbox_vibration_peak_acceleration = st.number_input("Gearbox Peak Acceleration (g)", min_value=0.0, max_value=10.0,
                                                              step=0.1,
                                                              key="gearbox_vibration_peak_acceleration")
                gearbox_vibration_displacement = st.number_input("Gearbox Displacement (µm)", min_value=0.0, max_value=1000.0, step=0.1,
                                                         key="gearbox_vibration_displacement")

        # Submit Button
        if st.button("Submit Data"):
            try:
                # Check if essential fields are filled (add your required fields here)
                if not date or not area or not equipment:
                    st.error("Please fill in all required fields before submitting.")
                elif is_running and ("de_temp" not in st.session_state or "dr_temp" not in st.session_state):
                    st.error("Please provide temperature values if the equipment is running.")
                else:
                    # Prepare data
                    if not is_running:
                        # If equipment is not running, set all numeric fields to 0 and strings to 'N/A'
                        data = {
                            "Date": [date],
                            "Area": [area],
                            "Equipment": [equipment],
                            "Is Running": [False],
                            "Driving End Temp": [0.0],
                            "Driven End Temp": [0.0],
                            "Oil Level": ["N/A"],
                            "Abnormal Sound": ["N/A"],
                            "Leakage": ["N/A"],
                            "Observation": ["Not Running"],
                            "RMS Velocity (mm/s)": [0.0],
                            "Peak Acceleration (g)": [0.0],
                            "Displacement (µm)": [0.0],
                            "Gearbox Temp": [0.0],
                            "Gearbox Oil Level": ["N/A"],
                            "Gearbox Leakage": ["N/A"],
                            "Gearbox Abnormal Sound": ["N/A"],
                            "Gearbox RMS Velocity (mm/s)": [0.0],
                            "Gearbox Peak Acceleration (g)": [0.0],
                            "Gearbox Displacement (µm)": [0.0],
                        }

                    else:
                        # If equipment is running, save entered values
                        data = {
                            "Date": [date],
                            "Area": [area],
                            "Equipment": [equipment],
                            "Is Running": [True],
                            "Driving End Temp": [st.session_state.de_temp],
                            "Driven End Temp": [st.session_state.dr_temp],
                            "Oil Level": [st.session_state.oil_level],
                            "Abnormal Sound": [st.session_state.abnormal_sound],
                            "Leakage": [st.session_state.leakage],
                            "Observation": [st.session_state.observation],
                            "RMS Velocity (mm/s)": [st.session_state.vibration_rms_velocity],
                            "Peak Acceleration (g)": [st.session_state.vibration_peak_acceleration],
                            "Displacement (µm)": [st.session_state.vibration_displacement],
                            "Gearbox Temp": [
                                st.session_state.gearbox_temp if "gearbox_temp" in st.session_state else 0.0],
                            "Gearbox Oil Level": [
                                st.session_state.gearbox_oil if "gearbox_oil" in st.session_state else "N/A"],
                            "Gearbox Leakage": [
                                st.session_state.gearbox_leakage if "gearbox_leakage" in st.session_state else "N/A"],
                            "Gearbox Abnormal Sound": [
                                st.session_state.gearbox_leakage if "gearbox_abnormal_sound" in st.session_state else "N/A"]
                        }

                    # Save to CSV
                    df = pd.DataFrame(data)
                    file_path = "condition_data.csv"
                    if not os.path.exists("data"):
                        os.makedirs("data")
                    if os.path.exists(file_path):
                        df.to_csv(file_path, mode="a", header=False, index=False)
                    else:
                        df.to_csv(file_path, index=False)

                    st.success("Data Submitted Successfully!")

            except Exception as e:
                st.error(f"An error occurred: {e}")

    # Tab 2: Reports and Visualizations
    with tab2:
        st.header("Reports and Visualization")
        file_path = "condition_data.csv"

        # Load data
        data = load_data(file_path)

        if data.empty:
            st.warning("No data available. Please enter condition monitoring data first.")
        else:
            st.write("### Full Data")
            st.dataframe(data)

            # Check if 'Equipment' column exists
            if "Equipment" not in data.columns:
                st.error("The 'Equipment' column is missing. Please check the data file.")
            else:
                # Combine all equipment into a single list
                all_equipment = [equipment for area in equipment_lists.values() for equipment in area]

                # Dropdown for Equipment Selection
                selected_equipment = st.selectbox("Select Equipment", options=all_equipment)

                # Date Range Inputs
                start_date = st.date_input("Start Date", value=datetime(2023, 1, 1))
                end_date = st.date_input("End Date", value=datetime.now())

                if start_date > end_date:
                    st.error("Start date cannot be later than end date.")
                else:
                    # Filter data for the selected equipment and date range
                    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
                    data = data.dropna(subset=["Date"])  # Remove invalid dates
                    filtered_data = data[
                        (data["Equipment"] == selected_equipment) &
                        (data["Date"] >= pd.to_datetime(start_date)) &
                        (data["Date"] <= pd.to_datetime(end_date))
                        ]

                    # Check if filtered data is empty
                    if filtered_data.empty:
                        st.warning(f"No data found for {selected_equipment} between {start_date} and {end_date}.")
                        st.write(f"### {selected_equipment} Report")
                        st.write("The equipment hasn't been running during the selected date range.")
                    else:
                        st.write(f"### Filtered Data for {selected_equipment}")
                        st.dataframe(filtered_data)

                        # Visualizations
                        st.subheader("Data Visualizations")

                        # Allow user to choose the dataset for visualization
                        data_option = st.radio(
                            "Select data for visualization:",
                            options=["General Table (All Data)", "Filtered Table"],
                            key="data_option"
                        )

                        # Select appropriate dataset based on user choice
                        if data_option == "General Table (All Data)":
                            visualization_data = data  # Use the full dataset
                            st.write("Using data from the general table (all records).")
                        else:
                            visualization_data = filtered_data  # Use the filtered dataset
                            st.write("Using data from the filtered table.")

                        # Driving and Driven End Temperature Trend
                        if "Driving End Temp" in visualization_data.columns and "Driven End Temp" in visualization_data.columns:
                            st.write("#### Driving and Driven End Temperature Trend for Equipment")
                            temp_chart_data = visualization_data[["Date", "Driving End Temp", "Driven End Temp"]].melt(
                                id_vars="Date",
                                var_name="Temperature Type",
                                value_name="Temperature")
                            fig = px.line(
                                temp_chart_data,
                                x="Date",
                                y="Temperature",
                                color="Temperature Type",
                                title="Driving and Driven End Temperature Trend",
                                labels={"Temperature": "Temperature (°C)"}
                            )
                            st.plotly_chart(fig)
                        else:
                            st.warning(
                                "Temperature data (Driving End or Driven End) is missing in the selected dataset.")

                        # Equipment Vibration Trend
                        if "RMS Velocity (mm/s)" in visualization_data.columns and "Peak Acceleration (g)" in visualization_data.columns and "Displacement (µm)" in visualization_data.columns:
                            st.write("#### Vibration Trend for Equipment")
                            vibration_chart_data = visualization_data[
                                ["Date", "RMS Velocity (mm/s)", "Peak Acceleration (g)", "Displacement (µm)"]].melt(
                                id_vars="Date",
                                var_name="Vibration Type",
                                value_name="Value")
                            fig = px.line(
                                vibration_chart_data,
                                x="Date",
                                y="Value",
                                color="Vibration Type",
                                title="Vibration Trend for Equipment",
                                labels={"Value": "Value"}
                            )
                            st.plotly_chart(fig)
                        else:
                            st.warning("Vibration data is missing in the selected dataset.")

                        # Driving and Driven End Temperature Trend for Gearbox
                        if "Gearbox Temp" in visualization_data.columns:
                            st.write("#### Gearbox Temperature Trend")
                            fig = px.line(
                                visualization_data,
                                x="Date",
                                y="Gearbox Temp",
                                title="Gearbox Temperature Trend",
                                labels={"Gearbox Temp": "Temperature (°C)"}
                            )
                            st.plotly_chart(fig)
                        else:
                            st.warning("Gearbox Temperature data is missing in the selected dataset.")

                        # Equipment Vibration Trend for Gearbox
                        if "Gearbox RMS Velocity (mm/s)" in visualization_data.columns and "Gearbox Peak Acceleration (g)" in visualization_data.columns and "Gearbox Displacement (µm)" in visualization_data.columns:
                            st.write("#### Vibration Trend for Gearbox")
                            gearbox_vibration_chart_data = visualization_data[
                                ["Date", "Gearbox RMS Velocity (mm/s)", "Gearbox Peak Acceleration (g)",
                                 "Gearbox Displacement (µm)"]].melt(id_vars="Date",
                                                                    var_name="Vibration Type",
                                                                    value_name="Value")
                            fig = px.line(
                                gearbox_vibration_chart_data,
                                x="Date",
                                y="Value",
                                color="Vibration Type",
                                title="Vibration Trend for Gearbox",
                                labels={"Value": "Value"}
                            )
                            st.plotly_chart(fig)
                        else:
                            st.warning("Gearbox Vibration data is missing in the selected dataset.")

                        # Oil Level Distribution for Equipment
                        if "Oil Level" in visualization_data.columns:
                            st.write("#### Oil Level Distribution for Equipment")
                            oil_summary = visualization_data["Oil Level"].value_counts().reset_index()
                            oil_summary.columns = ["Oil Level", "Count"]
                            fig = px.bar(
                                oil_summary,
                                x="Oil Level",
                                y="Count",
                                title="Oil Level Distribution for Equipment",
                                labels={"Count": "Number of Records"}
                            )
                            st.plotly_chart(fig)
                        else:
                            st.warning("Oil Level data is missing in the selected dataset.")

                        # Oil Level Distribution for Gearbox
                        if "Gearbox Oil Level" in visualization_data.columns:
                            st.write("#### Oil Level Distribution for Gearbox")

                            # Check for missing or null values
                            if visualization_data["Gearbox Oil Level"].notna().any():
                                # Create a summary of Gearbox Oil Level distribution
                                gearbox_oil_summary = visualization_data[
                                    "Gearbox Oil Level"].value_counts().reset_index()
                                gearbox_oil_summary.columns = ["Gearbox Oil Level", "Count"]

                                # Create the bar chart
                                fig = px.bar(
                                    gearbox_oil_summary,
                                    x="Gearbox Oil Level",
                                    y="Count",
                                    title="Oil Level Distribution for Gearbox",
                                    labels={"Count": "Number of Records"}
                                )
                                st.plotly_chart(fig)
                            else:
                                st.warning("No valid Gearbox Oil Level data available in the selected dataset.")
                        else:
                            st.warning("Gearbox Oil Level data is missing in the selected dataset.")

# Add Back Button
if st.button("Back to Home"):
    st.session_state.page = "main"
