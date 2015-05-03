drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  date integer not null,
  username text not null,  
  temp real,
  turbidity real,
  salinity real,
  do real,
  
  fish integer,
  crabs integer,
  shrimp integer,
  
  phytoA integer,
  phytoB integer,
  phytoC integer,
  phytoD integer,
  phytoE integer,
  phytoF integer,
  phytoG integer,
  phytoH integer,
  phytoI integer,
  
  zooJ integer,
  zooK integer,
  zooL integer,
  
  notes text
  
);