with staging as (
    select * from {{ ref('stg_311_requests') }}
),

complaints as (
    select distinct
        complaint_type,
        descriptor,
        descriptor_2
    from staging
    where complaint_type is not null
)

select
    {{ dbt_utils.generate_surrogate_key(['complaint_type', 'descriptor']) }} as complaint_key,
    complaint_type,
    descriptor,
    descriptor_2
from complaints
