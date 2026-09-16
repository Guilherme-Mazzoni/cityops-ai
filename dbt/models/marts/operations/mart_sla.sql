with facts as (
    select * from {{ ref('fact_service_requests') }}
),

agencies as (
    select * from {{ ref('dim_agency') }}
),

complaints as (
    select * from {{ ref('dim_complaint') }}
),

locations as (
    select * from {{ ref('dim_location') }}
)

select
    f.unique_key,
    a.agency,
    c.complaint_type,
    l.borough,
    f.status,
    f.is_closed,
    f.is_sla_violated,
    f.resolution_time_hours,
    f.sla_target_hours
from facts f
left join agencies a on f.agency_key = a.agency_key
left join complaints c on f.complaint_key = c.complaint_key
left join locations l on f.location_key = l.location_key
