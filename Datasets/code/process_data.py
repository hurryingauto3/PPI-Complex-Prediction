file_name = "9606.txt"
file_name2 = 'protein_interactors_score_mentha.tsv'
processed_file = open(file_name2, "a")
unprocessed_file = open(file_name, errors="ignore")
# print(unprocessed_file.readline().split(";"))
# for mentha
for line in unprocessed_file:
    listed = line.split(";")
    PROTEINA = listed[0]
    GENEA = listed[1]
    PROTEINB = listed[2]
    GENEB = listed[3]
    SCORE = listed[4]
    processed_line = "\t".join([PROTEINA, GENEA, PROTEINB, GENEB, SCORE])
    processed_file.write(processed_line + "\n")
    print(processed_line)

# for signor
# for line in unprocessed_file:
#     listed = line.split("\t")
#     ENTITYA = listed[0]
#     IDA = listed[2]
#     ENTITYB = listed[4]
#     IDB = listed[6]
#     SCORE = listed[26]
#     processed_line = "\t".join([ENTITYA, IDA, ENTITYB, IDB, SCORE])
#     processed_file.write(processed_line + "\n")
#     print(processed_line)
