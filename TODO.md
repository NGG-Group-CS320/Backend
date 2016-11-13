# To do

## Miscellaneous
- [ ] Add description to README
- [ ] Check that we agree that the MIT license is acceptable
- [ ] Figure out how we will deploy to the AWS server

## Database initialization
- [ ] Create postgres server
 - http://tecadmin.net/install-postgresql-server-on-ubuntu/
- [ ] Create main table in postgres
 - Someone will have to figure out all the data types/attributes for all the columns to do this correctly
- [ ] Load all CSV files
 - http://stackoverflow.com/questions/2987433/how-to-import-csv-file-data-into-a-postgresql-table
 - It may be good to write a script which, for each file in a directory, ingests the file and moves it to a different directory. That'll make loading the next batch of files really easy (and will make HP happy)

## Precomputing and health scores
- [ ] Make function which returns the health score for a system
- [ ] Create precomputed_stats table in postgres
 - PROBABLY average & std dev for certain chosen columns
 - This should also contain the health scores

## Webserver
- [ ] Create webserver (PROBABLY we said Apache for this)
- [ ] Make the webserver server database info to the user
