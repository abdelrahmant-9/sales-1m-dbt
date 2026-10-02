-- One row per transaction with the money amounts calculated.
select
    s.transaction_id,
    s.sold_at,
    s.sale_date,
    s.sale_month,
    s.customer_id,
    s.product_id,
    s.store_id,
    p.category,
    st.channel,
    s.quantity,
    s.discount_pct,
    {{ money('p.list_price * s.quantity') }}                        as gross_amount,
    {{ money('p.list_price * s.quantity * (1 - s.discount_pct)') }} as net_amount
from {{ ref('stg_sales') }} s
join {{ ref('stg_products') }} p on s.product_id = p.product_id
join {{ ref('stg_stores') }} st  on s.store_id = st.store_id
