drop table tweets if exists;
create table tweets(
  dt date not null,
  post_user text not null,
  post_time timestamp not null,
  content text not null,
  attitude char not null
);