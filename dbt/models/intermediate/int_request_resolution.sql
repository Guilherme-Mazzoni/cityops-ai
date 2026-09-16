with staging as (
    select * from {{ ref('stg_311_requests') }}
),

resolution_calc as (
    select
        *,
        case 
            when closed_date is not null then extract(epoch from (closed_date - created_date)) / 3600.0
            else null
        end as resolution_time_hours,
        case 
            when closed_date is not null then true 
            else false 
        end as is_closed
    from staging
)

select * from resolution_calc
