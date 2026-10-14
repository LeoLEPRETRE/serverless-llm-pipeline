variable "aws_region" {
  type    = string
  default = "eu-north-1"
}

variable "project_name" {
  type    = string
  default = "serverless-llm-pipeline"
}

variable "image_tag" {
  type    = string
  default = "v0.1.2"
}

variable "groq_model" {
  type    = string
  default = "openai/gpt-oss-120b"
}

variable "desired_count" {
  type    = number
  default = 1
}

variable "allowed_cidr" {
  type = string
}