from post.serializers import PostSerializer

def create_post(create_data : dict[str, str])-> None:
    hash_tag_data = create_data["hashtags"]
    