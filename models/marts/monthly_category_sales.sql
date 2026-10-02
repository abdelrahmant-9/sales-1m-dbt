select
    sale_month,
    category,
    count(*)                    as transactions,
    sum(quantity)               as units,
    {{ money('sum(net_amount)') }} as revenue,
    {{ money('avg(net_amount)') }} as avg_ticket
from {{ ref('fct_sales') }}
group by sale_month, category
order by sale_month, category
