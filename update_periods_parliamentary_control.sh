curl "http://www.parliament.bg/bg/parliamentarycontrol" 2> /dev/null |\
    grep "/bg/parliamentarycontrol/period/" |\
    perl -pe "s|.*?([12]\d\d\d-\d*).*|\1|" |\
    cat > data/periods_parliamentary_control
