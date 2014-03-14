blk='\x1b[0;30m' # Black - Regular
red='\x1b[0;31m' # Red
grn='\x1b[0;32m' # Green
ylw='\x1b[0;33m' # Yellow
blu='\x1b[0;34m' # Blue
pur='\x1b[0;35m' # Purple
cyn='\x1b[0;36m' # Cyan
wht='\x1b[0;37m' # White

err='\x1b[37;41m' # Error
war='\x1b[30;43m' # Warning

IFS='' # dunno why needed but if not, read ignores multiple spaces
while read data; do
  echo $data | sed \
-e "s%^\(\[.*\%\]\)\( Building CXX object.*$\)%\1$grn\2$blk%" \
-e "s%^.*Linking .*$%\x1b[0;31m&$blk%" \
-e "s%^.*Scanning dependencies .*$%$pur&$blk%" \
-e "s%^\(\[.*\%\]\)\( Generating.*$\)%\1$blu\2$blk%" \
-e "s%^\(#### Running command: \)\(\".*\"\)\( in \)\(\".*\"$\)%$blu\1$cyn\2$blu\3$cyn\4$blk%" \
-e "s%^####%$blu&$blk%" \
-e "s%^.*: error: .*$%$err&$blk%" \
-e "s%^.*: warning: .*$%$war&$blk%"  \
-e "s%^\(\[==========\]\|\[----------\]\|\[ *RUN *\]\|\[ *OK *\]\|\[ *PASSED *\]\)%$grn&$blk%" \
-e "s%^\[ *FAILED *\]%$red&$blk%" ;


done


