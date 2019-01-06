from Bio import SeqIO

records = list(SeqIO.parse(snakemake.input[0],'fasta'))
filtered_records = []

for record in records:
	if record.id in snakemake.config['mirnas']:
		filtered_records.append(record)
	elif len(snakemake.config['mirnas']) == 0: # use all records if mirna config entry is empty
		filtered_records.append(record)
	else:
		pass

SeqIO.write(filtered_records,snakemake.output[0],'fasta')
