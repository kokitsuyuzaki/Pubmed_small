#! /bin/sh

# Search all journal
ls -d Put_Data_Here/*/*/ > xml.txt

# Parse XML
while read line
do
txt=${line}
echo $txt
python parseXML.py $txt
done<xml.txt

# Constuct SQLite
sqlite3 pubmed.sqlite < schema.query