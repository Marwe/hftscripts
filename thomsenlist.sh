#!/bin/bash

# get thomsen reuters list
# http://ip-science.thomsonreuters.com/cgi-bin/jrnlst/jlresults.cgi?PC=MASTER
# select format for print A-Z

outf="journallist_$(date -I).rst"
journp="$(which journaltrparser.py)"
if [ ! -x "$journp" ] ; then 
	echo could not find journaltrparser.py
	exit 1
fi

tmpdir="$(mktemp --tmpdir -d tmptrlist.XXXX)"
if [ $? -ne 0 ] ; then
	echo "error creating tmpdir"
	exit 1
else
	echo "working in $tmpdir"
	cd "$tmpdir"
fi


# 35 pages in 2015
# 43 pages end of 2005
for i in {1..50} 
do 
  echo "pwd: $(pwd)"
  wget -c "http://ip-science.thomsonreuters.com/cgi-bin/jrnlst/jlresults.cgi?PC=MASTER&mode=print&Page=$i" -O "resultpage$i"
done

"$journp" resultpage*| sort -n -k 2 | grep -v '^$' | sort -n -k 2 | grep -v '^$' > "$outf"

# remove numbers etc. in the beginning of the line
sed -e 's#^[^A-Za-z]*##' "$outf" | gzip > "${outf%rst}txt.gz"

echo result in "$(pwd)/$outf" and "$(pwd)/${outf%rst}txt.gz"

