#!/usr/bin/env python3
# This file is part of the Network Performance Monitor which is released under the GNU General Public License v3.0
# See the file LICENSE for full license details.

import math

DAY_MINUTES=24*60

class bin:
	def __init__(self,fractional_hour):
		self.values=[]
		self.time = fractional_hour

	def add_value(self,value):
		self.values.append(value)

	def mean(self):
		return sum(self.values) / len(self.values) if len(self.values) > 0 else 0

class time_bins:

	def __init__(self,bin_minutes):
		nbins = math.floor(DAY_MINUTES/bin_minutes)
		self.bin_width = float(bin_minutes)/60.0
		self.bin_mid = self.bin_width/2.0
		self.bins = []
		t = 0.0
		while t < 24:
			b = bin(t + self.bin_mid)
			self.bins.append(b)
			t += self.bin_width

	def add_value(self, fractional_hour, value):
		b = int(math.floor(fractional_hour / self.bin_width))
		self.bins[b].add_value(value)

	def get_times(self):
		return [b.time for b in self.bins]

	def get_means(self):
		return [b.mean() for b in self.bins]

