import facebook


def post_to_facebook():
    graph = facebook.GraphAPI(access_token="EAAE2SwiAhjABALfzam8rzni3ZA3kYdcNpBAZBacCU5NkfiClY6l1tv8i9ZAKCfIWXlgVjLEpjlqTyoJQvPw8eBwwZC6IzGZA1RcMd7Kze9LpYdcDAom4HzLUpDoKrzz5OA6l0393jcguTwzc1TLZBZB2xILzaZA2CsBdhAZBjBWbLugILqdDmPNLyYqSLFgngbWYZBheZCaRBZATrwZDZD")
    print(graph)
    # to post to your wall
    graph.put_object("me", "feed", message="Posting on my wall1!")
    # to get your posts/feed
    # feed = graph.get_connections("me", "feed")
    # post = feed["data"]
    # print(post)
    # to put comments for particular post id
    # graph.put_object(post["id"], "comments", message="First!")


post_to_facebook()