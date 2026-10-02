# إزاي تشغّل المشروع (Sales 1M+ rows — dbt)

## أول مرة بس
افتح الفولدر في VS Code ← Terminal (`Ctrl + ~`):

```bash
uv sync
uv run python scripts/generate_data.py
```
التاني بيعمل 1.2 مليون عملية بيع في ملفات CSV ويحمّلهم في DuckDB (حوالي 5 ثواني).

## 1) شغّل dbt
```bash
uv run dbt build
```
لازم تشوف: `Done. PASS=30 WARN=0 ERROR=0`

## 2) Lineage graph
```bash
uv run dbt docs generate
uv run dbt docs serve --port 8082
```
افتح http://localhost:8082

## 3) بُص على النتايج
```bash
uv run python -c "import duckdb; c=duckdb.connect('warehouse/sales.duckdb'); print(c.sql('select count(*) from fct_sales')); print(c.sql('select value_level, count(*) from customer_summary group by 1'))"
```

---

## أسئلة ممكن الإنستراكتور يسألها

**الداتا جاية منين؟**
سكريبت Python بيعمل داتا عشوائية (بـ `random.seed(42)` عشان تطلع نفس الداتا كل مرة) ويحمّلها في schema اسمها `raw`.

**إيه الفرق بين source و seed؟**
source = جدول موجود في الداتابيز قبل dbt (`raw.sales`). seed = ملف CSV صغير جوه المشروع dbt بيحمّله بنفسه (`city_regions.csv`).

**ليه staging views و marts tables؟**
staging تنضيف بسيط ومش محتاج يتخزن. marts بتتقري كتير وفيها 1.2M صف فبخزّنها table عشان الـ queries تبقى أسرع.

**`fct_sales` بيعمل إيه؟**
بيربط كل عملية بيع بالمنتج والفرع، ويحسب `gross_amount` (السعر × الكمية) و `net_amount` (بعد الخصم).

**الـ macro بيعمل إيه؟**
`money()` بيعمل round لرقمين عشريين. بستخدمه في كذا model بدل ما أكتب round كل مرة.

**`value_level` اتحسب إزاي؟**
بجمع كل اللي العميل صرفه: 42 ألف أو أكتر High، من 30 لـ 42 ألف Medium، والباقي Low.

**الـ tests؟**
`unique` و `not_null` على الـ IDs، `relationships` إن كل بيع ليه منتج وفرع وعميل موجودين، `accepted_values` على الـ channel. وفيه test في `tests/` إن السعر بعد الخصم عمره ما يبقى أكبر من قبل الخصم.

**ليه DuckDB مش BigQuery؟**
عشان يشتغل على جهازي ببلاش. الـ SQL هو هو، وفي `profiles.yml` إعدادات BigQuery.
