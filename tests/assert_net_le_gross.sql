-- A discount can only make the price lower: net must never be bigger than gross.
select * from {{ ref('fct_sales') }} where net_amount > gross_amount
