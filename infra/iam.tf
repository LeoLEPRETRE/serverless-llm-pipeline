data "aws_caller_identity" "current" {}

locals {
  groq_api_key_param_name = "/serverless-llm-pipeline/groq-api-key"
  groq_api_key_param_arn  = "arn:aws:ssm:${var.aws_region}:${data.aws_caller_identity.current.account_id}:parameter${local.groq_api_key_param_name}"
}

data "aws_iam_policy_document" "ecs_tasks_assume" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "task_execution" {
  name               = "${var.project_name}-task-execution"
  assume_role_policy = data.aws_iam_policy_document.ecs_tasks_assume.json
}

resource "aws_iam_role_policy_attachment" "task_execution_managed" {
  role       = aws_iam_role.task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

data "aws_iam_policy_document" "read_groq_secret" {
  statement {
    actions   = ["ssm:GetParameters"]
    resources = [local.groq_api_key_param_arn]
  }
}

resource "aws_iam_role_policy" "task_execution_read_secret" {
  name   = "read-groq-secret"
  role   = aws_iam_role.task_execution.id
  policy = data.aws_iam_policy_document.read_groq_secret.json
}