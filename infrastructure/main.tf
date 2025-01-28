provider "aws" {
    region = "eu-central-1"
}

resource "aws_sns_topic" "input_sns" {
    name = "ab-testing-ctr"
}

resource "aws_iam_role" "lambda_execution" {
    name = "lambda_execution_role"
    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Action = "sts:AssumeRole"
                Effect = "Allow"
                Principal = {
                    Service = "lambda.amazonaws.com"
                }
            }
        ]
    })
}

resource "aws_iam_policy" "lambda_policy" {
    name        = "lambda_policy"
    description = "IAM policy for Lambda execution"
    policy      = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Action = [
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents",
                    "sns:Publish",
                    "rds:*"
                ]
                Effect   = "Allow"
                Resource = "*"
            }
        ]
    })
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
    role       = aws_iam_role.lambda_execution.name
    policy_arn = aws_iam_policy.lambda_policy.arn
}

resource "aws_lambda_function" "lambda_execution" {
    filename         = "../dist/lambda_ctr_function.zip"
    function_name    = "lambda_handler"
    role             = aws_iam_role.lambda_execution.arn
    handler          = "src.app.lambda_handler"
    runtime          = "python3.12"
    source_code_hash = filebase64sha256("../dist/lambda_ctr_function.zip")

    environment {
        variables = {
            DATABASE_HOST     = aws_db_instance.postgres_micro.endpoint
            DATABASE_PORT     = aws_db_instance.postgres_micro.port
            DATABASE_DB_NAME  = aws_db_instance.postgres_micro.db_name
            DATABASE_USER     = aws_db_instance.postgres_micro.username
            DATABASE_PASSWORD = aws_db_instance.postgres_micro.password
        }
    }
}

resource "aws_lambda_permission" "allow_sns" {
    statement_id  = "AllowExecutionFromSNS"
    action        = "lambda:InvokeFunction"
    function_name = aws_lambda_function.lambda_execution.function_name
    principal     = "sns.amazonaws.com"
    source_arn    = aws_sns_topic.input_sns.arn
}

resource "aws_sns_topic_subscription" "sns_labmda_subscription" {
    topic_arn = aws_sns_topic.input_sns.arn
    protocol  = "lambda"
    endpoint  = aws_lambda_function.lambda_execution.arn
}

resource "aws_db_instance" "postgres_micro" {
    allocated_storage    = 20
    engine               = "postgres"
    engine_version       = "17.2"
    instance_class       = "db.t2.micro"
    db_name              = "ctrchallenge"
    username             = "postgres"
    password             = "test123" # not very secure
    parameter_group_name = "default.postgres12"
}