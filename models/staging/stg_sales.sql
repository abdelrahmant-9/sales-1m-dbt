select
    transaction_id,
    sold_at,
    cast(sold_at as date)               as sale_date,
    date_trunc('month', sold_at)::date  as sale_month,
    customer_id,
    product_id,
    store_id,
    quantity,
    discount_pct
from {{ source('raw', 'sales') }}
