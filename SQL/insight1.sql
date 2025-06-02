-- The win records (percentage win and total wins) for each team by year and gender, excluding ties,
-- matches with no result, and matches decided by the DLS method in the event that, for whatever
-- reason, the planned innings can’t be completed.
select
  year,
  gender,
  team,
  sum(
    case when team = winner then 1 else 0 end
  ) as total_wins,
  count(*) as total_matches,
  round(
    cast(
      sum(
        case when team = winner then 1 else 0 end
      ) as float
    )* 100 / count(*),
    2
  ) as percentage_win
from
  (
    select
      strftime('%Y', match_date) as year,
      gender,
      team1 as team,
      winner
    from
      match_results
    where
      outcome_method is null
      and outcome_result is null
    union all
    select
      strftime('%Y', match_date) as year,
      gender,
      team2 as team,
      winner
    from
      match_results
    where
      outcome_method is null
      and outcome_result is null
  )
group by
  1,
  2,
  3
order by
  1,
  2,
  3