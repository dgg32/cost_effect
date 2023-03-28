

# Introduction

  

  

This repository contains code and data for my article "[Calculate Cost-Benefit in a Bayesian Knowledge Graph](https://medium.com/p/c54db348de19)".

1. The scripts are for data flow between Google Sheets, Neo4j and OpenMarkov.

  

2. The source data folder contains the TSV downloaded from the Google Sheets for debugging purpose. The pgmx_output folder contains TSV files that are extracted from a pgmx file.

  

  

# Prerequisite

Neo4j Desktop

OpenMarkov
  

# Run
First, config the config.yaml to match your Google Sheets setup.
  
1. Convert data from Google Sheets to a pgmx file
```console
python google_to_pgmx.py [model_name] > [model].pgmx
```

For example:
```console
python google_to_pgmx.py cost_effect > google_test.pgmx
```

 
2. Convert data from Google Sheets to Neo4j

```console
python tsv_to_neo4j.py
```
It generates a series of files in the ./neo4j folder.

3. Other utility files.

pgmx_to_tsv.py is to parse a PGMX file and generate two node files, a criterion, a link, and a potential TSV file. You use this script when you have modified data in OpenMarkov and want to overwrite the changes back into your TSV files.

And you can use upsert_tsv.py to upsert the new data into an old TSV file.

## Authors

  

*  **Sixing Huang** - *Concept and Coding*

  

## License

  

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
