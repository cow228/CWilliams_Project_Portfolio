Features/pass_FI.png: Features/rank_features.py preproc_files/pass_proc.csv Features/feature_imp_cl.py
	python Features/rank_features.py

preproc_files/pass_proc.csv: Preprocessing/preprocessing.py import_files/pass_stats.csv Preprocessing/null_fixes.py Preprocessing/handle_outliers.py Preprocessing/load_data.py Preprocessing/test_normality.py
	python Preprocessing/null_fixes.py
	python Preprocessing/norm_fixes.py
	python Preprocessing/preprocessing.py

import_files/pass_stats.csv: import/import_nfl.py import_files/new_team_pts.csv import_files/coach_data.csv
	python import/import_nfl.py

import_files/new_team_pts.csv: import/new_teams_plyr_demo.py
	python import/new_teams_plyr_demo.py

import_files/coach_data.csv: import/coach_import.py
	python import/coach_import.py



