#!/bin/bash

read -p "Enter your command: " user_input

echo "$user_input" | python3 control_send.py

