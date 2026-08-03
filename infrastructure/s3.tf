resource "aws_s3_bucket" "data_lake_raw" {
  bucket = "ecom-data-lake-raw-madhu"
}

resource "aws_s3_bucket" "data_lake_stage" {
  bucket = "ecom-data-lake-stage-madhu"
}
