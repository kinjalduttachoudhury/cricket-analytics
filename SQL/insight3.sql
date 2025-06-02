-- Which players had the highest strike rate as batsmen in 2019? (Note to receive full credit, you
-- need to account for handling extras properly.)
select
  strftime('%Y', match_date) as year,
  batter,
  sum(runs_batter) as runs_scored,
  count(*) as deliveries_faced,
  round(
    cast(
      sum(runs_batter) as float
    )* 100 / count(*),
    2
  ) as strike_rate
FROM
  match_ball_by_ball
where
  extras_wides is null -- ignoring only wide balls, because other extras are counted as deliveries faced by batsmen
  and strftime('%Y', match_date) = '2019'
group by
  1,
  2
order by
  5 desc
