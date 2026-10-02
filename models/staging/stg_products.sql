select
    product_id,
    sku,
    category,
    {{ money('list_price') }} as list_price
from {{ source('raw', 'products') }}
