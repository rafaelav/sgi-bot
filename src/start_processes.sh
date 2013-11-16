#!/bin/bash

python save_data_script.py && (python follow_script.py & python unfollow_script.py &)

