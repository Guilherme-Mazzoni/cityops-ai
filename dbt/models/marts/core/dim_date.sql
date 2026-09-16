with staging as (
    select * from {{ ref('stg_311_requests') }}
),

dates as (
    select distinct date(created_date) as date_day
    from staging
    where created_date is not null
    union
    select distinct date(closed_date) as date_day
    from staging
    where closed_date is not null
    union
    select distinct date(due_date) as date_day
    from staging
    where due_date is not null
)

select
    date_day as date_key,
    date_day,
    extract(year from date_day) as year,
    extract(month from date_day) as month,
    extract(day from date_day) as day,
    extract(isodow from date_day) as day_of_week
from dates
where date_day is not null
