def get_query(username):
    query = """
    {
      user(login: "%s") {
        name
        avatarUrl
        repositories(first: 100) {
          nodes{
            name
          }
        }
      }
    }
    """ % username

    return query
