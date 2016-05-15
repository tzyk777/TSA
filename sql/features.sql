drop table if exists features;
create table features(
  sentiment text not null,
  word text not null,
  frequency integer not null
);