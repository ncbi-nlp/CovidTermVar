ANNOTATIONS_DIR=$(realpath "${1}")
DICT="${ANNOTATIONS_DIR}/DICT"
LEX="${ANNOTATIONS_DIR}/LEX"
aitslab="${ANNOTATIONS_DIR}/aitslab"
GRAM="${ANNOTATIONS_DIR}/GRAM"
python -u extract_terms.py "${DICT}" MESH:C000657245 True terms/results_DICT_COVID19.tsv
python -u extract_terms.py "${DICT}" NCBITaxon:2697049 True terms/results_DICT_SARSCoV2.tsv
python -u extract_terms.py "${LEX}" MESH:C000657245 True terms/results_LEX_COVID19.tsv
python -u extract_terms.py "${LEX}" NCBITaxon:2697049 True terms/results_LEX_SARSCoV2.tsv
python -u extract_terms.py "${aitslab}" MESH:C000657245 True terms/results_aitslab_COVID19.tsv
python -u extract_terms.py "${aitslab}" NCBITaxon:2697049 True terms/results_aitslab_SARSCoV2.tsv
python -u extract_terms.py "${GRAM}" MESH:C000657245 True terms/results_GRAM_COVID19.tsv
python -u extract_terms.py "${GRAM}" NCBITaxon:2697049 True terms/results_GRAM_SARSCoV2.tsv
