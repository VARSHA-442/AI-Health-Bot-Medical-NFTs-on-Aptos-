from cryptography.fernet import Fernet

def generate_encrypted_file(summary_text, output_path="encrypt.txt", key_path="key.txt"):
    if not summary_text:
        print("DEBUG: summary_text is None or empty.")
        raise ValueError("summary_text is empty or None. Cannot encrypt empty content.")

    # Generate encryption key and cipher
    key = Fernet.generate_key()
    cipher = Fernet(key)

    # Encrypt the summary
    encrypted_summary = cipher.encrypt(summary_text.encode())

    # Write the encrypted summary to file
    with open(output_path, "wb") as file:
        file.write(encrypted_summary)

    # Write the encryption key to file
    with open(key_path, "wb") as key_file:
        key_file.write(key)

    return output_path, key_path


# Example usage
if _name_ == "_main_":
    # This is where you get the summary from (model output or user input)
    summary = "This is a demo medical summary for encryption."  # Replace this with your actual summary logic

    print("DEBUG: Summary before encryption:", summary)

    try:
        enc_file, key_file = generate_encrypted_file(summary)
        print(f"Encrypted summary saved to: {enc_file}")
        print(f"Encryption key saved to: {key_file}")
    except Exception as e:
        print("❌ Error during encryption:", str(e))