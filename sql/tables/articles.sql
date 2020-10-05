CREATE TABLE IF NOT EXISTS civic_jabber.articles (
  id text,
  source_id text,
  source_name text,
  source_brand text,
  source_description text,
  title text,
  body text,
  summary text,
  keywords text[],
  images text[],
  url text,
  extraction_date timestamp
) ;
