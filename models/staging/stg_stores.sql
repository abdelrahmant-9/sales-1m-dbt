select
    store_id,
    store_name,
    channel
from {{ source('raw', 'stores') }}
