CREATE TABLE IF NOT EXISTS civic_jabber.regulations (
  id text,
  state text,
  issue text,
  volume text,
  regulation_number text,
  description text,
  summary text,
  preamble text,
  body text,
  titles text,
  authority text,
  contact text,
  link text,
  extra_attributes jsonb,
  register_date timestamp,
  effective_date timestamp,
  as_of_date timestamp
) ;