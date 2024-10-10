import strawberry

# @strawberry.type
# class Query(VulnerabilityQuery, PolicyQuery):
#     pass

# @strawberry.type
# class Mutation(VulnerabilityMutation, PolicyMutation):
#     pass


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"


# Create the schema
# schema = strawberry.Schema(query=Query, mutation=Mutation)
schema = strawberry.Schema(query=Query)
