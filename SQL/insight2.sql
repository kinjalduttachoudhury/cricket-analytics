-- Which male and female teams had the highest win percentages in 2019?
with all_teams_data as (
  select
    year,
    gender,
    team,
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
        strftime('%Y', match_date) = '2019'
      union all
      select
        strftime('%Y', match_date) as year,
        gender,
        team2 as team,
        winner
      from
        match_results
      where
        strftime('%Y', match_date) = '2019'
    )
  group by
    1,
    2,
    3
)
select
  year,
  gender,
  team,
  percentage_win
from
  (
    select
      year,
      gender,
      team,
      percentage_win,
      rank() over (
        partition by gender
        order by
          percentage_win desc
      ) as rnk
    from
      all_teams_data
  )
where
  rnk = 1
