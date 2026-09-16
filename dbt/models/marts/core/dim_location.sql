with location_clean as (
    select * from {{ ref('int_request_location') }}
),

locations as (
    select distinct
        borough,
        city,
        incident_zip
    from location_clean
    where borough is not null or city is not null or incident_zip is not null
)

select
    {{ dbt_utils.generate_surrogate_key(['borough', 'city', 'incident_zip']) }} as location_key,
    borough,
    city,
    incident_zip
from locations
