import csv
import datetime
import os
import re
import shutil

def dtm2str(dtmobj):
	return "" if not dtmobj else str(dtmobj.month)+"/"+str(dtmobj.day)+"/"+str(dtmobj.year) 	# Convert datetime object back to string

def str2dtm(strdate):
	m, d, y = strdate.split("/") # "06/24/2020" ["6","24","2020"]
	return datetime.datetime(int(y), int(m), int(d))

def re_exist(r, s):
	return True if re.search(r, s) else False

def money2float(s):
	s = s.replace("$", "").replace(",", "")
	return float(s)

def userinputmoney(s):
	while True:
		try:
			money = float(input(s))
			return money
		except ValueError:
			print("Not a valid float. Try again.")

def parse_invoice(filename):
	with open(filename+'.txt', 'r') as file:
		data = file.read()
		datalist = data.split("\n")
		total_due = -1
		dd_total = {}

		earliest_date = None
		latest_date   = None

		for data in datalist:
			if data.strip(): # if there is data Non Blanks
				m = re.search(r"[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}", data)
				if m:
					trans_date = m.group(0)
					n = re.search(r"\$(\d{1,3}(\,\d{3})*|(\d+))\.\d{2}$", data)
					if n:
						trans_amt = money2float(n.group(0))
						if trans_amt > 0:
							dtm_trans_date = str2dtm(trans_date) # "06/24/2020"
							if not earliest_date and not latest_date:
								earliest_date = dtm_trans_date
								latest_date   = dtm_trans_date
							elif dtm_trans_date < earliest_date:
								earliest_date = dtm_trans_date
							elif dtm_trans_date > latest_date:
								latest_date = dtm_trans_date
						# Data is here and we need to keep track of it
						if trans_date in dd_total:
							dd_total[trans_date] += trans_amt
						else:   # if trans_date not in dd_total
							dd_total[trans_date] = trans_amt
					else:
						pass
				else:
					pass

			else: # Blanks
				continue
			if "TOTAL DUE:" in data.strip():
				total_due_amt = -1
				m = re.search(r"\$(\d{1,3}(\,\d{3})*|(\d+))\.\d{2}$", data)
				if m:   # if there's a match
					total_due = money2float(m.group(0))

		total = 0
		for dates in dd_total:
			total += dd_total[dates]

		total = round(total, 2)

		if total != total_due:
			print("ERROR: Something doesn't add up....")
			print("Calculated Total:", total, "\tPOS Total:", total_due)

		return total_due, dtm2str(earliest_date), dtm2str(latest_date)

def dd_parse(dd_total):
	dd_subtotal  = round( dd_total / 1.08875, 2)	# POS Amount

	dd_pretax 		= userinputmoney("Pre-Tax Total: ")
	dd_tax 	  		= userinputmoney("Total Tax: ")
	dd_commission 	= userinputmoney("Total Commission: ")
	dd_error 		= userinputmoney("Error Charge: ")
	dd_payout 		= dd_pretax + dd_tax - dd_commission - dd_error
	print("Total Net Payout: ", round(dd_payout, 2))

	print()

	if dd_total == dd_pretax+dd_tax:
		print("*** DoorDash subtotal is on the money.", dd_total)
	else:
		difference = dd_subtotal-dd_pretax
		print("POS Subtotal:", dd_subtotal, "\tDoorDash SubTotal:", round(dd_pretax, 2), "\tDifference ($):", round(difference, 2), "\tError (%):", round(difference / dd_total, 3)*100)
		
		if difference/dd_total > 0.05:
			print("*** ERROR: Subtotal Mismatch. Difference is greater than 5%")
		else:
			pass

	if dd_commission/dd_pretax <= 0.2 and dd_commission/dd_subtotal <= 0.2:
		print("*** Commissions are fair and under 20%")
	elif dd_commission/dd_pretax > 0.2 and dd_commission/dd_subtotal > 0.2:
		print("*** Bruh u really fucked up")
	elif dd_commission/dd_pretax > 0.2:
		print("*** DoorDash Commission Calculation greater than 20%")  # This should never be the case
	elif dd_commission/dd_subtotal > 0.2:
		print("*** POS Commission Calculation greater than 20%")

	print("DoorDash Calculation:", dd_commission, "/", dd_pretax, "=", round(dd_commission/dd_pretax, 2))
	print("POS Calculation:     ", dd_commission, "/", dd_subtotal, "=", round(dd_commission/dd_subtotal, 2))

