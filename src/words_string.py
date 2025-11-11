def words_string(s):
    import re
    return [word for word in re.split('[ ,]+', s.strip()) if word]
