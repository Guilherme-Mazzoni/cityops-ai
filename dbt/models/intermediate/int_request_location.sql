with staging as (
    select * from {{ ref('stg_311_requests') }}
),

location_clean as (
    select
        unique_key,
        coalesce(borough, 'Unspecified') as borough,
        incident_zip,
        city,
        latitude,
        longitude,
        case 
            when latitude is not null and longitude is not null then true
            else false
        end as has_geocoordinates
    from staging
)

select * from location_clean
