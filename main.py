from pathlib import Path
import subprocess
import csv
import iCalImport

# CSV Template  :   uid, summary, start, end, location, description, status, last_modified
#
#

# Runs the pre-established calendar fetch service
iCalImport.main()