from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
from snowflake.snowpark.types import StructField, StructType, IntegerType, StringType, VariantType
from dotenv import load_dotenv
import os


load_dotenv()

account  = os.getenv("ACCOUNT")
user = os.getenv("USER")
password = os.getenv("PASSWORD")

connection_parameters = {
    "user":'your user_name',
    "password":'your password',
    "account":'your account_name',
    "warehouse":'your warehouse_name',
    "database":'your database name',
    "schema":'your schema_name'
}
new_session = Session.builder.configs(connection_parameters).create()

new_session.sql('CREATE OR REPLACE DATABASE snowflake_sample_data;').collect()

new_session.sql('CREATE OR REPLACE SCHEMA tasty_bytes_sample_data.raw_pos;').collect()

new_session.sql('CREATE OR REPLACE STAGE tasty_bytes_sample_data.public.blob_stage url = "s3://sfquickstarts/tastybytes/" file_format = (type = csv);').collect()


menu_schema = StructType([StructField("menu_id",IntegerType()),\
                         StructField("menu_type_id",IntegerType()),\
                         StructField("menu_type",StringType()),\
                         StructField("truck_brand_name",StringType()),\
                         StructField("menu_item_id",IntegerType()),\
                         StructField("menu_item_name",StringType()),\
                         StructField("item_category",StringType()),\
                         StructField("item_subcategory",StringType()),\
                         StructField("cost_of_goods_usd",IntegerType()),\
                         StructField("sale_price_usd",IntegerType()),\
                         StructField("menu_item_health_metrics_obj",VariantType())])

df_blob_stage_read = new_session.read.schema(menu_schema).csv('@tasty_bytes_sample_data.public.blob_stage/raw_pos/menu/')

df_blob_stage_read.write.mode("overwrite").save_as_table("tasty_bytes_sample_data.raw_pos.menu")

df_menu_freezing_point = new_session.table("tasty_bytes_sample_data.raw_pos.menu").filter(col("truck_brand_name") == 'Freezing Point')

print(df_menu_freezing_point.show())

new_session.close()
