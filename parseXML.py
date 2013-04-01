#!/usr/bin/python
# -*- coding: utf_8 -*-

import os
from lxml import etree, objectify
import sys
import codecs
import re

# XML file name
xml_dir = sys.argv[1]
os.chdir(xml_dir)
xml_file = os.listdir(".")

# open output file
out1 = open('../../../pubmed.txt', 'a+')
out2 = open('../../../pmc.txt', 'a+')

# Each XML file
for s in range(len(xml_file)):
	#print str(s + 1) + " / " + str(len(xml_file))

	# parse XML
	tree = objectify.parse(xml_file[s], parser = etree.XMLParser())
	root = tree.getroot()

	try:

		# Journal
		Journal = re.sub(r'Put_Data_Here/articles.[A-Z]-[A-Z]/', '', xml_dir).replace("/", "")
		# Year
		Year = root.xpath("front")[0].xpath("article-meta")[0].xpath("pub-date")[0].xpath("year")[0].text
		# Title
		T = len(root.xpath("front")[0].xpath("article-meta")[0].xpath("title-group")[0])
		preTitle = root.xpath("front")[0].xpath("article-meta")[0].xpath("title-group")[0]
		
		if T != 0:
			if T == 1:
				Title = preTitle[0].text
			if T > 1:
				Title = ""
				for r in range(T):
					Title = Title + str(preTitle[r].text)
			
		# Abstruct
		A = len(root.xpath("front")[0].xpath("article-meta")[0].xpath("abstract")[0])
		preAbstruct = root.xpath("front")[0].xpath("article-meta")[0].xpath("abstract")[0]
		
		if A != 0:
			if A == 1:
				Abstruct = preAbstruct[0].text
			if A > 1:
				Abstruct = ""
				for r in range(A):
					Abstruct = Abstruct + str(preAbstruct[r].text)
		
		# PMID / Pumbed URL
		PMID = root.xpath("front")[0].xpath("article-meta")[0].xpath("article-id")[0].text
		PM_URL = "http://www.ncbi.nlm.nih.gov/pubmed/" + PMID

		# remove ¥t ¥n
		PMID = PMID.replace("\t","")
		PMID = PMID.replace("\n","")
		Journal = Journal.replace("\t","")
		Journal = Journal.replace("\n","")
		Year = Year.replace("\t","")
		Year = Year.replace("\n","")
		Title = Title.replace("\t","")
		Title = Title.replace("\n","")
		Abstruct = Abstruct.replace("\t","")
		Abstruct = Abstruct.replace("\n","")
		PM_URL = PM_URL.replace("\t","")
		PM_URL = PM_URL.replace("\n","")

		# output
		out1.write(PMID.encode("utf_8"))
		out1.write("\t")
		out1.write(Journal.encode("utf_8"))
		out1.write("\t")
		out1.write(Year.encode("utf_8"))
		out1.write("\t")
		out1.write(Title.encode("utf_8"))
		out1.write("\t")
		out1.write(Abstruct.encode("utf_8"))
		out1.write("\t")
		out1.write(PM_URL.encode("utf_8"))
		out1.write("\n")

	except IndexError:
		pass
	except AttributeError:
		pass
	except UnicodeEncodeError:
		pass
			
	#  PMCID / PMCURL
	try:
		PMCID = "PMC" + root.xpath("front")[0].xpath("article-meta")[0].xpath("article-id")[1].text
		PMC_URL = "http://www.ncbi.nlm.nih.gov/pmc/articles/" + PMCID + "/pdf/"

		# remove ¥t ¥n
		PMCID = PMCID.replace("\t","")
		PMCID = PMCID.replace("\n","")
		PMC_URL = PMC_URL.replace("\t","")
		PMC_URL = PMC_URL.replace("\n","")

		# output
		out2.write(PMID.encode("utf_8"))
		out2.write("\t")
		out2.write(PMCID.encode("utf_8"))
		out2.write("\t")
		out2.write(PMC_URL.encode("utf_8"))
		out2.write("\n")

	except IndexError:
		pass
	except NameError:
		pass

# close
out1.close()
out2.close()
