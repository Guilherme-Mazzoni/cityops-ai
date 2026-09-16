with resolution as (
    select * from {{ ref('int_request_resolution') }}
),

sla as (
    select * from {{ ref('int_request_sla') }}
),

location as (
    select * from {{ ref('int_request_location') }}
)

select
    r.unique_key,
    
    -- Foreign Keys
    {{ dbt_utils.generate_surrogate_key(['r.agency']) }} as agency_key,
    {{ dbt_utils.generate_surrogate_key(['r.complaint_type', 'r.descriptor']) }} as complaint_key,
    {{ dbt_utils.generate_surrogate_key(['l.borough', 'l.city', 'l.incident_zip']) }} as location_key,
    
    date(r.created_date) as created_date_key,
    date(r.closed_date) as closed_date_key,
    date(r.due_date) as due_date_key,
    
    -- Dimensions
    r.status,
    r.open_data_channel_type as channel_type,
    
    -- Facts / Metrics
    r.resolution_time_hours,
    s.sla_target_hours,
    
    -- Flags
    r.is_closed,
    s.is_sla_violated,
    l.has_geocoordinates,
    
    -- Geolocations for GIS tools
    l.latitude,
    l.longitude

from resolution r
left join sla s on r.unique_key = s.unique_key
left join location l on r.unique_key = l.unique_key
