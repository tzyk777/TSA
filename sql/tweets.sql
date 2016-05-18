drop table if exists tweets;
create table tweets(
  dt date not null,
  post_user text not null,
  post_time timestamp not null,
  content text not null,
);

