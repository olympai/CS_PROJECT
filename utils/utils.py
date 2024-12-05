def correct_uri(original_uri):
    # Checken, ob der String korrekt beginnt
    if original_uri and original_uri.startswith("postgres://"):
        # Ersetze "postgres://" mit "postgresql://"
        corrected_uri = original_uri.replace("postgres://", "postgresql://", 1)
    else:
        raise ValueError("Die DATABASE_URI scheint nicht korrekt zu sein oder fehlt.")
    return corrected_uri