def cav_parse(cav_total):
	cav_subtotal = round(cav_total / 1.08875, 2)	# POS Amount

	web_subtotal = 0
	web_ordertax = 0
	restaurant_portion = 0
	caviar_portion 	   = 0
	cav_error = 0

	with open("order_items.csv", newline='', encoding = "ISO-8859-1") as csvfile:
		raw_csv = list(csv.reader(csvfile, delimiter=',', quotechar='"'))

		first = True
		for row in raw_csv:
			if first:
				first = False
				continue

			if row[0] == "-- End of results --":
				print("Caviar Order Items EOF")
				break

			row = [x.replace("$", "") for x in row]

			if row[7] == "-" or row[8] == "-" or row[9] == "-":
				cav_error += float(row[6])
				continue

			if row[6]:
				web_subtotal += float(row[6])
			if row[7]:
				web_ordertax += float(row[7])
			if row[8] and row[9]: # Restaurant Portion and Caviar Portion and order not cancelled
				restaurant_portion += float(row[8])
				caviar_portion += float(row[9])

	with open("pickup_order_items.csv", newline='', encoding = "ISO-8859-1") as csvfile:
		raw_csv = list(csv.reader(csvfile, delimiter=',', quotechar='"'))

		first = True
		for row in raw_csv:
			if first:
				first = False
				continue

			if row[0] == "-- End of results --":
				print("Caviar Pick Up Items EOF")
				break

			row = [x.replace("$", "") for x in row]

			if row[7] == "-" or row[8] == "-" or row[9] == "-":
				cav_error += float(row[6])
				continue

			if row[6]:
				web_subtotal += float(row[6])
			if row[7]:
				web_ordertax += float(row[7])
			if row[8] and row[9]: # Restaurant Portion and Caviar Portion and order not cancelled
				restaurant_portion += float(row[8])
				caviar_portion += float(row[9])

	web_subtotal = round(web_subtotal, 2)
	web_ordertax = round(web_ordertax, 2)
	restaurant_portion = round(restaurant_portion, 2)
	caviar_portion 	   = abs(round(caviar_portion, 2))
	cav_error = round(cav_error, 2)

	if cav_total == web_subtotal+web_ordertax:
		print("*** Caviar's subtotal is on the money.", cav_total)
	else:
		difference = round(cav_subtotal-web_subtotal, 2)
		print("POS Subtotal:", cav_subtotal, "\tCaviar SubTotal:", web_subtotal, "\tDifference ($):", difference, "\tError (%):", round(difference / cav_subtotal * 100, 3))
		
		if difference/cav_total > 0.05:
			print("*** ERROR: Subtotal Mismatch. Difference is greater than 5%")
			print("Caviar's Cancellation Total:", cav_error)
		else:
			pass

	if caviar_portion/web_subtotal <= 0.2 and caviar_portion/cav_subtotal <= 0.2:
		print("*** Commissions are fair and under 20%")
	elif caviar_portion/web_subtotal > 0.2 and caviar_portion/cav_subtotal > 0.2:
		print("*** Bruh u really fucked up")
	elif caviar_portion/web_subtotal > 0.2:
		print("*** Caviar Commission Calculation greater than 20%")  # This should never be the case
	elif caviar_portion/cav_subtotal > 0.2:
		print("*** POS Commission Calculation greater than 20%")

	print("Caviar Calculation:", caviar_portion, "/", web_subtotal, "=", round(caviar_portion/web_subtotal, 2))
	print("POS Calculation:   ", caviar_portion, "/", cav_subtotal, "=", round(caviar_portion/cav_subtotal, 2))


if __name__ == '__main__':

	cav_total, cav_begin_date, cav_end_date = parse_invoice("caviar")
	dd_total,   dd_begin_date,  dd_end_date = parse_invoice("doordash")
	

	print("Caviar Total  :", cav_total, "\t", cav_begin_date, "-", cav_end_date)
	print("Doordash Total:",  dd_total, "\t",  dd_begin_date, "-",  dd_end_date)

	print("========================  CAVIAR  =========================\n")
	cav_parse(cav_total)
	
	print("======================== DOOR DASH ========================\n")
	dd_parse(dd_total)
	
	##################################################################################################
	# Put files in archive

	begin_date, end_date = cav_begin_date, cav_end_date
	if cav_begin_date != dd_begin_date or cav_end_date != dd_end_date:
		print("\n\nBegin and/or End Dates Don't Match")

	m, d, y = begin_date.split("/")
	m = m if len(m) == 2 else "0"+m
	d = d if len(d) == 2 else "0"+d
	y = y if len(y) == 2 else y[-2:]
	begin_date = m+"."+d+"."+y

	m, d, y = end_date.split("/")
	m = m if len(m) == 2 else "0"+m
	d = d if len(d) == 2 else "0"+d
	y = y if len(y) == 2 else y[-2:]
	end_date = m+"."+d+"."+y

	path = "/mnt/c/Users/bryle/Desktop/Delivery Match Up"
	foldername = begin_date+"-"+end_date

	dir = os.path.join(path, foldername, "")
	if not os.path.exists(dir): # Check if directory exists
		os.mkdir(dir) # Make if not
		print("Creating directory for", foldername)

	orig_cav_file 	 = path+"/caviar.txt"
	orig_dd_file 	 = path+"/doordash.txt"
	orig_cavcsv_file = path+"/order_items.csv"
	orig_cavpickupcsv_file = path+"/pickup_order_items.csv"

	target_cav_file 	 = path+"/"+foldername+"/caviar.txt"
	target_dd_file 		 = path+"/"+foldername+"/doordash.txt"
	target_cavcsv_file 	 = path+"/"+foldername+"/order_items.csv"
	target_cavpickupcsv_file 	 = path+"/"+foldername+"/pickup_order_items.csv"

	shutil.copyfile(orig_cav_file, target_cav_file)
	shutil.copyfile(orig_dd_file, target_dd_file)
	shutil.copyfile(orig_cavcsv_file, target_cavcsv_file)
	shutil.copyfile(orig_cavpickupcsv_file, target_cavpickupcsv_file)
	print("Moved 4 files into archive", foldername)

	with open('caviar.txt', 'w') as file:
		file.write("")
		print("Wiped caviar.txt in root")

	with open('doordash.txt', 'w') as file:
		file.write("")
		print("Wiped doordash.txt in root")
	
	os.remove("order_items.csv")
	print("Deleted order_items.csv in root")

	os.remove("pickup_order_items.csv")
	print("Deleted order_items.csv in root")


