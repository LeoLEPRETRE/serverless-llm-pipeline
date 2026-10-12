resource "aws_ecr_repository" "app" {
    name                 = var.project_name
    image_tag_mutability = "IMMUTABLE"
    force_delete         = true

    image_scanning_configuration {
        scan_on_push = true
    }
}

resource "aws_ecr_lifecycle_policy" "app" {
    repository = aws_ecr_repository.app.name

    policy = jsonencode({
        rules = [{
            rulePriority = 1
            selection = {
                tagStatus   = "untagged"
                countType   = "sinceImagePushed"
                countUnit   = "days"
                countNumber = 1
            }
            action = {
                type = "expire"
            }
        },
        {
            rulePriority = 2
            selection = {
                tagStatus   = "any"
                countType   = "imageCountMoreThan"
                countNumber = 5
            }
            action = {
                type = "expire"
            }
        }]
    })
}