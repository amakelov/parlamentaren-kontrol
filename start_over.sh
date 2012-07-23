rm -rf data
mkdir data
sh update_all_periods.sh
sh update_IDs_plenary_stenograms_after_2012.sh
python stenograms_to_db.py
