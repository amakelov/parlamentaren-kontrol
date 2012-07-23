curl "http://www.parliament.bg/bg/plenaryprogram" 2> /dev/null |\
    grep "/bg/plenaryprogram/period/" |\
    perl -pe "s|.*?([12]\d\d\d-\d*).*|\1|" |\
    cat > data/periods_plenary_programs
