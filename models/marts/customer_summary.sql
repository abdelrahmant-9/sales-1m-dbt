-- How much each customer bought, and a simple value level.
with customer_sales as (
    select
        customer_id,
        count(*)        as purchases,
        {{ money('sum(net_amount)') }} as total_spent,
        max(sale_date)  as last_purchase_date
    from {{ ref('fct_sales') }}
    group by customer_id
)

select
    c.customer_id,
    c.customer_name,
    c.city,
    c.region,
    cs.purchases,
    cs.total_spent,
    cs.last_purchase_date,
    case
        when cs.total_spent >= 42000 then 'High'
        when cs.total_spent >= 30000 then 'Medium'
        else 'Low'
    end as value_level
from {{ ref('stg_customers') }} c
join customer_sales cs on c.customer_id = cs.customer_id
