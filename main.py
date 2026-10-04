import sys
import subprocess
if len(sys.argv) ==1:
  sys.stdio.write("""try one:
    1. lobman new app my_app
    2. lobman new package my_package
    3. lobman run my_app""")
