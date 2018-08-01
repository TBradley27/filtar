#!/bin/env python

import sys
import functools
from functools import reduce
import re
import os
from Bio import AlignIO
from Bio.AlignIO import MafIO
from subprocess import call

if sys.argv[3] == "hsa" and sys.argv[5] == 'test':    #Identify the species identifier passed through the command line
        build = "hg19"
elif sys.argv[3] == "hsa" and sys.argv[5] != 'test':
       build = "hg38"
elif sys.argv[3] == "mmu":
        build = "mm10"
else:
        build = ''

print (sys.argv)
print (build)

idx = AlignIO.MafIO.MafIndex(sys.argv[1], sys.argv[2], "{}.chr{}".format(build, sys.argv[4])  )

start_pos = []
end_pos = []
accession = 'empty'
with open(sys.argv[6] ) as f:
    for line in f:    #Open and loop through line-by-line the relevant BED file
        parts = line.split()  

        if accession == 'empty':
            accession = parts[4]   
            start_pos.append(int(parts[1]))
            end_pos.append(int(parts[2]))
            strand = (int(parts[3]))

        elif parts[4] == accession:       # If accession has multiple entries in bed, add additional genome co-ordinates to rel. lists
            start_pos.append(int(parts[1]))
            end_pos.append(int(parts[2]))
            strand = (int(parts[3]))

        else:
           # write process - triggered once script hits a record != accession

           if strand == -1:
               start_pos = start_pos[::-1] # Reverse Order
               end_pos = end_pos[::-1]
           else:
               pass

           print (accession)
           print (start_pos)
           print (end_pos)
           print (strand)             

           new_multiple_alignment = idx.get_spliced(start_pos, end_pos, strand) # splice through the index
           AlignIO.write(new_multiple_alignment, "results/{}.fa".format(accession), "fasta")
           
           call("exe/targetscan7/convert_fasta_to_tsv.sh results/{}.fa {} > tmp{}.tsv".format(accession, accession, sys.argv[4]), shell=True) #Execute a shell command
           call(["rm", "results/{}.fa".format(accession)])
           call("cat tmp{}.tsv >> results/hsa_chr{}_msa_tmp.tsv".format(sys.argv[4], sys.argv[4]), shell=True)
           call(["rm","tmp{}.tsv".format(sys.argv[4])])
           
           start_pos = [] # initialise a new transcript record
           end_pos = []
           start_pos.append(int(parts[1]))
           end_pos.append(int(parts[2]))
           strand = (int(parts[3]))
           accession = parts[4]
    else: #Not sure, but I think this is for transcripts with only one 'exon', which are not the first transcript in the bed record.

       if strand == -1:
               start_pos = start_pos[::-1] # Reverse Order
               end_pos = end_pos[::-1]
       else:        
               pass

       print (accession)
       print (start_pos)
       print (end_pos)
       new_multiple_alignment = idx.get_spliced(start_pos, end_pos, strand)
       AlignIO.write(new_multiple_alignment, "results/{}.fa".format(accession), "fasta")

       call("exe/targetscan7/convert_fasta_to_tsv.sh results/{}.fa {} > tmp{}.tsv".format(accession, accession, sys.argv[4]), shell=True) #Execute a shell command
       call(["rm", "results/{}.fa".format(accession)])
       call("cat tmp{}.tsv >> results/hsa_chr{}_msa_tmp.tsv".format(sys.argv[4], sys.argv[4]), shell=True)
       call(["rm","tmp{}.tsv".format(sys.argv[4])])

TaxID = {"hg38":"9606", "hg19":"9606", "panTro4":"9598", "panTro5":"9598", "gorGor3":"9595",   "ponAbe2":"9601",   "nomLeu3":"9581", "nomLeu2":"9581", "nomLeu1":"9581","rheMac3":"9544",  
     "rheMac8":"9544", "macFas5":"9541",  "papHam1":"9557",	"tarSyr1":"9476",	"tarSyr2":"9476",	"dipOrd1":"10020",	"tupBel1":"37347",	"micMur1":"30608",	"choHof1":"9358",	"proCap1":"9813",
     "papAnu2":"9557",   "chlSab2":"60711",   "calJac3":"9483",   "saiBol1":"27679",   "otoGar3":"30611",   "tupChi1":"246437",   "speTri2":"43179",   "jacJac1":"51337",  
     "micOch1":"79684",   "criGri1":"10029",   "mesAur1":"10036",   "mm10":"10090",   "rn6":"10116", "rn5":"10116",   "hetGla2":"10181",   "cavPor3":"10141",   "chiLan1":"34839",  
     "octDeg1":"10160",   "oryCun2":"9986",   "ochPri3":"9978", "ochPri2":"9978",  "susScr3":"9823",   "vicPac2":"30538",	"vicPac2":"30538",   "camFer1":"419612",   "turTru2":"9739",   "orcOrc1":"9733",  
     "panHod1":"59538",   "bosTau8":"9913", "bosTau7":"9913",   "oviAri3":"9940",	"oviAri1":"9940",   "capHir1":"9925",   "equCab2":"9796",   "cerSim1":"9807",   "felCat8":"9685",   "canFam3":"9615",  
     "musFur1":"9669",   "ailMel1":"9646",   "odoRosDiv1":"9708",   "lepWed1":"9713",   "pteAle1":"9402",   "pteVam1":"132908",   "myoDav1":"225400",   "myoLuc2":"59463", 
     "eptFus1":"29078",   "eriEur2":"9365",	"eriEur2":"9365",   "sorAra2":"42254",	"sorAra1":"42254",   "conCri1":"143302",   "loxAfr3":"9785",   "eleEdw1":"28737",   "triMan1":"127582",   "chrAsi1":"185453", 
     "echTel2":"9371",	"echTel2":"9371",   "oryAfe1":"1230840",   "dasNov3":"9361",   "monDom5":"13616",   "sarHar1":"9305",   "macEug2":"9315",   "ornAna1":"9258",   "falChe1":"345164", 
     "falPer1":"9854",   "ficAlb2":"59894",   "zonAlb1":"44394",   "geoFor1":"48883",   "taeGut2":"59729",	"taeGut1":"59729",   "pseHum1":"181119",   "melUnd1":"13146",   "amaVit1":"241585", 
     "araMac1":"176014",   "colLiv1":"8932",  "anaPla1":"8839",   "galGal4":"9031",  "melGal1":"9103",   "allMis1":"8496",   "cheMyd1":"8469",  "chrPic2":"8478",	"chrPic1":"8478", 
     "pelSin1":"13735",   "apaSpi1":"55534",   "anoCar2":"28377",   "xenTro7":"8364",	"xenTro3":"8364",   "latCha1":"7897",   "tetNig2":"99883",   "fr3":"31033",   "takFla1":"433684", 
     "oreNil2":"8128",   "neoBri1":"32507",   "hapBur1":"8153",   "mayZeb1":"106582",   "punNye1":"303518",   "oryLat2":"8090",   "xipMac1":"8083",   "gasAcu1":"69293", 
     "gadMor1":"8049",   "danRer10":"7955",	"danRer7":"7955",   "astMex1":"7994",   "lepOcu1":"7918",	"petMar2":"7757", "petMar1":"7757"
}

