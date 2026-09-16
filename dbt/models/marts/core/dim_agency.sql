with staging as (
    select * from {{ ref('stg_311_requests') }}
),

agencies as (
    select distinct
        agency,
        agency_name
    from staging
    where agency is not null
)

select
    {{ dbt_utils.generate_surrogate_key(['agency']) }} as agency_key,
    agency,
    agency_name
from agencies
