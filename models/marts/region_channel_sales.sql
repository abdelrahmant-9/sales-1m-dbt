select
    c.region,
    f.channel,
    count(*)          as transactions,
    {{ money('sum(f.net_amount)') }} as revenue
from {{ ref('fct_sales') }} f
join {{ ref('stg_customers') }} c on f.customer_id = c.customer_id
group by c.region, f.channel
order by revenue desc
