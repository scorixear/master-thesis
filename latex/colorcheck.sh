gs -o - -sDEVICE=inkcov $1 | tail -n +6 | sed ':a;N;$!ba;s/\n / /g' > /tmp/colorlog # each page on one line
echo -n "Black and white pages: "
grep -e "0.00000  0.00000  0.00000  [01]." /tmp/colorlog | wc -l
echo -n "Colored pages: "
grep -v -e "0.00000  0.00000  0.00000  [01]." /tmp/colorlog | wc -l
grep -v -e "0.00000  0.00000  0.00000  [01]." /tmp/colorlog
