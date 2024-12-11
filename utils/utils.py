# correct uri for postgresql
def correct_uri(original_uri):
    # check, whether string starts with "postgres://"
    if original_uri and original_uri.startswith("postgres://"):
        # replace "postgres://" with "postgresql://"
        corrected_uri = original_uri.replace("postgres://", "postgresql://", 1)
    else:
        raise ValueError("Die DATABASE_URI scheint nicht korrekt zu sein oder fehlt.")
    return corrected_uri