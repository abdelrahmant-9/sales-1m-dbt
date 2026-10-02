select
    c.customer_id,
    c.customer_name,
    c.gender,
    c.city,
    r.country,
    r.region
from {{ source('raw', 'customers') }} c
left join {{ ref('city_regions') }} r on c.city = r.city