CommonName = {"hg38":"Human", "panTro4":"Chimp", "gorGor3":"Gorilla",   "ponAbe2":"Orangutan",   "nomLeu3":"Gibbon",    "rheMac3":"Rhesis Macaque",   "macFas5":"Crab-eating Macaque",  
     "papAnu2":"Baboon",   "chlSab2":"Green Monkey",   "calJac3":"Marmoset",   "saiBol1":"Squirrel monkey",   "otoGar3":"Bushbaby",   "tupChi1":"Chineses tree shrew",   "speTri2":"Squirrell",   "jacJac1":"Lesser Egyptian jerboa",  
     "micOch1":"Prairie vole",   "criGri1":"Chinese hamster",   "mesAur1":"Golden hamster",   "mm10":"Mouse",   "rn6":"Rat",   "hetGla2":"Naked mole-rat",   "cavPor3":"Guinea pig",   "chiLan1":"Chinchilla",  
     "octDeg1":"Brush-tailed rat",   "oryCun2":"Rabbit",   "ochPri3":"Pika",   "susScr3":"Pig",   "vicPac2":"Alpaca",   "camFer1":"Bactrian camel",   "turTru2":"Dolphin",   "orcOrc1":"Killer whale",  
     "panHod1":"Tibetan antelope",   "bosTau8":"Cow",   "oviAri3":"Sheep",   "capHir1":"Domestic goat",   "equCab2":"Horse",   "cerSim1":"White rhinocerous",   "felCat8":"Cat",   "canFam3":"Dog",  
     "musFur1":"Ferret",   "ailMel1":"Panda",   "odoRosDiv1":"Pacific walrus",   "lepWed1":"Weddell seal",   "pteAle1":"Black flying-fox",   "pteVam1":"Megabat",   "myoDav1":"David's myotis bat",   "myoLuc2":"Microbat", 
     "eptFus1":"Big brown bat",   "eriEur2":"Hedgehog",   "sorAra2":"Shrew",   "conCri1":"Star-nosed mole",   "loxAfr3":"Elephant",   "eleEdw1":"Cape elephant shrew",   "triMan1":"Manatee",   "chrAsi1":"Cape golden mole", 
     "echTel2":"Tenrec",   "oryAfe1":"Aardvark",   "dasNov3":"Armadillo",   "monDom5":"Opossum",   "sarHar1":"Tasmanian devil",   "macEug2":"Wallaby",   "ornAna1":"Platypus",   "falChe1":"Saker falcon", 
     "falPer1":"Peregrine falcon",   "ficAlb2":"Collared flycatcher",   "zonAlb1":"White-throated sparrow",   "geoFor1":"Medium ground finch",   "taeGut2":"Zebra finch",   "pseHum1":"Tibetan ground jay",   
     "melUnd1":"Budgerigar",   "amaVit1":"Parrot", "araMac1":"Scarlet macaw",   "colLiv1":"Rock pigeon",  "anaPla1":"Mallard duck",   "galGal4":"Chicken",  "melGal1":"Turkey",   
     "allMis1":"American alligator",   "cheMyd1":"Green seaturtle",  "chrPic2":"Painted turtle", "pelSin1":"Chinese softshell turtle",   "apaSpi1":"Spiny softshell turtle",   "anoCar2":"Lizard",   "xenTro7":"Xenopus",   
     "latCha1":"Coelacanth"}

f = open("results/hsa_chr{}_msa_tmp.tsv".format(sys.argv[4]), 'r')

# prevents writing to an already existing file
call(["rm",sys.argv[7]])

target = open(sys.argv[7], 'w')

for line in iter(f):
    #result = pattern.sub(lambda x: d[x.group()], line)
    result = reduce(lambda x, y: x.replace(y, TaxID[y]), TaxID, line)
    target.write(result)
    del result
f.close()

call(["rm","results/hsa_chr{}_msa_tmp.tsv".format(sys.argv[4])])