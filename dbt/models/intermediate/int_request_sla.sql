with staging as (
    select * from {{ ref('int_request_resolution') }}
),

sla_calc as (
    select
        *,
        case 
            when is_closed = true and due_date is not null and closed_date > due_date then true
            when is_closed = false and due_date is not null and current_timestamp > due_date then true
            else false
        end as is_sla_violated,
        case 
            when due_date is not null then extract(epoch from (due_date - created_date)) / 3600.0
            else null
        end as sla_target_hours
    from staging
)

select * from sla_calc
