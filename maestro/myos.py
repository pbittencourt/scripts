#!/usr/bin/env python3

import os, platform, sys
print(os.name)
print(platform.system())
print(platform.release())
print(sys.platform)

# path of this script
abs_path = os.path.abspath(__file__)
print(abs_path)

# directory of this script
file_dir = os.path.dirname(abs_path)
print(file_dir)

# parent directory
parent_dir = os.path.dirname(file_dir)
print(parent_dir)

# driver's dir: inside parent directoru
drivers_dir = os.path.join(parent_dir, 'drivers')
print(drivers_dir)

# executable depends on user's os
user_os = platform.system()
if user_os == 'Linux':
	driver_exe = 'chromedriver'
elif user_os == 'Windows':
	driver_exe = 'chromedriver.exe'

print(os.path.join(drivers_dir, driver_exe))