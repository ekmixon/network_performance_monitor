#!/usr/bin/env python3
# This file is part of the Network Performance Monitor which is released under the GNU General Public License v3.0
# See the file LICENSE for full license details.

from subprocess import check_output,Popen,STDOUT,PIPE
import numpy as np
import signal
from datetime import datetime

def nz_values(arr):
# return an array containing all non-zero values in the source array
	nztuples = np.nonzero(arr)
	return [arr[i] for i in nztuples[0]]

def get_client_id():
	cmd = "sum /etc/machine-id | cut -f 1 -d ' '"
	ps = Popen(cmd,shell=True,stdout=PIPE,stderr=STDOUT)
	(sn_str,return_code) = ps.communicate()
	return (sn_str.decode()).rstrip("\n")

class sigterm_handler():
	def sh(self,signalNumber, frame):
		self.terminate = True
	def __init__(self):
		self.terminate = False
		signal.signal(signal.SIGTERM, self.sh)

def fractional_hour(timestamp):
	# convert timestamp to fractional hour e.g. timestamp = 13:30 -> 13.5, timestamp = 15:45 -> 15.75 etc.
	SECONDS_PER_HOUR = 60*60
	dt = datetime.fromtimestamp(timestamp)
	dt_12am = datetime.combine(dt,datetime.min.time())
	tdelta = dt - dt_12am
	return round(float(tdelta.seconds)/SECONDS_PER_HOUR,3)

