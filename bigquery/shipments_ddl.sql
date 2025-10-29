
CREATE TABLE `your-gcp-project-id.shipments_analytics.shipments`
(
  order_id STRING,
  merchant_id STRING,
  weight FLOAT64,
  volume_cm3 INT64,
  city STRING,
  area STRING,
  status STRING,
  created_at TIMESTAMP,
  delivered_at TIMESTAMP,
  cod_amount FLOAT64,
  commission FLOAT64
)
PARTITION BY
  DATE(created_at)
CLUSTER BY
  city
OPTIONS(
  description="Table for analyzing shipment data, partitioned by creation date and clustered by city."
);
