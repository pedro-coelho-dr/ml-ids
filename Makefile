conda:
	conda env export --from-history > environment.yml

update:
	conda env update -f environment.yml --prune