#!/usr/bin/python3
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import argparse
import datetime
import time

import canigen

parser = argparse.ArgumentParser(
    description="Generates SocketCAN messages for AWS IoT FleetWise demo"
)
parser.add_argument("-i", "--interface", default="vcan0", help="CAN interface, e.g. vcan0")
parser.add_argument("-o", "--only-obd", action="store_true", help="Only generate OBD messages")
args = parser.parse_args()

can_sim = canigen.Canigen(
    interface=args.interface,
    database_filename=None if args.only_obd else "hscan.dbc",
    obd_config_filename="obd_config.json",
)
BRAKE_PRESSURE_SIGNAL = "BrakePedalPressure"
ENGINE_TORQUE_SIGNAL = "EngineTorque"
TIRE_PRESSURE_SIGNAL_FL = "TireRRPrsFL"
TIRE_PRESSURE_SIGNAL_FR = "TireRRPrsFR"
TIRE_PRESSURE_SIGNAL_RL = "TireRRPrsRL"
TIRE_PRESSURE_SIGNAL_RR = "TireRRPrsRR"
OUTSIDE_TEMPERATURE_SIGNAL= "OtsAirTmp"
WHEEL_SPEED_SIGNAL_FL = "WHEEL_SPEED_FL"
WHEEL_SPEED_SIGNAL_FR = "WHEEL_SPEED_FR"
WHEEL_SPEED_SIGNAL_RL = "WHEEL_SPEED_RL"
WHEEL_SPEED_SIGNAL_RR = "WHEEL_SPEED_RR"

def set_with_print(func, name, val):
    print(str(datetime.datetime.now()) + " Set " + name + " to " + str(val))
    func(name, val)


try:
    while True:
        set_with_print(can_sim.set_sig, BRAKE_PRESSURE_SIGNAL, 0)
	set_with_print(can_sim.set_sig, OUTSIDE_TEMPERATURE_SIGNAL, 7)
        for i in range(1, 11):
            set_with_print(can_sim.set_pid, "ENGINE_SPEED", 1000 + i * 100)
            set_with_print(can_sim.set_pid, "VEHICLE_SPEED", i * 10)
	    set_with_print(can_sim.set_pid, WHEEL_SPEED_SIGNAL_FL, i * 10)
	    set_with_print(can_sim.set_pid, WHEEL_SPEED_SIGNAL_FR, i * 10)
	    set_with_print(can_sim.set_pid, WHEEL_SPEED_SIGNAL_RL, i * 10)
	    set_with_print(can_sim.set_pid, WHEEL_SPEED_SIGNAL_RR, i * 10)
            set_with_print(can_sim.set_pid, "FUEL_TANK_LEVEL", 100 - i)
            set_with_print(can_sim.set_pid, "AMBIENT_AIR_TEMPERATURE", 20 + i)
            set_with_print(can_sim.set_pid, "ENGINE_COOLANT_TEMPERATURE", 80 + i)
            set_with_print(can_sim.set_pid, "THROTTLE_POSITION", (i % 4) * 100)
            set_with_print(can_sim.set_dtc, "ECM_DTC1", i / 5 >= 1)
	    set_with_print(can_sim.set_sig, OUTSIDE_TEMPERATURE_SIGNAL, 7-i)
	    time.sleep(0.5)
            set_with_print(can_sim.set_sig, TIRE_PRESSURE_SIGNAL_FL, i+200)
	    set_with_print(can_sim.set_sig, TIRE_PRESSURE_SIGNAL_FR, i+210)
	    set_with_print(can_sim.set_sig, TIRE_PRESSURE_SIGNAL_RL, i+220)
	    set_with_print(can_sim.set_sig, TIRE_PRESSURE_SIGNAL_RR, i+230)
            time.sleep(5)
            if i < 6 or i > 9:
                # trigger is > 7000 so trigger
                set_with_print(can_sim.set_sig, BRAKE_PRESSURE_SIGNAL, 8000)
            set_with_print(can_sim.set_sig, ENGINE_TORQUE_SIGNAL, i * 100)
            time.sleep(0.5)
            set_with_print(can_sim.set_sig, BRAKE_PRESSURE_SIGNAL, i * 200)
except KeyboardInterrupt:
    print("Stopping...")
    can_sim.stop()
except Exception:
    raise
