from password_manager_cli import main, load_or_generate_key

# Run the program.
if __name__ == '__main__':
    load_or_generate_key()  # Create or load the key for encryption or decryption.
    main()                  # Run the program's main function.
