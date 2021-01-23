# C# Entity Generator

An Entity Generator written in Python for creating Models based on tables on SQL Server

## Motivation

When using EfCore, we always have to map the Models created by us to to the SQL Tables in order to use all it's features, but sometimes it may get hard when dealing with
so many fields. for that task, this generator can easily do all the heavy lifting work for you

## How to Use

First you have the install the Requirements (actually it's only one) from the `Requirements.txt` file with the following command:

```bash
  pip3 intall Requirements.txt
```

Then , you have to configure the file `db_file.txt` with your env

Now, in order to use it you can execute:

```bash
  python3 ./gen_entity <your_table_name>
```
